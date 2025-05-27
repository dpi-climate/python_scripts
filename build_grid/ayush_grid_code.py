import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point
from pyproj import Transformer
import os

def create_grid(lat_min, long_min, lat_max, long_max, resolution_km):
    transformer = Transformer.from_crs("epsg:4326", "epsg:3395", always_xy=True)
    xmin, ymin = transformer.transform(long_min, lat_min)
    xmax, ymax = transformer.transform(long_max, lat_max)
    resolution_m = resolution_km * 1000
    rows = int(np.ceil((ymax - ymin) / resolution_m))
    cols = int(np.ceil((xmax - xmin) / resolution_m))
    polygons = []

    for i in range(cols):
        for j in range(rows):
            x0 = xmin + i * resolution_m
            x1 = xmin + (i + 1) * resolution_m
            y0 = ymin + j * resolution_m
            y1 = ymin + (j + 1) * resolution_m
            polygons.append(Polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)]))
    
    grid = gpd.GeoDataFrame({'geometry': polygons}, crs="epsg:3395")
    grid = grid.to_crs("epsg:4326")
    return grid

def read_csv_data(csv_file):
    df = pd.read_csv(csv_file)
    df = df[df['timestamp'] == 0]
    return df

def create_geodataframe(df):
    geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
    gdf = gpd.GeoDataFrame(df, crs="epsg:4326", geometry=geometry)
    return gdf

def area_weighted_temperature(group):
    if len(group) == 1:
        return group['value'].values[0]
    else:
        return np.average(group['value'], weights=group['area'])

xmin, ymin, xmax, ymax = -87.8412, 41.7392, -87.5515, 42.3256  # Example bounds 
resolution = 5  # Grid resolution in kilometers

# Create the grid
grid = create_grid(ymin, xmin, ymax, xmax, resolution)
grid.to_file('grid.shp')

# Read the CSV data
df = read_csv_data('./t2_wrf_t0_t71.csv')

# Create a GeoDataFrame from the CSV data
temperature_gdf = create_geodataframe(df)

# Perform spatial join to intersect temperature points with the grid
joined = gpd.sjoin(temperature_gdf, grid, how="inner", predicate='within')

# Check the joined DataFrame
print("Joined DataFrame:")
print(joined.head())
print(joined.columns)

# Calculate area of each grid cell and add it to the joined DataFrame
grid['area'] = grid.geometry.area
joined = joined.merge(grid[['geometry', 'area']], left_on='index_right', right_index=True)

# Debug the joined DataFrame
print("Joined DataFrame with area:")
print(joined.head())

# Calculate area-weighted average temperature for each grid cell
area_weighted_avg = joined.groupby('index_right').apply(area_weighted_temperature).reset_index()
area_weighted_avg.columns = ['index', 'weighted_avg_temperature']

# Debug the area_weighted_avg DataFrame
print("Area-weighted average DataFrame:")
print(area_weighted_avg.head())

# Merge with original grid to get the final result
grid = grid.merge(area_weighted_avg, left_index=True, right_on='index', how='left')

# Debug the merged grid DataFrame
print("Merged grid DataFrame:")
print(grid.head())

# Save the result to a new shapefile
grid.to_file('./grid_with_temperature.shp')

# Plotting the grid with temperatures
fig, ax = plt.subplots(figsize=(10, 10))
grid.boundary.plot(ax=ax, color='black')
grid.plot(column='weighted_avg_temperature', ax=ax, legend=True, cmap='viridis')
ax.set_aspect('equal')
ax.set_title('Grid with Weighted Average Temperature')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()

# Ensure the shapefile contains all necessary files
expected_files = ['grid_with_temperature.shp', 'grid_with_temperature.shx', 'grid_with_temperature.dbf', 'grid_with_temperature.prj']
missing_files = [file for file in expected_files if not os.path.isfile(file)]
    
if missing_files:
    print(f"Missing files: {', '.join(missing_files)}")
else:
    print("All necessary shapefile components are present.")