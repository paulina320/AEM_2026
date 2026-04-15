"""Tests for aem.statistics module."""

import numpy as np
import pandas as pd
import pytest

from aem.statistics import (
    anova_one_way,
    chi_square,
    correlation,
    descriptive_stats,
    effect_size_cohen_d,
    power_analysis,
    t_test,
)


class TestDescriptiveStats:
    def test_basic(self):
        s = descriptive_stats([1, 2, 3, 4, 5])
        assert s["n"] == 5
        assert s["mean"] == pytest.approx(3.0)
        assert s["median"] == pytest.approx(3.0)
        assert s["min"] == 1
        assert s["max"] == 5

    def test_returns_series(self):
        assert isinstance(descriptive_stats([1, 2, 3]), pd.Series)

    def test_std_single_value(self):
        s = descriptive_stats([5.0, 5.0, 5.0])
        assert s["std"] == pytest.approx(0.0)


class TestTTest:
    def test_significant_difference(self):
        g1 = [1, 2, 3, 4, 5]
        g2 = [10, 11, 12, 13, 14]
        res = t_test(g1, g2)
        assert res["p_value"] < 0.05

    def test_no_significant_difference(self):
        rng = np.random.default_rng(0)
        g1 = rng.normal(5, 1, 100)
        g2 = rng.normal(5, 1, 100)
        res = t_test(g1, g2)
        assert res["p_value"] > 0.01  # very likely not significant

    def test_returns_expected_keys(self):
        res = t_test([1, 2, 3], [4, 5, 6])
        for key in ("t", "df", "p_value", "cohen_d"):
            assert key in res.index

    def test_paired(self):
        before = [5, 6, 7, 8, 9]
        after  = [6, 8, 9, 10, 11]
        res = t_test(before, after, paired=True)
        assert res["p_value"] < 0.05

    def test_cohen_d_sign(self):
        res = t_test([1, 2, 3], [4, 5, 6])
        assert res["cohen_d"] < 0  # group1 mean < group2 mean → negative d


class TestAnovaOneWay:
    def test_three_groups_significant(self):
        res = anova_one_way([1, 2, 3], [10, 11, 12], [20, 21, 22])
        assert res["p_value"] < 0.05

    def test_similar_groups_not_significant(self):
        rng = np.random.default_rng(1)
        groups = [rng.normal(5, 1, 30) for _ in range(3)]
        res = anova_one_way(*groups)
        assert res["p_value"] > 0.001  # not strongly significant with equal means

    def test_eta_squared_range(self):
        res = anova_one_way([1, 2, 3], [10, 11, 12], [20, 21, 22])
        assert 0 <= res["eta_squared"] <= 1

    def test_df_values(self):
        res = anova_one_way([1, 2], [3, 4], [5, 6])
        assert res["df_between"] == pytest.approx(2.0)
        assert res["df_within"] == pytest.approx(3.0)


class TestEffectSizeCohenD:
    def test_zero_effect(self):
        d = effect_size_cohen_d([5, 5, 5], [5, 5, 5])
        assert np.isnan(d)  # pooled std = 0

    def test_large_effect(self):
        # Groups separated by 10 SD units → very large effect
        d = effect_size_cohen_d([0, 1, 0, 1], [10, 11, 10, 11])
        assert abs(d) > 2

    def test_symmetry(self):
        d1 = effect_size_cohen_d([1, 2, 3], [4, 5, 6])
        d2 = effect_size_cohen_d([4, 5, 6], [1, 2, 3])
        assert d1 == pytest.approx(-d2)


class TestChiSquare:
    def test_basic(self):
        res = chi_square([[10, 20], [30, 40]])
        assert "p_value" in res.index
        assert "cramers_v" in res.index

    def test_returns_series(self):
        assert isinstance(chi_square([[5, 10], [10, 5]]), pd.Series)

    def test_cramers_v_range(self):
        res = chi_square([[50, 5], [5, 50]])
        assert 0 <= res["cramers_v"] <= 1


class TestCorrelation:
    def test_perfect_positive(self):
        res = correlation([1, 2, 3, 4], [2, 4, 6, 8])
        assert res["r"] == pytest.approx(1.0)

    def test_perfect_negative(self):
        res = correlation([1, 2, 3, 4], [8, 6, 4, 2])
        assert res["r"] == pytest.approx(-1.0)

    def test_n_correct(self):
        res = correlation([1, 2, 3], [4, 5, 6])
        assert res["n"] == 3


class TestPowerAnalysis:
    def test_returns_series(self):
        res = power_analysis(0.5)
        assert isinstance(res, pd.Series)

    def test_n_positive(self):
        res = power_analysis(0.5)
        assert res["n_per_group"] > 0

    def test_larger_effect_needs_fewer_subjects(self):
        small = power_analysis(0.2)
        large = power_analysis(0.8)
        assert large["n_per_group"] < small["n_per_group"]

    def test_given_n_returns_power(self):
        res = power_analysis(0.5, n=100)
        assert 0 < res["power"] <= 1
