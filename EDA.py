#%%
import pandas as pd

df = pd.read_csv("usgs_gauge_metadata.csv")

print(df.head())
print(df.columns)
print(df.info())

# %%
import pandas as pd

path = "data/usgs_timeseries/usgs_gauge_height_streamflow_wide.csv"

df = pd.read_csv(
    "data/usgs_timeseries/usgs_gauge_height_streamflow_wide.csv",
    dtype={"site_id": str},
    parse_dates=["datetime"],
)

df["site_id"] = df["site_id"].str.zfill(8)

print(df.shape)
print(df.columns.tolist())
print(df.head())

print("\nDate coverage by gauge:")
print(
    df.groupby("site_id")["datetime"]
    .agg(["min", "max", "count"])
)

print("\nMissing values:")
print(
    df[["streamflow_cfs", "gage_height_ft"]]
    .isna()
    .sum()
)

# %%

summary = pd.read_csv(
    "data/usgs_timeseries/usgs_download_summary.csv"
)

print(summary.to_string(index=False))
print("\nFailed requests:")
print(summary.loc[summary["status"] != "success"])
# %%
