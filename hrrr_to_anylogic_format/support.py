from netCDF4 import Dataset
import numpy as np
import pandas as pd

def write_results(data, columns, file_path):
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(file_path, index=False)

def kelvin_to_celsius(mtrx):
    return mtrx - 273.15

def build_mask(nc_file, lat_name, lon_name, lat_top_left, lon_top_left, lat_bottom_right, lon_bottom_right):
    dataset = Dataset(nc_file)

    latitudes = dataset.variables[lat_name][:]
    longitudes = dataset.variables[lon_name][:]

    # Handle longitudes in [0, 360] instead of [-180, 180]
    if longitudes.max() > 180:
        longitudes = np.where(longitudes > 180, longitudes - 360, longitudes)

    mask = (
        (latitudes >= lat_bottom_right) & (latitudes <= lat_top_left) &
        (longitudes >= lon_top_left) & (longitudes <= lon_bottom_right)
    )

    return mask, latitudes, longitudes

def mask_variable(nc_file, mask, var_name):
    dataset = Dataset(nc_file)
    variable = dataset[var_name][0]

    masked_variable = np.where(mask, variable, np.nan)
    masked_variable_numeric = masked_variable.astype(np.float64)

    return masked_variable_numeric
