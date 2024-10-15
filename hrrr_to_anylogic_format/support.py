from netCDF4 import Dataset
import numpy as np
import pandas as pd

from shapely.geometry import LineString, Point
from shapely.ops import transform
from shapely.prepared import prep
from pyproj import Transformer


def build_mask_lats_lons_points(dataset, lat_name, lon_name, lon_a, lat_a, lon_b, lat_b):
    points = []

    latitudes = dataset.variables[lat_name][:]
    longitudes = dataset.variables[lon_name][:]

    # Handle longitudes in [0, 360] instead of [-180, 180]
    if longitudes.max() > 180:
        longitudes = np.where(longitudes > 180, longitudes - 360, longitudes)

    if latitudes.ndim == 1 and longitudes.ndim == 1:
        # Create grid of latitudes and longitudes
        lon_grid, lat_grid = np.meshgrid(longitudes, latitudes)
    else:
        # latitudes and longitudes are already 2D grids
        lat_grid = latitudes
        lon_grid = longitudes

    # Flatten the grids
    lat_flat = lat_grid.flatten()
    lon_flat = lon_grid.flatten()

    # Define the route in WGS84
    route_wgs84 = LineString([(lon_a, lat_a), (lon_b, lat_b)])

    # Define transformer
    transformer = Transformer.from_crs('epsg:4326', 'esri:102003', always_xy=True)

    # Project the route
    route_proj = transform(transformer.transform, route_wgs84)

    # Create buffer around route (e.g., 50 km)
    buffer_distance = 200000  # in meters
    route_buffer_proj = route_proj.buffer(buffer_distance)

    # Project the grid points
    x_flat, y_flat = transformer.transform(lon_flat, lat_flat)

    # Create shapely Points
    points_proj = [Point(xy) for xy in zip(x_flat, y_flat)]

    # Prepare the buffer geometry
    prep_route_buffer_proj = prep(route_buffer_proj)

    # Compute the mask
    mask_flat = np.array([prep_route_buffer_proj.contains(point) for point in points_proj])

    # Reshape the mask to the grid shape
    mask = mask_flat.reshape(lat_grid.shape)

    # Print mask statistics
    print(f"Mask has {np.sum(mask)} True values out of {mask.size} total points.")

    # Get the masked latitudes and longitudes
    latitudes_masked = lat_grid[mask]
    longitudes_masked = lon_grid[mask]

    for lat, lon in zip(latitudes_masked, longitudes_masked):
        lat_rounded = round(lat, 2)
        lon_rounded = round(lon, 2)
        points.append([lat_rounded, lon_rounded])

    return mask, lat_grid, lon_grid, points

def build_mask(dataset, lat_name, lon_name, lat_top_left, lon_top_left, lat_bottom_right, lon_bottom_right):
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

def kelvin_to_celsius(mtrx):
    return mtrx - 273.15

def mask_variable(dataset, mask, var_name):
    
    variable = dataset[var_name][0]

    masked_variable = np.where(mask, variable, np.nan)
    masked_variable_numeric = masked_variable.astype(np.float64)

    return masked_variable_numeric

if __name__ == "__main__":

    var_name = 'TMP_2maboveground'
    lat_name = 'latitude'
    lon_name = 'longitude'

    path = "C:/Users/carolvfs/Documents/data/HRRR_2024092300_2024092723"
    ncfile = f"{path}/2024092300.nc"
    dataset = Dataset(ncfile)

    lon_sf, lat_sf = -122.4194, 37.7749  # San Francisco
    lon_chi, lat_chi = -87.6298, 41.8781  # Chicago

    mask, lat_grid, lon_grid, points = build_mask_lats_lons_points(dataset, lat_name, lon_name, lon_sf, lat_sf, lon_chi, lat_chi)

    

