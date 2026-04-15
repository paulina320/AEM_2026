"""Tests for aem.data module."""

import pandas as pd
import pytest

from aem.data import generate_experiment_data, load_sample


class TestLoadSample:
    def test_reaction_times(self):
        df = load_sample("reaction_times")
        assert isinstance(df, pd.DataFrame)
        assert "condition" in df.columns
        assert len(df) > 0

    def test_memory_recall(self):
        df = load_sample("memory_recall")
        assert "strategy" in df.columns

    def test_caffeine_alertness(self):
        df = load_sample("caffeine_alertness")
        assert "dose" in df.columns

    def test_unknown_raises(self):
        with pytest.raises(ValueError, match="Unknown dataset"):
            load_sample("does_not_exist")


class TestGenerateExperimentData:
    def test_default_conditions(self):
        df = generate_experiment_data(seed=0)
        assert set(df["condition"]) == {"control", "treatment"}

    def test_row_count(self):
        df = generate_experiment_data(n_subjects=20, seed=0)
        assert len(df) == 40  # 2 conditions × 20 subjects

    def test_custom_conditions(self):
        df = generate_experiment_data(
            n_subjects=10, conditions=["A", "B", "C"], seed=1
        )
        assert set(df["condition"]) == {"A", "B", "C"}
        assert len(df) == 30

    def test_columns(self):
        df = generate_experiment_data()
        assert set(df.columns) == {"subject_id", "condition", "score"}

    def test_reproducible(self):
        df1 = generate_experiment_data(seed=99)
        df2 = generate_experiment_data(seed=99)
        pd.testing.assert_frame_equal(df1, df2)
