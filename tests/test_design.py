"""Tests for aem.design module."""

import numpy as np
import pandas as pd
import pytest

from aem.design import (
    block_design,
    counterbalance,
    full_factorial,
    latin_square,
    randomize_order,
)


class TestFullFactorial:
    def test_two_by_two(self):
        df = full_factorial({"A": [1, 2], "B": ["low", "high"]})
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 4
        assert set(df.columns) == {"A", "B"}

    def test_three_levels(self):
        df = full_factorial({"X": [1, 2, 3]})
        assert len(df) == 3

    def test_three_factors(self):
        df = full_factorial({"A": [0, 1], "B": [0, 1], "C": [0, 1]})
        assert len(df) == 8

    def test_column_names(self):
        df = full_factorial({"Speed": ["slow", "fast"], "Noise": [0, 1]})
        assert list(df.columns) == ["Speed", "Noise"]


class TestRandomizeOrder:
    def test_returns_same_rows(self):
        df = full_factorial({"A": [1, 2], "B": [3, 4]})
        shuffled = randomize_order(df, seed=0)
        assert len(shuffled) == len(df)
        assert set(shuffled["A"]) == set(df["A"])

    def test_reproducible_with_seed(self):
        df = full_factorial({"A": list(range(10))})
        s1 = randomize_order(df, seed=7)
        s2 = randomize_order(df, seed=7)
        pd.testing.assert_frame_equal(s1, s2)

    def test_reset_index(self):
        df = full_factorial({"A": [1, 2, 3, 4]})
        shuffled = randomize_order(df, seed=1)
        assert list(shuffled.index) == list(range(len(df)))


class TestLatinSquare:
    def test_shape(self):
        ls = latin_square(4, seed=0)
        assert ls.shape == (4, 4)

    def test_rows_contain_all_values(self):
        ls = latin_square(5, seed=1)
        for row in ls:
            assert set(row) == set(range(5))

    def test_columns_contain_all_values(self):
        ls = latin_square(5, seed=2)
        for col in ls.T:
            assert set(col) == set(range(5))

    def test_size_one(self):
        ls = latin_square(1)
        assert ls.shape == (1, 1)
        assert ls[0, 0] == 0


class TestBlockDesign:
    def test_total_rows(self):
        df = block_design(["A", "B", "C"], n_blocks=4, seed=0)
        assert len(df) == 12  # 3 treatments × 4 blocks

    def test_each_block_has_all_treatments(self):
        treatments = ["X", "Y", "Z"]
        df = block_design(treatments, n_blocks=3, seed=0)
        for block_id in df["block"].unique():
            block_treatments = set(df.loc[df["block"] == block_id, "treatment"])
            assert block_treatments == set(treatments)

    def test_columns(self):
        df = block_design(["A"], n_blocks=2)
        assert list(df.columns) == ["block", "treatment"]


class TestCounterbalance:
    def test_three_conditions(self):
        orders = counterbalance(["A", "B", "C"])
        assert len(orders) == 6

    def test_two_conditions(self):
        orders = counterbalance([1, 2])
        assert set(orders) == {(1, 2), (2, 1)}

    def test_returns_list_of_tuples(self):
        orders = counterbalance(["X", "Y"])
        assert isinstance(orders, list)
        assert all(isinstance(o, tuple) for o in orders)
