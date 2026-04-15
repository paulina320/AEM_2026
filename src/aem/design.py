"""
Experimental Design Utilities
==============================
Tools for constructing and randomising experimental designs, including
full-factorial layouts, Latin squares, block designs and counterbalanced
sequences.
"""

from __future__ import annotations

import itertools
import random
from typing import Any, Sequence

import numpy as np
import pandas as pd


def full_factorial(factors: dict[str, Sequence[Any]]) -> pd.DataFrame:
    """
    Generate a full-factorial design table.

    Parameters
    ----------
    factors : dict
        Mapping of factor name to a list of its levels.
        Example: ``{"A": [1, 2], "B": ["low", "high"]}``

    Returns
    -------
    pd.DataFrame
        One row per treatment combination, columns named after the factors.

    Examples
    --------
    >>> df = full_factorial({"Speed": ["slow", "fast"], "Noise": [0, 1]})
    >>> len(df)
    4
    """
    names = list(factors.keys())
    levels = list(factors.values())
    combinations = list(itertools.product(*levels))
    return pd.DataFrame(combinations, columns=names)


def randomize_order(design: pd.DataFrame, seed: int | None = None) -> pd.DataFrame:
    """
    Randomly shuffle the rows of an experimental design.

    Parameters
    ----------
    design : pd.DataFrame
        Design table (e.g., from :func:`full_factorial`).
    seed : int, optional
        Random seed for reproducibility.

    Returns
    -------
    pd.DataFrame
        Shuffled copy of *design* with reset integer index.
    """
    return design.sample(frac=1, random_state=seed).reset_index(drop=True)


def latin_square(n: int, seed: int | None = None) -> np.ndarray:
    """
    Generate a random *n × n* Latin square.

    Each integer from 0 to *n-1* appears exactly once in every row and
    every column.

    Parameters
    ----------
    n : int
        Size of the square (number of treatments).
    seed : int, optional
        Random seed.

    Returns
    -------
    np.ndarray of shape (n, n)

    Examples
    --------
    >>> ls = latin_square(4, seed=0)
    >>> ls.shape
    (4, 4)
    """
    rng = np.random.default_rng(seed)
    # Build first row as a random permutation, then shift cyclically
    first_row = rng.permutation(n)
    square = np.array([(first_row + i) % n for i in range(n)])
    # Shuffle rows and columns
    row_perm = rng.permutation(n)
    col_perm = rng.permutation(n)
    return square[row_perm][:, col_perm]


def block_design(
    treatments: Sequence[Any],
    n_blocks: int,
    seed: int | None = None,
) -> pd.DataFrame:
    """
    Create a randomised complete-block design.

    Each block contains every treatment exactly once, in a random order.

    Parameters
    ----------
    treatments : sequence
        List of treatment labels.
    n_blocks : int
        Number of experimental blocks.
    seed : int, optional
        Random seed.

    Returns
    -------
    pd.DataFrame
        Columns: ``block``, ``treatment``.

    Examples
    --------
    >>> df = block_design(["A", "B", "C"], n_blocks=3, seed=42)
    >>> list(df.columns)
    ['block', 'treatment']
    >>> len(df)
    9
    """
    rng = random.Random(seed)
    rows: list[dict[str, Any]] = []
    for b in range(1, n_blocks + 1):
        order = list(treatments)
        rng.shuffle(order)
        for t in order:
            rows.append({"block": b, "treatment": t})
    return pd.DataFrame(rows)


def counterbalance(conditions: Sequence[Any]) -> list[tuple[Any, ...]]:
    """
    Return all possible orderings of *conditions* (full counterbalancing).

    Parameters
    ----------
    conditions : sequence
        Experimental conditions to counterbalance.

    Returns
    -------
    list of tuple
        All *n!* permutations.

    Examples
    --------
    >>> orders = counterbalance(["A", "B", "C"])
    >>> len(orders)
    6
    """
    return list(itertools.permutations(conditions))
