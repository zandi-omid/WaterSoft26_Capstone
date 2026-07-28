# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 14:49:54 2026

@author: gomez
"""

#pip install pandas xarray s3fs h5netcdf dask h5py

import os
import s3fs
import xarray as xr
import pandas as pd
import warnings

warnings.filterwarnings("ignore")

def fetch_nwm_forecasts_fast(date_str, cycles, stream_id, config="short_range", save_dir="."):
    fs = s3fs.S3FileSystem(anon=True)
    all_dfs = []
    
    os.makedirs(save_dir, exist_ok=True)
    
    for cycle in cycles:
        cycle_str = str(cycle).zfill(2)
        
        if config == "short_range":
            prefix = f"noaa-nwm-pds/nwm.{date_str}/short_range/nwm.t{cycle_str}z.short_range.channel_rt.f*.conus.nc"
            config_abbr = "sr"
        elif config == "medium_range_mem1":
            prefix = f"noaa-nwm-pds/nwm.{date_str}/medium_range_mem1/nwm.t{cycle_str}z.medium_range.channel_rt_1.f*.conus.nc"
            config_abbr = "mr"
        else:
            raise ValueError("Config must be 'short_range' or 'medium_range_mem1'")
            
        file_paths = sorted(fs.glob(prefix))
        if not file_paths:
            print(f"No files found for {date_str} cycle {cycle_str}Z in {config}.")
            continue
            
        print(f"Fetching {len(file_paths)} files for {date_str} Cycle {cycle_str}Z ({config}) in parallel...")
        
        lead_times = [int(p.split('.f')[-1].split('.')[0]) for p in file_paths]
        
        s3_urls = [f"s3://{p}" for p in file_paths]
        
        def subset_stream(ds):
            return ds.sel(feature_id=stream_id)[['streamflow']]
        
        try:
            ds = xr.open_mfdataset(
                s3_urls, 
                engine='h5netcdf',
                backend_kwargs={"storage_options": {"anon": True}}, 
                combine='nested', 
                concat_dim='time',
                preprocess=subset_stream,
                parallel=True
            )
            
            df = ds.compute().to_dataframe().reset_index()
            
            init_time = pd.to_datetime(f"{date_str}{cycle_str}", format="%Y%m%d%H")
            df['init_time'] = init_time
            df['lead_time_hours'] = lead_times
            df['forecast_datetime'] = df['init_time'] + pd.to_timedelta(df['lead_time_hours'], unit='h')
            df['config'] = config
            cols_to_keep = [
                'init_time', 
                'forecast_datetime', 
                'lead_time_hours', 
                'feature_id', 
                'streamflow', 
                'config'
            ]
            df = df[[c for c in cols_to_keep if c in df.columns]]
            
            filename = f"{stream_id}_{config_abbr}_{date_str}_{cycle_str}Z.csv"
            filepath = os.path.join(save_dir, filename)
            
            df.to_csv(filepath, index=False)
            print(f"Successfully saved data to: {filepath}")
            
            all_dfs.append(df)
            
        except Exception as e:
            print(f"Error processing cycle {cycle_str}: {e}")
            
    if all_dfs:
        return pd.concat(all_dfs, ignore_index=True)
    else:
        return pd.DataFrame()

# ==========================================
# Code Execution
# ==========================================
if __name__ == "__main__":
    TARGET_DATE = "20260728"    # Format: YYYYMMDD
    STREAM_ID = 3168766
    OUTPUT_FOLDER = "./nwm_data"
    
    print("--- SHORT RANGE ---")
    fetch_nwm_forecasts_fast(
        date_str=TARGET_DATE, 
        cycles=[0, 12], 
        stream_id=STREAM_ID, 
        config="short_range",
        save_dir=OUTPUT_FOLDER
    )
    
    print("\n--- MEDIUM RANGE MEM 1 ---")
    fetch_nwm_forecasts_fast(
        date_str=TARGET_DATE, 
        cycles=[0], 
        stream_id=STREAM_ID, 
        config="medium_range_mem1",
        save_dir=OUTPUT_FOLDER
    )