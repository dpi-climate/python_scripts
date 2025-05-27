import pandas as pd
import numpy as np
import rasterio
from rasterio.features import shapes
from shapely.geometry import shape
import geopandas as gpd
from rasterio.io import MemoryFile

# Load GeoJSON file
geojson_file = './t2_wrf_t0_t71.geojson'
gdf = gpd.read_file(geojson_file)

# Extract the property '1980' and other relevant attributes
gdf = gdf[['geometry', '1980']]

resolution = 0.04  # Approx 3 km resolution, adjust as needed
min_lon, max_lon = gdf.total_bounds[0], gdf.total_bounds[2]
min_lat, max_lat = gdf.total_bounds[1], gdf.total_bounds[3]
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

# Create a MemoryFile object to store the raster
with MemoryFile() as memfile:
    with memfile.open(
        driver='GTiff',
        height=raster.shape[0],
        width=raster.shape[1],
        count=1,
        dtype=raster.dtype,
        crs='+proj=latlong',
        transform=rasterio.transform.from_origin(min_lon, max_lat, resolution, resolution),
    ) as dataset:
        dataset.write(raster, 1)

        # Read the raster data from the MemoryFile
        with memfile.open() as src:
            image = src.read(1)
            results = (
                {'properties': {'temperature': value}, 'geometry': shape(geom)}
                for geom, value in shapes(image, transform=src.transform)
                if not np.isnan(value)
            )

temperature_polygons = gpd.GeoDataFrame.from_features(results)

# Load census tracts
census_tracts = gpd.read_file('./cb_2018_17_tract_500k.geojson')

# Set CRS for temperature polygons and convert to the same CRS as census tracts
temperature_polygons.crs = census_tracts.crs
temperature_polygons = temperature_polygons.to_crs(census_tracts.crs)

# Perform intersection between temperature polygons and census tracts
intersection = gpd.overlay(census_tracts, temperature_polygons, how='intersection')

# Calculate the area of each intersected geometry
intersection['area'] = intersection.area

# Function to calculate area-weighted temperature
def area_weighted_temperature(group):
    if len(group) == 1:
        return group['temperature'].values[0]
    else:
        return np.average(group['temperature'], weights=group['area'])

# Calculate area-weighted average temperature for each census tract
area_weighted_avg = intersection.groupby('GEOID').apply(area_weighted_temperature).reset_index()
area_weighted_avg.columns = ['GEOID', 'weighted_avg_temperature']

# Merge the calculated temperatures back into the original census tracts
census_tracts = census_tracts.merge(area_weighted_avg, on='GEOID', how='left')

# Save the updated census tracts to a shapefile
census_tracts.to_file('./census_tracts_with_temperature.shp')
