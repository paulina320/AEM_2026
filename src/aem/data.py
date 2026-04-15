"""
Data Loading and Generation
============================
Utilities for loading bundled sample datasets and generating synthetic
experiment data for practice and testing.
"""

from __future__ import annotations

import importlib.resources as pkg_resources
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Built-in sample datasets
# ---------------------------------------------------------------------------

_SAMPLE_DIR = Path(__file__).parent.parent.parent / "data"

_AVAILABLE_SAMPLES: dict[str, str] = {
    "reaction_times": "reaction_times.csv",
    "memory_recall": "memory_recall.csv",
    "caffeine_alertness": "caffeine_alertness.csv",
}


def load_sample(name: str) -> pd.DataFrame:
    """
    Load one of the bundled sample datasets.

    Parameters
    ----------
    name : str
        Dataset name. Available datasets:

        * ``"reaction_times"`` – simple reaction-time experiment
          (between-subjects, two conditions).
        * ``"memory_recall"`` – word-recall study
          (within-subjects, three encoding strategies).
        * ``"caffeine_alertness"`` – caffeine dose × time-of-day factorial
          design with alertness ratings.

    Returns
    -------
    pd.DataFrame

    Raises
    ------
    ValueError
        If *name* is not one of the available datasets.

    Examples
    --------
    >>> df = load_sample("reaction_times")
    >>> "condition" in df.columns
    True
    """
    if name not in _AVAILABLE_SAMPLES:
        raise ValueError(
            f"Unknown dataset '{name}'. "
            f"Available: {list(_AVAILABLE_SAMPLES)}"
        )
    path = _SAMPLE_DIR / _AVAILABLE_SAMPLES[name]
    return pd.read_csv(path)


# ---------------------------------------------------------------------------
# Synthetic data generators
# ---------------------------------------------------------------------------

def generate_experiment_data(
    n_subjects: int = 30,
    conditions: list[str] | None = None,
    effect_size: float = 0.5,
    noise: float = 1.0,
    seed: int | None = 42,
) -> pd.DataFrame:
    """
    Generate a synthetic between-subjects experiment dataset.

    The dependent variable is drawn from a normal distribution; the
    treatment group's mean is shifted by ``effect_size * noise``.

    Parameters
    ----------
    n_subjects : int
        Number of participants per condition.
    conditions : list of str, optional
        Condition labels. Defaults to ``["control", "treatment"]``.
    effect_size : float
        Mean shift for each successive condition (Cohen's *d* units).
    noise : float
        Standard deviation of the within-condition distribution.
    seed : int, optional
        Random seed.

    Returns
    -------
    pd.DataFrame
        Columns: ``subject_id``, ``condition``, ``score``.

    Examples
    --------
    >>> df = generate_experiment_data(n_subjects=20, seed=0)
    >>> set(df["condition"]) == {"control", "treatment"}
    True
    >>> len(df) == 40
    True
    """
    if conditions is None:
        conditions = ["control", "treatment"]
    rng = np.random.default_rng(seed)
    rows: list[dict[str, Any]] = []
    subject_counter = 1
    for i, cond in enumerate(conditions):
        mean = i * effect_size * noise
        scores = rng.normal(loc=mean, scale=noise, size=n_subjects)
        for score in scores:
            rows.append(
                {
                    "subject_id": subject_counter,
                    "condition": cond,
                    "score": round(float(score), 4),
                }
            )
            subject_counter += 1
    return pd.DataFrame(rows)
