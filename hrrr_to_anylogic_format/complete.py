import pandas as pd
import numpy as np
from netCDF4 import Dataset

lat_top_left = 45.96515752022081
lon_top_left = -124.37257188287798
lat_bottom_right = 34.0336856583888
lon_bottom_right = -87.21894471194958

var_name = 'TMP_2maboveground'
lat_name = 'latitude'
lon_name = 'longitude'

path = "C:/Users/carolvfs/Documents/data/HRRR_2024092300_2024092723"

year = "2024"
month = "09"
day = "23"
hour = "07"

interval = 12

ti = 0
tf = 11

date_i = pd.to_datetime(f"{year}-{month}-{day} {hour}:00:00")
date_f = date_i + pd.Timedelta(hours=11)

new_t = 0

new_format_timestamp = 0

mask = []
avg_array = []
data = []
points = []

while ti <= 103:
    date_i_str = date_i.strftime('%Y-%m-%d-%H')
    date_f_str = date_f.strftime('%Y-%m-%d-%H')
    dates = f"{date_i_str}_{date_f_str}"
    print(dates)

    for plus_hour in range(interval):
        active_date = date_i + pd.Timedelta(hours=plus_hour)
        active_date_str = active_date.strftime('%Y%m%d%H')
        
        ncfile = f"{path}/{active_date_str}.nc"
        # print(ncfile)
        
        if not isinstance(mask, np.ndarray):
            dataset = Dataset(ncfile)

            latitudes = dataset.variables[lat_name][:]
            longitudes = dataset.variables[lon_name][:]

            # Handle longitudes in [0, 360] instead of [-180, 180]
            if longitudes.max() > 180:
                longitudes = np.where(longitudes > 180, longitudes - 360, longitudes)

            mask = (
                (latitudes >= lat_bottom_right) & (latitudes <= lat_top_left) &
                (longitudes >= lon_top_left) & (longitudes <= lon_bottom_right)
            )

            for lat, lon in zip(latitudes[mask], longitudes[mask]):
                points.append([lat, lon])
            
        variable = dataset[var_name][0]

        masked_variable = np.where(mask, variable, np.nan)
        masked_variable = masked_variable.astype(np.float64)
        masked_variable = masked_variable - 273.15

        avg_array.append(masked_variable)

    avg = np.mean(np.stack(avg_array), axis=0)

    for lat, lon, var_value in zip(latitudes[mask], longitudes[mask], avg[mask]):
        data.append([lat, lon, var_value, dates, new_format_timestamp])
    
    avg_array = []

    date_i += pd.Timedelta(hours=interval)
    date_f += pd.Timedelta(hours=interval)

    tf += interval
    ti += interval

    new_format_timestamp = 0 if new_format_timestamp == 1 else 1

    new_t += 1

df = pd.DataFrame(data, columns=["latitude", "longitude", "value", "datetime", "timestamp"])
output_path = "temperature.csv"
df.to_csv(output_path, index=False)

df = pd.DataFrame(points, columns=["latitude", "longitude"])
output_path = "points.csv"
df.to_csv(output_path, index=False)
