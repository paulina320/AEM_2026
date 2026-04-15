"""
AEM – Applied Experimental Methods Development Kit
"""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("aem")
except PackageNotFoundError:
    __version__ = "0.1.0"

from .design import (
    full_factorial,
    randomize_order,
    latin_square,
    block_design,
    counterbalance,
)
from .statistics import (
    descriptive_stats,
    t_test,
    anova_one_way,
    effect_size_cohen_d,
    chi_square,
    correlation,
    power_analysis,
)
from .visualization import (
    plot_means,
    plot_distribution,
    plot_interaction,
    plot_residuals,
)
from .data import (
    load_sample,
    generate_experiment_data,
)

__all__ = [
    # design
    "full_factorial",
    "randomize_order",
    "latin_square",
    "block_design",
    "counterbalance",
    # statistics
    "descriptive_stats",
    "t_test",
    "anova_one_way",
    "effect_size_cohen_d",
    "chi_square",
    "correlation",
    "power_analysis",
    # visualization
    "plot_means",
    "plot_distribution",
    "plot_interaction",
    "plot_residuals",
    # data
    "load_sample",
    "generate_experiment_data",
]
