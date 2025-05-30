# MAP_copernicus-file

#if catagory not install

!apt-get install -y libproj-dev proj-data proj-bin libgeos-dev
!pip install cartopy
uploaded = files.upload()
#this is first uplode then work


import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np

# Load the dataset
ds = xr.open_dataset('/content/METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2_1748583129068.nc')
sst = ds['analysed_sst'].squeeze() - 273.15  # Convert Kelvin to Celsius

# Extract coordinate names
lon = ds['longitude']
lat = ds['latitude']

# Set up the figure
fig = plt.figure(figsize=(16, 8))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_facecolor('black')

# Add land features
land = cfeature.NaturalEarthFeature('physical', 'land', '50m',
                                    edgecolor='black',
                                    facecolor='gray')
ax.add_feature(land, zorder=1)

# Define contour levels
filled_levels = np.arange(-2, 32, 1)   # for filled color contours
line_levels = np.arange(-2, 32, 4)     # for black line contours

# Plot filled contours
cf = ax.contourf(lon, lat, sst, levels=filled_levels, cmap='jet',
                 transform=ccrs.PlateCarree(), zorder=0)

# Plot contour lines
cl = ax.contour(lon, lat, sst, levels=line_levels, colors='black',
                linewidths=0.6, transform=ccrs.PlateCarree(), zorder=2)
ax.clabel(cl, inline=True, fontsize=9, fmt="%.0f°C")

# Add coastlines
ax.coastlines(color='black', linewidth=0.5)

# Colorbar
cbar = plt.colorbar(cf, ax=ax, orientation='horizontal', shrink=0.7, pad=0.05)
cbar.set_label("Sea Surface Temperature (°C)", fontsize=12, weight='bold')
cbar.ax.tick_params(labelsize=10)

# Title (moved upward using plt.text)
plt.text(0.5, 1.07, "Sea Surface Temperature (°C)",
         transform=ax.transAxes,
         fontsize=17, fontweight='bold', color='black',
         ha='center', va='bottom')


plt.show()
