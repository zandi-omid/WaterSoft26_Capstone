# WaterSoft 2026 Capstone

This repository contains a reproducible data pipeline for collecting,
organizing, and analyzing USGS stream-gauge observations together with
project-specific NOAA flood-stage metadata.

The current focus of the project is data preparation, quality control, and
exploratory data analysis for hydrologic applications.

---

# Repository Structure

```text
WaterSoft26_Capstone/
│
├── config/
│   └── gauges.csv                 # List of USGS gauges used in the project
│
├── data/
│   ├── raw/
│   │   ├── noaa/
│   │   └── usgs/
│   │       └── timeseries/         # Downloaded USGS observations
│   │
│   ├── interim/
│   │   └── usgs_gauge_metadata.csv
│   │
│   ├── processed/
│   │   └── master_gauge_metadata.csv
│   │
│   └── samples/                    # Small sample datasets
│
├── docs/                           # Project documentation
│
├── notebooks/
│   └── EDA.ipynb                   # Exploratory data analysis
│
├── scripts/
│   ├── 01_download_usgs_metadata.py
│   ├── 02_build_master_metadata.py
│   └── 03_download_usgs_timeseries.py
│
├── src/
│   └── watersoft/
│       └── __init__.py
│
├── tests/
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

# Setup

Python 3.10 or newer is recommended.

Clone the repository:

```bash
git clone https://github.com/zandi-omid/WaterSoft26_Capstone.git
cd WaterSoft26_Capstone
```

Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

---

# Data Pipeline

## Step 1 — Download USGS metadata

```bash
python scripts/01_download_usgs_metadata.py
```

Output:

```text
data/interim/usgs_gauge_metadata.csv
```

---

## Step 2 — Build the master metadata table

```bash
python scripts/02_build_master_metadata.py
```

Output:

```text
data/processed/master_gauge_metadata.csv
```

---

## Step 3 — Download USGS time-series observations

```bash
python scripts/03_download_usgs_timeseries.py
```

Outputs:

```text
data/raw/usgs/timeseries/
├── usgs_gauge_height_streamflow_long.csv
├── usgs_gauge_height_streamflow_wide.csv
└── usgs_download_summary.csv
```

The downloader retrieves streamflow and gage-height observations in yearly
chunks using parallel requests.

---

# Exploratory Data Analysis

After the pipeline has completed, launch Jupyter:

```bash
jupyter lab
```

Open:

```text
notebooks/EDA.ipynb
```

The notebook reads the generated files from the `data/` directory and performs
basic exploratory analyses, including:

- station metadata inspection
- observation coverage
- missing-value analysis
- download summary
- descriptive statistics
- duplicate detection

---

# Data Organization

| Directory | Description |
|-----------|-------------|
| `data/raw/` | Raw downloaded datasets |
| `data/interim/` | Intermediate files created during processing |
| `data/processed/` | Final processed datasets used by the project |
| `data/samples/` | Small sample datasets for demonstrations and testing |

---

# Gauge Configuration

The gauges used throughout the project are defined in

```text
config/gauges.csv
```

To add or remove gauges, simply edit this file.

---

# Collaboration

Create a new branch before making changes:

```bash
git switch main
git pull --ff-only
git switch -c feature/my-feature
```

After making changes:

```bash
git add .
git commit -m "Describe your changes"
git push -u origin feature/my-feature
```

Then open a Pull Request into `main`.

---

# Notes

Large generated datasets are intentionally excluded from Git. Each collaborator
should generate them locally by running the pipeline scripts.

The `src/watersoft/` package is reserved for reusable Python modules as the
project grows.