import numpy as np
import rasterio
import geopandas as gpd
from shapely.geometry import box
from rasterio.io import MemoryFile

# Load GeoJSON file
geojson_file = "C:/Users/carolvfs/Documents/GitHub/react_mapbox_ts/public/Yearly_Precipitation_Sum.json"
gdf = gpd.read_file(geojson_file)

# Extract relevant attributes
gdf = gdf[['geometry', '1980']]

# Define the resolution and bounds
# resolution = 0.04  # Approx 3 km resolution, adjust as needed
# resolution = 0.009  # A close approximation for 1 km resolution in both latitude and longitude in the US
resolution = 0.008  # A close approximation for 1 km resolution in both latitude and longitude in the US
min_lon, min_lat, max_lon, max_lat = gdf.total_bounds
ncols = int((max_lon - min_lon) / resolution) + 1
nrows = int((max_lat - min_lat) / resolution) + 1

# Create an empty raster with NaN values
raster = np.full((nrows, ncols), np.nan, dtype=np.float32)

# Populate raster with values from GeoJSON
for i, row in gdf.iterrows():
    geom = row['geometry']
    value = row['1980']
    if geom.is_empty or np.isnan(value):
        continue

    # Calculate bounds for the geometry to determine where to place it in the raster
    bounds = geom.bounds
    min_col = int((bounds[0] - min_lon) / resolution)
    max_col = int((bounds[2] - min_lon) / resolution)
    min_row = int((max_lat - bounds[3]) / resolution)
    max_row = int((max_lat - bounds[1]) / resolution)

    for r in range(min_row, max_row + 1):
        for c in range(min_col, max_col + 1):
            if 0 <= r < nrows and 0 <= c < ncols:
                raster[r, c] = value

# Save the raster to a GeoTIFF file
output_file = 'output.tif'
with rasterio.open(
    output_file,
    'w',
    driver='GTiff',
    height=raster.shape[0],
    width=raster.shape[1],
    count=1,
    dtype=raster.dtype,
    crs='+proj=latlong',
    transform=rasterio.transform.from_origin(min_lon, max_lat, resolution, resolution),
) as dataset:
    dataset.write(raster, 1)

print(f"Raster saved to {output_file}")
