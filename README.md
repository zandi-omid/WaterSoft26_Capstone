# WaterSoft 2026 Capstone

This repository contains a reproducible data pipeline for collecting,
organizing, quality-controlling, and analyzing USGS stream-gauge observations
together with project-specific NOAA flood-stage metadata.

The current focus of the project is data preparation, quality control,
exploratory data analysis (EDA), and developing LSTM-based streamflow
forecasting models for comparison with National Weather Service (NWS)
forecast products.

---

# Repository Structure

```text
WaterSoft26_Capstone/
│
├── config/
│   └── gauges.csv                     # List of USGS gauges used in the project
│
├── data/
│   ├── raw/
│   │   ├── noaa/
│   │   └── usgs/
│   │       └── timeseries/
│   │
│   ├── interim/
│   │   └── usgs_gauge_metadata.csv
│   │
│   ├── processed/
│   │   └── master_gauge_metadata.csv
│   │
│   └── samples/
│
├── docs/
│
├── notebooks/
│   └── 01_EDA.ipynb
│
├── scripts/
│   ├── 01_download_usgs_metadata.py
│   ├── 02_build_master_metadata.py
│   ├── 03_download_usgs_timeseries.py
│   └── 04_fill_usgs_timeseries_gaps.py
│
├── src/
├── tests/
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

Install the required packages:

```bash
python -m pip install -r requirements.txt
```

---

# Data Pipeline

## Step 1 — Download USGS metadata

```bash
python scripts/01_download_usgs_metadata.py
```

Output

```text
data/interim/usgs_gauge_metadata.csv
```

---

## Step 2 — Build the master metadata table

```bash
python scripts/02_build_master_metadata.py
```

Output

```text
data/processed/master_gauge_metadata.csv
```

---

## Step 3 — Download USGS time-series observations

```bash
python scripts/03_download_usgs_timeseries.py
```

Outputs

```text
data/raw/usgs/timeseries/
├── usgs_gauge_height_streamflow_long.csv
├── usgs_gauge_height_streamflow_wide.csv
└── usgs_download_summary.csv
```

The downloader retrieves streamflow and gage-height observations in yearly
chunks using parallel requests.

---

## Step 4 — Fill missing observations

```bash
python scripts/04_fill_usgs_timeseries_gaps.py
```

Outputs

```text
data/raw/usgs/timeseries/
├── usgs_gauge_height_streamflow_long_filled.csv
├── usgs_gauge_height_streamflow_wide_filled.csv
└── usgs_gap_filling_summary.csv
```

The script fills the rare missing observations independently for each gauge
using the nearest available observation in time while preserving the original
downloaded datasets.

---

# Exploratory Data Analysis

Launch Jupyter Lab

```bash
jupyter lab
```

Open

```text
notebooks/01_EDA.ipynb
```

The notebook includes analyses such as

- gauge metadata inspection
- observation coverage
- missing-value assessment
- download summary
- descriptive statistics
- duplicate detection
- visualization of streamflow and stage observations

---

# Data Organization

| Directory | Description |
|-----------|-------------|
| `data/raw/` | Raw downloaded datasets |
| `data/interim/` | Intermediate processing products |
| `data/processed/` | Final processed datasets |
| `data/samples/` | Small example datasets |

---

# Gauge Configuration

The gauges used throughout the project are listed in

```text
config/gauges.csv
```

Modify this file to add or remove stations.

---

# Collaboration

To contribute to the project, first synchronize your local repository:

```bash
git switch main
git pull --ff-only
```

Create a new feature branch:

```bash
git switch -c feature/my-feature
```

After making your changes:

```bash
git add .
git commit -m "Describe your changes"
git push -u origin feature/my-feature
```

Open a Pull Request (PR) on GitHub to merge your branch into `main`.

Before starting new work, make sure your local `main` branch is up to date:

```bash
git switch main
git pull --ff-only
```



---

# Notes

Large generated datasets are intentionally excluded from version control.
Each collaborator should generate the datasets locally by running the pipeline.

The `src/` directory is reserved for reusable Python modules as the project
continues to grow.