# WaterSoft 2026 Capstone

This repository contains a reproducible data pipeline for collecting and
analyzing USGS stream-gauge observations and related NOAA flood-stage metadata.
The initial study area includes gauges in the Nueces River basin in Texas.

## Repository contents

- `download_data.py`: downloads metadata for the selected USGS gauges.
- `build_master_metadata.py`: combines USGS metadata with project-specific
  NOAA reach and flood-stage information.
- `download_gauge_timeseries.py`: downloads instantaneous streamflow and gage
  height observations in parallel yearly chunks.
- `EDA.py`: performs initial checks of coverage and missing values.
- `usgs_gauge_metadata.csv`: downloaded USGS station metadata.
- `master_gauge_metadata.csv`: combined project metadata.

## Setup

Python 3.10 or newer is recommended.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run the pipeline

Run the scripts from the repository root:

```bash
python download_data.py
python build_master_metadata.py
python download_gauge_timeseries.py
python EDA.py
```

The time-series downloader requests calendar-year chunks concurrently. Adjust
`MAX_DOWNLOAD_WORKERS` in `download_gauge_timeseries.py` if necessary; the
default is four simultaneous requests.

## Data policy

Generated time-series files are intentionally excluded from Git because they
can be hundreds of megabytes or larger. Each collaborator should regenerate
them locally with `download_gauge_timeseries.py`. Small files ending in
`_sample.csv` may be committed when a shared example is useful.

Expected generated files:

```text
data/usgs_timeseries/usgs_gauge_height_streamflow_long.csv
data/usgs_timeseries/usgs_gauge_height_streamflow_wide.csv
data/usgs_timeseries/usgs_download_summary.csv
```

## Collaboration

Create a short-lived branch for each task and open a pull request into `main`.
Keep pull requests focused, request at least one collaborator review, and avoid
committing generated data or machine-specific files.

```bash
git switch main
git pull --ff-only
git switch -c feature/descriptive-task-name
```
