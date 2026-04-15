"""
Visualization Helpers
======================
Ready-made plotting functions for common experimental-methods figures.
All functions return a :class:`matplotlib.figure.Figure` so results can
be displayed in Jupyter notebooks or saved to disk.
"""

from __future__ import annotations

from typing import Sequence

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def plot_means(
    data: pd.DataFrame,
    x: str,
    y: str,
    hue: str | None = None,
    error_bars: str = "se",
    title: str = "",
) -> plt.Figure:
    """
    Bar chart of group means with error bars.

    Parameters
    ----------
    data : pd.DataFrame
        Long-form data frame.
    x : str
        Column name for the categorical (grouping) variable.
    y : str
        Column name for the continuous dependent variable.
    hue : str, optional
        Second grouping variable for a clustered bar chart.
    error_bars : {"se", "sd", "ci"}
        Type of error bar: standard error, standard deviation, or 95 % CI.
    title : str
        Plot title.

    Returns
    -------
    matplotlib.figure.Figure
    """
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(data=data, x=x, y=y, hue=hue, errorbar=error_bars, ax=ax)
    ax.set_title(title or f"Mean {y} by {x}")
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    if hue is not None:
        ax.legend(title=hue)
    fig.tight_layout()
    return fig


def plot_distribution(
    data: Sequence[float] | pd.Series,
    label: str = "values",
    bins: int | str = "auto",
    title: str = "",
) -> plt.Figure:
    """
    Histogram with a kernel-density overlay.

    Parameters
    ----------
    data : array-like
        Numeric observations.
    label : str
        Label for the x-axis.
    bins : int or str
        Number of histogram bins (passed to :func:`matplotlib.pyplot.hist`).
    title : str
        Plot title.

    Returns
    -------
    matplotlib.figure.Figure
    """
    arr = np.asarray(data, float)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(arr, bins=bins, density=True, alpha=0.6, color="steelblue", edgecolor="white")
    sns.kdeplot(arr, ax=ax, color="darkblue", linewidth=2)
    ax.set_xlabel(label)
    ax.set_ylabel("Density")
    ax.set_title(title or f"Distribution of {label}")
    fig.tight_layout()
    return fig


def plot_interaction(
    data: pd.DataFrame,
    x: str,
    y: str,
    group: str,
    title: str = "",
) -> plt.Figure:
    """
    Interaction plot (line chart of group means).

    Parameters
    ----------
    data : pd.DataFrame
        Long-form data frame.
    x : str
        Factor plotted on the x-axis.
    y : str
        Dependent variable (continuous).
    group : str
        Second factor whose levels become separate lines.
    title : str
        Plot title.

    Returns
    -------
    matplotlib.figure.Figure
    """
    means = data.groupby([x, group], observed=True)[y].mean().reset_index()
    fig, ax = plt.subplots(figsize=(7, 4))
    for name, grp in means.groupby(group, observed=True):
        ax.plot(grp[x].astype(str), grp[y], marker="o", label=str(name))
    ax.set_xlabel(x)
    ax.set_ylabel(f"Mean {y}")
    ax.set_title(title or f"Interaction: {y} ~ {x} × {group}")
    ax.legend(title=group)
    fig.tight_layout()
    return fig


def plot_residuals(
    fitted: Sequence[float],
    residuals: Sequence[float],
    title: str = "",
) -> plt.Figure:
    """
    Residuals-vs-fitted plot for regression diagnostics.

    Parameters
    ----------
    fitted : array-like
        Fitted (predicted) values.
    residuals : array-like
        Model residuals.
    title : str
        Plot title.

    Returns
    -------
    matplotlib.figure.Figure
    """
    f, r = np.asarray(fitted, float), np.asarray(residuals, float)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.scatter(f, r, alpha=0.6, color="steelblue", edgecolors="white")
    ax.axhline(0, color="red", linestyle="--", linewidth=1)
    ax.set_xlabel("Fitted values")
    ax.set_ylabel("Residuals")
    ax.set_title(title or "Residuals vs Fitted")
    fig.tight_layout()
    return fig
