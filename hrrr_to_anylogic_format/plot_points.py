from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Coordinates for the bounding box
lat_top_left = 45.96515752022081
lon_top_left = -124.37257188287798
lat_bottom_right = 34.0336856583888
lon_bottom_right = -87.21894471194958

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

# Plotting the masked points using Cartopy
plt.figure(figsize=(10, 6))

# Use a PlateCarree projection for lat/lon grid
ax = plt.axes(projection=ccrs.PlateCarree())

# Add coastlines and state borders for reference
ax.coastlines()
ax.add_feature(cfeature.BORDERS)
ax.add_feature(cfeature.STATES, edgecolor='gray')

# Plot the masked points
plt.scatter(masked_longitudes, masked_latitudes, color='red', s=10, label='Masked Points', transform=ccrs.PlateCarree())

# Set extent to the bounding box area
ax.set_extent([lon_top_left, lon_bottom_right, lat_bottom_right, lat_top_left])

# Add title and legend
plt.title('Masked Points in the Bounding Box')
plt.legend()

# Show the plot
plt.show()
