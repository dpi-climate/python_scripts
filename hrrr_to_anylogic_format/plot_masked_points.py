from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Coordinates for the bounding box
lat_top_left = 45.97
lon_top_left = -124.37
lat_bottom_right = 34.03
lon_bottom_right = -87.21894471194958

# lat_top_left = 42.510225759855686
# lon_top_left = -88.83649485961635
# lat_bottom_right = 41.30775734879674
# lon_bottom_right = -87.54692281997878

# Path to your NetCDF file
path = "C:/Users/carolvfs/Documents/data/HRRR_2024092300_2024092723"
ncfile = f"{path}/2024092415.nc"

# Open the NetCDF file
dataset = Dataset(ncfile)

# Extract latitude and longitude data
latitudes = dataset.variables['latitude'][:]
longitudes = dataset.variables['longitude'][:]

# Adjust longitudes if they are in 0-360 format instead of -180 to 180
if longitudes.max() > 180:
    longitudes = np.where(longitudes > 180, longitudes - 360, longitudes)

# Create a mask for points within the bounding box
mask = (
    (latitudes >= lat_bottom_right) & (latitudes <= lat_top_left) &
    (longitudes >= lon_top_left) & (longitudes <= lon_bottom_right)
)

# Masked points
masked_latitudes = latitudes[mask]
masked_longitudes = longitudes[mask]

# Chicago coordinates
chicago_lat = 41.8781
chicago_lon = -87.6298

# Plotting the masked points using Cartopy
plt.figure(figsize=(10, 6))

# Use a PlateCarree projection for lat/lon grid
ax = plt.axes(projection=ccrs.PlateCarree())

# Add coastlines and state borders for reference
ax.coastlines()
ax.add_feature(cfeature.BORDERS)
ax.add_feature(cfeature.STATES, edgecolor='gray')

# Plot the masked points
plt.scatter(masked_longitudes, masked_latitudes, color='red', s=8, label='Masked Points', transform=ccrs.PlateCarree())

# Plot Chicago as a text label near the city's location
ax.text(chicago_lon, chicago_lat, 'Chicago', transform=ccrs.PlateCarree(), fontsize=12, verticalalignment='bottom', color='blue')

# Set extent to the bounding box area
ax.set_extent([lon_top_left, lon_bottom_right, lat_bottom_right, lat_top_left])

# Add title and legend
plt.title('Masked Points in the Bounding Box')
plt.legend()

# Save the plot as a PNG file
plt.savefig('sf-chicago.png', format='png', dpi=300)

# Show the plot
plt.show()
