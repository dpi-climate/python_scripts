import geopandas as gpd
import numpy as np
from shapely.geometry import Point, Polygon
import json

# Load your GeoJSON file
geojson_file = "C:/Users/carolvfs/Documents/GitHub/react_mapbox_ts/public/Yearly_Precipitation_Sum.json"
with open(geojson_file, "r") as file:
    data = json.load(file)

# Create a GeoDataFrame from the GeoJSON
gdf = gpd.GeoDataFrame.from_features(data["features"])

# Get the bounds of the data
minx, miny, maxx, maxy = gdf.total_bounds

# Define the resolution (1 km in degrees, approximately)
resolution = 0.01  # Adjust as necessary for your coordinate system

# Create a rectangular grid
x_coords = np.arange(minx, maxx + resolution, resolution)
y_coords = np.arange(miny, maxy + resolution, resolution)
grid_points = [Point(x, y) for x in x_coords for y in y_coords]

# Create a GeoDataFrame for the grid
grid_gdf = gpd.GeoDataFrame(geometry=grid_points, crs=gdf.crs)

# Spatial join to match grid points with existing data
joined_gdf = gpd.sjoin(grid_gdf, gdf, how="left", predicate="intersects")

# Add a 'value' column with existing data or set to null
joined_gdf["value"] = joined_gdf["1980"].fillna("null")

# Convert back to GeoJSON if needed
rectangular_grid_geojson = joined_gdf.to_json()

# Save to a file
output_file = "rectangular_grid.geojson"

with open(output_file, "w") as file:
    file.write(rectangular_grid_geojson)
print(f"Rectangular grid saved to {output_file}")