import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from pyproj import Transformer

def create_grid(lat_min, long_min, lat_max, long_max, resolution_km):

    #converting coordinate system WGS84
    transformer = Transformer.from_crs("epsg:4326", "epsg:3395", always_xy=True)

    #transform latitude and logitude to meters
    xmin, ymin = transformer.transform(long_min, lat_min)
    xmax, ymax = transformer.transform(long_max, lat_max)

    #converting km resolution to m
    resolution_m = resolution_km * 1000

    #Calculates the amount of rows and columns needed for the grid calculated by resolution
    rows = int(np.ceil((ymax - ymin) / resolution_m))
    cols = int(np.ceil((xmax-xmin) / resolution_m))

    #empty set of polygon
    polygons = []

    #creates the grid by adding values of each position in the polygons set
    for i in range(cols):
        for j in range(rows):
            x0 = xmin + i * resolution_m
            x1 = xmin + (i + 1) * resolution_m
            y0 = ymin + j * resolution_m
            y1 = ymin + (j + 1) * resolution_m
            polygons.append(Polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)]))
    

     # Create a GeoDataFrame
    grid = gpd.GeoDataFrame({'geometry': polygons}, crs="epsg:3395")
    
    # Convert the grid back to latitude and longitude
    grid = grid.to_crs("epsg:4326")

    return grid

xmin, ymin, xmax, ymax = -87.8412, 41.7392, -87.5515, 42.3256  # Example bounds 
resolution = 1

# Create the grid
grid = create_grid(ymin, xmin, ymax, xmax, resolution)

# Save the grid to a shapefile
grid.to_file('grid.shp')

# Ensure the shapefile contains all necessary files
import os
expected_files = ['grid.shp', 'grid.shx', 'grid.dbf', 'grid.prj']
missing_files = [file for file in expected_files if not os.path.isfile(file)]

if missing_files:
    print(f"Missing files: {', '.join(missing_files)}")
else:
    print("All necessary shapefile components are present.")

# Plotting the grid
fig, ax = plt.subplots(figsize=(10, 10))

# Plot each polygon in the grid
for geom in grid.geometry:
    if geom.is_valid:
        x, y = geom.exterior.xy
        ax.plot(x, y, color='black')

ax.set_aspect('equal')  # Set aspect ratio to be equal
ax.set_title('Grid')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()