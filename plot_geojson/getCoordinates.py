import geopandas as gpd
import pandas as pd

def with_null_values():
    # Load the GeoJSON file
    geojson_path = "C:/Users/carolvfs/Documents/GitHub/react_mapbox_ts/public/Yearly_Precipitation_Sum.json"
    data = gpd.read_file(geojson_path)

    # Get the bounding box of the GeoDataFrame
    minx, miny, maxx, maxy = data.total_bounds

    # Define the coordinates for Mapbox (top-left, top-right, bottom-right, bottom-left)
    mapbox_coordinates = [
        [minx, maxy],  # Top-left
        [maxx, maxy],  # Top-right
        [maxx, miny],  # Bottom-right
        [minx, miny],  # Bottom-left
    ]

    print("Mapbox coordinates:", mapbox_coordinates)

def no_null_values():
    # Load the GeoJSON file
    geojson_path = "C:/Users/carolvfs/Documents/GitHub/react_mapbox_ts/public/Yearly_Precipitation_Sum.json"
    data = gpd.read_file(geojson_path)

    # Ensure the "1980" column is numeric and filter out null values
    data["1980"] = pd.to_numeric(data["1980"], errors="coerce")
    data_cleaned = data[data["1980"].notnull()]  # Keep only rows with non-null values

    # Get the bounding box of the filtered GeoDataFrame
    minx, miny, maxx, maxy = data_cleaned.total_bounds

    # Define the coordinates for Mapbox (top-left, top-right, bottom-right, bottom-left)
    mapbox_coordinates = [
        [minx, maxy],  # Top-left
        [maxx, maxy],  # Top-right
        [maxx, miny],  # Bottom-right
        [minx, miny],  # Bottom-left
    ]

    print("Mapbox coordinates:", mapbox_coordinates)

no_null_values()
