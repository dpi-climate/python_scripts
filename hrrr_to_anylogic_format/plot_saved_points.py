import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point

url = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"

# Read the points.csv file
df = pd.read_csv("points.csv")

# Create a GeoDataFrame from the CSV data
geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
gdf = gpd.GeoDataFrame(df, geometry=geometry)

# Plot the points
# world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world = gpd.read_file(url)

# Set up the plot
fig, ax = plt.subplots(figsize=(10, 10))

# Plot the world map as a base layer
world.plot(ax=ax, color='lightgray')

# Plot the points from the points.csv file
gdf.plot(ax=ax, marker='o', color='red', markersize=5)

# Add titles and labels
# plt.title('Points along the Route from San Francisco to Chicago')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# Show the plot
plt.show()
