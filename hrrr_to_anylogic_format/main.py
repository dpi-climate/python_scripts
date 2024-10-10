from support import build_mask, mask_variable, kelvin_to_celsius, write_results
import pandas as pd
import numpy as np

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
            mask, latitudes, longitudes = build_mask(ncfile, lat_name, lon_name, lat_top_left, lon_top_left, lat_bottom_right, lon_bottom_right)

            for lat, lon in zip(latitudes[mask], longitudes[mask]):
                points.append([lat, lon])
            
        masked_variable = mask_variable(ncfile, mask, var_name)
        masked_variable = kelvin_to_celsius(masked_variable)

        avg_array.append(masked_variable)

    avg = np.mean(np.stack(avg_array), axis=0)  
    avg_array = []

    date_i += pd.Timedelta(hours=interval)
    date_f += pd.Timedelta(hours=interval)

    tf += interval
    ti += interval

    new_format_timestamp = 0 if new_format_timestamp == 1 else 1

    new_t += 1

    write_results(data, ["latitude", "longitude", "value", "datetime", "timestamp"], "temperature.csv")
    write_results(points, ["latitude", "longitude"], "points.csv")
