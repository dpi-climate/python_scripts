import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from netCDF4 import Dataset

path = "C:/Users/carolvfs/Documents/data/HRRR_2024092300_2024092723"
ncfile = f"{path}/2024092415.nc"

# Open the NetCDF file
dataset = Dataset(ncfile)

# Extract data
latitudes = dataset.variables['latitude'][:]
longitudes = dataset.variables['longitude'][:]
variable = dataset.variables['TMP_2maboveground'][0]  # The first time step

# Create a figure with a specific projection
fig = plt.figure(figsize=(10, 6))
ax = plt.axes(projection=ccrs.PlateCarree())

# Plot the variable data
contour = ax.contourf(longitudes, latitudes, variable, 60, transform=ccrs.PlateCarree(), cmap='coolwarm')

# Add coastlines and borders for better context
ax.coastlines()
ax.add_feature(cfeature.BORDERS, linestyle=':')

# Add colorbar
cbar = plt.colorbar(contour, ax=ax, orientation='horizontal', pad=0.05)
cbar.set_label('Temperature (K)')

# Add title
plt.title('2m Temperature (Kelvin)')

# Show the plot
plt.show()
