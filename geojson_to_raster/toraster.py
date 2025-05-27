import fiona
import rasterio
from rasterio.transform import from_bounds
from rasterio.features import rasterize

# Input parameters
geojson_file = "input.geojson"
attribute_name = "1980"
out_raster = "output.tif"
pixel_size = 30  # Adjust based on your coordinate system units

# 1. Read the GeoJSON features
with fiona.open(geojson_file, "r") as src:
    # Extract geometries and values
    features = list(src)
    # Compute bounds (extent)
    bounds = src.bounds
    # Make sure the attribute exists in features. If not, handle gracefully.
    if not all(attribute_name in f["properties"] for f in features):
        raise ValueError(f"Not all features have the attribute '{attribute_name}'")

# 2. Determine the transform and shape of the output raster
xmin, ymin, xmax, ymax = bounds
width = int((xmax - xmin) / pixel_size)
height = int((ymax - ymin) / pixel_size)

transform = from_bounds(xmin, ymin, xmax, ymax, width, height)

# 3. Prepare (geometry, value) pairs for rasterization
shapes = ((f["geometry"], f["properties"][attribute_name]) for f in features)

# 4. Rasterize the vector data into a numpy array
raster_array = rasterize(
    shapes=shapes,
    out_shape=(height, width),
    transform=transform,
    fill=0,         # Value for areas not covered by any polygon
    dtype="float32" # Adjust data type if needed
)

# 5. Write the numpy array to a GeoTIFF
with rasterio.open(
    out_raster,
    'w',
    driver='GTiff',
    height=height,
    width=width,
    count=1,
    dtype='float32',
    crs=src.crs,
    transform=transform,
) as dst:
    dst.write(raster_array, 1)
