import pandas as pd
import numpy as np
from netCDF4 import Dataset
from shapely.geometry import LineString, Point
from shapely.ops import transform
from shapely.prepared import prep
from pyproj import Transformer
import os
from termcolor import colored

from support import build_mask_lats_lons_points, kelvin_to_celsius

# Coordinates for San Francisco and Chicago
lon_sf, lat_sf = -122.4194, 37.7749  # San Francisco
lon_chi, lat_chi = -87.6298, 41.8781  # Chicago

var_name = 'TMP_2maboveground'
lat_name = 'latitude'
lon_name = 'longitude'

path = "C:/Users/carolvfs/Documents/data/HRRR_2024092300_2024092723"

year = "2024"
month = "09"
day = "23"
# hour = "07"
utc_hour = "12" # cdt: 7am

time_zone = -5

interval = 12

tstamp = 0

date_i = pd.to_datetime(f"{year}-{month}-{day} {utc_hour}:00:00")
date_f = date_i + pd.Timedelta(hours=11)

new_t = 0

nightime = 0
period = "day"

mask = None
avg_array = []
data = []

while tstamp <= 103:
    
    date_i_str_cdt = (date_i + pd.Timedelta(hours=time_zone)).strftime('%Y-%m-%d-%H')
    date_f_str_cdt = (date_f + pd.Timedelta(hours=time_zone)).strftime('%Y-%m-%d-%H')
    dates_cdt = f"{date_i_str_cdt}_{date_f_str_cdt}"
    
    date_i_str_cdt_no_time = (date_i + pd.Timedelta(hours=time_zone)).strftime('%Y-%m-%d')
    
    print(dates_cdt)

    for plus_hour in range(interval):
        active_date = date_i + pd.Timedelta(hours=plus_hour)
        active_date_str = active_date.strftime('%Y%m%d%H')
        
        ncfile = f"{path}/{active_date_str}.nc"
        
        if not os.path.exists(ncfile):
            print(colored(f"File not found: {ncfile}","red" ))
            continue  # Skip to the next file

        print(f"Processing file: {ncfile}")

        dataset = Dataset(ncfile)

        # Read latitudes and longitudes if mask is not yet created
        if mask is None:
            mask, lat_grid, lon_grid, points = build_mask_lats_lons_points(dataset, lat_name, lon_name, lon_sf, lat_sf, lon_chi, lat_chi)
            
        # Read the variable data
        variable = dataset[var_name][:]
        variable = variable[0, :, :]
        dataset.close()

        # Ensure variable has the same shape as lat/lon grids
        if variable.shape != lat_grid.shape:
            print(colored(f"Variable shape {variable.shape} does not match grid shape {lat_grid.shape}", "red"))
            # continue  # Skip if shapes do not match

        # Apply mask to variable
        masked_variable = np.where(mask, variable, np.nan)
        masked_variable = masked_variable.astype(np.float64)
        masked_variable = kelvin_to_celsius(masked_variable)

        # Debug statements
        non_nan_count = np.count_nonzero(~np.isnan(masked_variable))
        # print(f"Non-NaN values in masked_variable: {non_nan_count}")
        # print(f"variable shape: {variable.shape}, mask shape: {mask.shape}")

        if non_nan_count > 0:
            avg_array.append(masked_variable)
        else:
            print(colored(f"All values are NaN after masking for date {active_date_str}.", "red"))

    # Check if avg_array is not empty before computing the mean
    if avg_array:
        avg = np.nanmean(np.stack(avg_array), axis=0)
    else:
        print(colored(f"No valid data in avg_array. Skipping.", "red"))
        avg_array = []
        date_i += pd.Timedelta(hours=interval)
        date_f += pd.Timedelta(hours=interval)

        tstamp += interval
        period = "day" if period == "night" else "night"
        new_t += 1
        continue  # Skip to the next iteration

    # Collect data for points within the mask
    for lat, lon, var_value in zip(lat_grid[mask], lon_grid[mask], avg[mask]):
        lat_rounded = round(lat, 2)
        lon_rounded = round(lon, 2)
        var_value_rounded = round(var_value, 2)

        data.append([lat_rounded, lon_rounded, var_value_rounded])

    # Save the data to CSV files
    df = pd.DataFrame(data, columns=["latitude", "longitude", "value"])
    output_path = f"temperature_{date_i_str_cdt_no_time}_{period}.csv"
    
    df.to_csv(output_path, index=False)
    
    avg_array = []
    data = []

    date_i += pd.Timedelta(hours=interval)
    date_f += pd.Timedelta(hours=interval)

    tstamp += interval

    period = "day" if period == "night" else "night"

    new_t += 1

df_points = pd.DataFrame(points, columns=["latitude", "longitude"])
output_path = "points.csv"
df_points.to_csv(output_path, index=False)

print(f"Number of points collected: {len(points)}")