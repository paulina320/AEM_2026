# AEM 2026 – Applied Experimental Methods

> **Development Kit** for the Applied Experimental Methods 2026 course.

This repository contains a Python package (`aem`) and a set of Jupyter
notebooks that cover the core tools and methods taught in the course:
experimental design, statistical analysis, and result visualisation.

---

## 📦 Package Overview

| Module | What it provides |
|---|---|
| `aem.design` | Full-factorial tables, randomisation, Latin squares, block designs, counterbalancing |
| `aem.statistics` | Descriptive stats, *t*-tests, one-way ANOVA, Cohen's *d*, χ², Pearson *r*, power analysis |
| `aem.visualization` | Bar charts of means, distribution plots, interaction plots, residuals-vs-fitted |
| `aem.data` | Three bundled sample datasets + synthetic-data generator |

---

## 🚀 Quick Start

### 1  Clone the repository

```bash
git clone https://github.com/paulina320/AEM_2026.git
cd AEM_2026
```

### 2  Create a virtual environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows
```

### 3  Install the package and its dependencies

```bash
pip install -e ".[dev]"
```

Or install just the runtime dependencies:

```bash
pip install -r requirements.txt
pip install -e .
```

### 4  Launch the notebooks

```bash
jupyter notebook notebooks/
```

---

## 📓 Notebooks

| Notebook | Topic |
|---|---|
| [`01_introduction.ipynb`](notebooks/01_introduction.ipynb) | Package overview, sample datasets, descriptive statistics |
| [`02_experimental_design.ipynb`](notebooks/02_experimental_design.ipynb) | Full-factorial designs, Latin squares, block designs, counterbalancing |
| [`03_statistical_analysis.ipynb`](notebooks/03_statistical_analysis.ipynb) | *t*-tests, ANOVA, effect sizes, correlation, power analysis, interaction plots |

---

## 🗃️ Sample Datasets

Located in `data/`. All datasets are included as CSV files.

| Dataset | Description |
|---|---|
| `reaction_times.csv` | Two-condition between-subjects reaction-time experiment |
| `memory_recall.csv` | Within-subjects word-recall study (3 encoding strategies) |
| `caffeine_alertness.csv` | 3 × 2 factorial: caffeine dose × time of day, alertness ratings |

Load them with:

```python
import aem

rt  = aem.load_sample("reaction_times")
mem = aem.load_sample("memory_recall")
caf = aem.load_sample("caffeine_alertness")
```

---

## 🔧 API Reference

### Experimental Design

```python
# Full-factorial design table
df = aem.full_factorial({"instruction": ["explicit", "implicit"],
                          "feedback": ["immediate", "delayed"]})

# Shuffle trial order (reproducibly)
df_rand = aem.randomize_order(df, seed=42)

# 4 × 4 Latin square
ls = aem.latin_square(4, seed=0)

# Randomised complete-block design
bd = aem.block_design(["control", "A", "B"], n_blocks=5, seed=0)

# All possible orderings (counterbalancing)
orders = aem.counterbalance(["cond1", "cond2", "cond3"])
```

### Statistical Analysis

```python
# Descriptive statistics
stats = aem.descriptive_stats(data)

# Independent-samples t-test
result = aem.t_test(group1, group2)

# One-way ANOVA
result = aem.anova_one_way(group1, group2, group3)

# Cohen's d effect size
d = aem.effect_size_cohen_d(group1, group2)

# Chi-square test of independence
result = aem.chi_square([[10, 20], [30, 40]])

# Pearson correlation
result = aem.correlation(x, y)

# Prospective power analysis (sample-size planning)
result = aem.power_analysis(effect_size=0.5, alpha=0.05, power=0.80)
```

### Visualisation

```python
import matplotlib.pyplot as plt

fig = aem.plot_means(df, x="condition", y="score")
fig = aem.plot_distribution(data, label="Score")
fig = aem.plot_interaction(df, x="dose", y="alertness", group="time_of_day")
fig = aem.plot_residuals(fitted_values, residuals)

plt.show()
```

---

## 🧪 Running the Tests

```bash
pytest
```

---

## 📁 Repository Structure

```
AEM_2026/
├── README.md
├── pyproject.toml          # package metadata and build config
├── requirements.txt        # pinned runtime dependencies
├── src/
│   └── aem/
│       ├── __init__.py
│       ├── design.py       # experimental design utilities
│       ├── statistics.py   # statistical analysis tools
│       ├── visualization.py# plotting helpers
│       └── data.py         # data loading / generation
├── notebooks/
│   ├── 01_introduction.ipynb
│   ├── 02_experimental_design.ipynb
│   └── 03_statistical_analysis.ipynb
├── data/
│   ├── reaction_times.csv
│   ├── memory_recall.csv
│   └── caffeine_alertness.csv
└── tests/
    ├── test_design.py
    ├── test_statistics.py
    └── test_data.py
```

---

## 📋 Requirements

- Python ≥ 3.10  
- numpy, scipy, pandas, matplotlib, seaborn, statsmodels, scikit-learn

---

## 📜 License

MIT
