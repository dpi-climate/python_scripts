import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd
from PIL import Image  # Import Pillow for GIF support

def build_colormap(geojson_data):
    # Ensure the "1980" column is numeric and filter out null values
    geojson_data["1980"] = pd.to_numeric(geojson_data["1980"], errors="coerce")
    data_cleaned = geojson_data[geojson_data["1980"].notnull()]  # Keep only rows with non-null values

    # Define custom color stops
    color_stops = [
        (0, '#FFFFFF'),
        (76.2, '#E0F3DB'),
        (127, '#C2E699'),
        (203.2, '#78C679'),
        (279.4, '#31A354'),
        (330.2, '#006837'),
        (406.4, '#FFEDA0'),
        (457.2, '#FED976'),
        (533.4, '#FEB24C'),
        (609.6, '#FD8D3C'),
        (660.4, '#FC4E2A'),
        (736.6, '#E31A1C'),
        (812.8, '#BD0026'),
        (863.6, '#800026'),
        (939.8, '#54278F'),
        (990.6, '#756BB1'),
        (1066.8, '#9E9AC8'),
        (1143, '#CBC9E2'),
        (1193.8, '#DADAEB'),
        (1270, '#F2F0F7'),
    ]

    # Create a custom colormap
    values, colors = zip(*color_stops)
    norm = mcolors.Normalize(vmin=min(values), vmax=max(values))
    cmap = mcolors.LinearSegmentedColormap.from_list("custom_colormap", colors, N=256)

    # Plot the data using the custom colormap
    fig, ax = plt.subplots(figsize=(10, 10))
    data_cleaned.plot(
        column="1980",
        cmap=cmap,
        norm=norm,
        # legend=True,
        legend=False,
        # legend_kwds={'label': "1980 Property Value", 'orientation': "horizontal"},
        ax=ax
    )

    # Customize the plot
    # ax.set_title("Visualization of 1980 Property with Custom Colors", fontsize=16)
    plt.axis("off")
    # plt.show()

    return fig

def save_png(fig, png_path, transparent=False):
    fig.savefig(png_path, dpi=300, bbox_inches="tight", transparent=transparent)

def save_gif(fig, png_path, gif_path, transparent=0):
    image = Image.open(png_path)
    image.save(gif_path, format="GIF", transparency=transparent)
    image.save(gif_path, format="GIF")

def count_points(geojson_data):
    points = geojson_data[geojson_data.geometry.type == "Point"]
    point_count = len(points)
    
    print(f"Number of points: {point_count}")



# Load the GeoJSON file
geojson_path = "C:/Users/carolvfs/Documents/GitHub/react_mapbox_ts/public/Yearly_Precipitation_Sum.json"
data = gpd.read_file(geojson_path)

png_path = "C:/Users/carolvfs/Documents/GitHub/urban-planner/public/1980_custom_color_map.png"
gif_path = "C:/Users/carolvfs/Documents/GitHub/urban-planner/public/1980_custom_color_map.gif"

count_points(data)

# fig = build_colormap(data)

