"""
Statistical Analysis Tools
============================
Convenience wrappers around :mod:`scipy.stats` and :mod:`statsmodels`
for the analyses most commonly encountered in experimental research:
descriptive statistics, *t*-tests, one-way ANOVA, effect sizes, χ²
tests, Pearson correlation, and prospective power analysis.
"""

from __future__ import annotations

from typing import Sequence

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.power import TTestIndPower


# ---------------------------------------------------------------------------
# Descriptive statistics
# ---------------------------------------------------------------------------

def descriptive_stats(data: Sequence[float] | pd.Series) -> pd.Series:
    """
    Compute common descriptive statistics for a 1-D sample.

    Parameters
    ----------
    data : array-like
        Numeric observations.

    Returns
    -------
    pd.Series
        Index: ``n``, ``mean``, ``median``, ``std``, ``sem``, ``min``,
        ``max``, ``skewness``, ``kurtosis``.

    Examples
    --------
    >>> s = descriptive_stats([1, 2, 3, 4, 5])
    >>> s["mean"]
    3.0
    """
    arr = np.asarray(data, dtype=float)
    return pd.Series(
        {
            "n": len(arr),
            "mean": float(np.mean(arr)),
            "median": float(np.median(arr)),
            "std": float(np.std(arr, ddof=1)),
            "sem": float(stats.sem(arr)),
            "min": float(np.min(arr)),
            "max": float(np.max(arr)),
            "skewness": float(stats.skew(arr)),
            "kurtosis": float(stats.kurtosis(arr)),
        }
    )


# ---------------------------------------------------------------------------
# Inferential tests
# ---------------------------------------------------------------------------

def t_test(
    group1: Sequence[float],
    group2: Sequence[float],
    equal_var: bool = True,
    paired: bool = False,
) -> pd.Series:
    """
    Perform an independent-samples or paired *t*-test.

    Parameters
    ----------
    group1, group2 : array-like
        Numeric observations for the two groups.
    equal_var : bool
        If ``True`` (default), assume equal variances (Student's *t*).
        If ``False``, use Welch's correction.
    paired : bool
        If ``True``, treat groups as paired (within-subjects).

    Returns
    -------
    pd.Series
        ``t``, ``df``, ``p_value``, ``cohen_d``.

    Examples
    --------
    >>> res = t_test([1, 2, 3], [4, 5, 6])
    >>> res["p_value"] < 0.05
    True
    """
    a, b = np.asarray(group1, float), np.asarray(group2, float)
    if paired:
        result = stats.ttest_rel(a, b)
        df = len(a) - 1
    else:
        result = stats.ttest_ind(a, b, equal_var=equal_var)
        df = result.df
    d = effect_size_cohen_d(group1, group2)
    return pd.Series({"t": result.statistic, "df": float(df), "p_value": result.pvalue, "cohen_d": d})


def anova_one_way(*groups: Sequence[float]) -> pd.Series:
    """
    One-way between-subjects ANOVA (Fisher's *F*-test).

    Parameters
    ----------
    *groups : array-like
        Two or more groups of numeric observations.

    Returns
    -------
    pd.Series
        ``F``, ``df_between``, ``df_within``, ``p_value``, ``eta_squared``.

    Examples
    --------
    >>> res = anova_one_way([1, 2, 3], [4, 5, 6], [7, 8, 9])
    >>> res["p_value"] < 0.05
    True
    """
    arrays = [np.asarray(g, float) for g in groups]
    f_stat, p_val = stats.f_oneway(*arrays)
    k = len(arrays)
    n_total = sum(len(a) for a in arrays)
    grand_mean = np.mean(np.concatenate(arrays))
    ss_between = sum(len(a) * (np.mean(a) - grand_mean) ** 2 for a in arrays)
    ss_total = sum(np.sum((a - grand_mean) ** 2) for a in arrays)
    eta_sq = ss_between / ss_total if ss_total > 0 else float("nan")
    return pd.Series(
        {
            "F": f_stat,
            "df_between": float(k - 1),
            "df_within": float(n_total - k),
            "p_value": p_val,
            "eta_squared": eta_sq,
        }
    )


def effect_size_cohen_d(
    group1: Sequence[float],
    group2: Sequence[float],
) -> float:
    """
    Compute Cohen's *d* (pooled-SD version).

    Parameters
    ----------
    group1, group2 : array-like
        Numeric observations.

    Returns
    -------
    float

    Examples
    --------
    >>> round(effect_size_cohen_d([1, 2, 3], [4, 5, 6]), 4)
    -3.0
    """
    a, b = np.asarray(group1, float), np.asarray(group2, float)
    mean_diff = np.mean(a) - np.mean(b)
    pooled_std = np.sqrt(
        ((len(a) - 1) * np.var(a, ddof=1) + (len(b) - 1) * np.var(b, ddof=1))
        / (len(a) + len(b) - 2)
    )
    return float(mean_diff / pooled_std) if pooled_std > 0 else float("nan")


def chi_square(
    observed: Sequence[Sequence[float]],
) -> pd.Series:
    """
    Pearson's χ² test of independence for a contingency table.

    Parameters
    ----------
    observed : 2-D array-like
        Observed frequency table.

    Returns
    -------
    pd.Series
        ``chi2``, ``p_value``, ``df``, ``cramers_v``.

    Examples
    --------
    >>> res = chi_square([[10, 20], [30, 40]])
    >>> "p_value" in res.index
    True
    """
    table = np.asarray(observed, float)
    chi2, p_val, df, _ = stats.chi2_contingency(table)
    n = table.sum()
    k = min(table.shape) - 1
    cramers_v = float(np.sqrt(chi2 / (n * k))) if n > 0 and k > 0 else float("nan")
    return pd.Series({"chi2": chi2, "p_value": p_val, "df": float(df), "cramers_v": cramers_v})


def correlation(
    x: Sequence[float],
    y: Sequence[float],
) -> pd.Series:
    """
    Pearson correlation between two variables.

    Parameters
    ----------
    x, y : array-like
        Paired numeric observations.

    Returns
    -------
    pd.Series
        ``r``, ``p_value``, ``n``.

    Examples
    --------
    >>> res = correlation([1, 2, 3, 4], [2, 4, 6, 8])
    >>> res["r"]
    1.0
    """
    a, b = np.asarray(x, float), np.asarray(y, float)
    r, p = stats.pearsonr(a, b)
    return pd.Series({"r": float(r), "p_value": float(p), "n": len(a)})


# ---------------------------------------------------------------------------
# Power analysis
# ---------------------------------------------------------------------------

def power_analysis(
    effect_size: float,
    alpha: float = 0.05,
    power: float = 0.80,
    n: int | None = None,
) -> pd.Series:
    """
    Compute sample size (or power) for an independent-samples *t*-test.

    Provide either *n* **or** leave it as ``None`` to compute the required *n*
    for the given *power*.

    Parameters
    ----------
    effect_size : float
        Cohen's *d*.
    alpha : float
        Significance level (default 0.05).
    power : float
        Desired statistical power (default 0.80).
    n : int, optional
        If given, compute the achieved power for that *n* per group.

    Returns
    -------
    pd.Series
        ``effect_size``, ``alpha``, ``power``, ``n_per_group``.

    Examples
    --------
    >>> res = power_analysis(0.5)
    >>> res["n_per_group"] > 0
    True
    """
    analysis = TTestIndPower()
    if n is None:
        n_required = analysis.solve_power(effect_size=effect_size, alpha=alpha, power=power)
        achieved_power = power
    else:
        n_required = float(n)
        achieved_power = analysis.solve_power(effect_size=effect_size, alpha=alpha, nobs1=n)
    return pd.Series(
        {
            "effect_size": effect_size,
            "alpha": alpha,
            "power": achieved_power,
            "n_per_group": float(np.ceil(n_required)),
        }
    )
