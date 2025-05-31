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

# Subset the data to Bay of Bengal region
sst_bob = sst.sel(longitude=slice(80, 100), latitude=slice(5, 25))
lon_bob = sst_bob['longitude']
lat_bob = sst_bob['latitude']     #if want plot another region than we have to replace bob to region 

fig = plt.figure(figsize=(10, 6))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_facecolor('black')

# Add land
land = cfeature.NaturalEarthFeature('physical', 'land', '50m',
                                    edgecolor='black', facecolor='gray')
ax.add_feature(land, zorder=1)

# Contour levels
filled_levels = np.arange(-2, 32, 1)
line_levels = np.arange(-2, 32, 1)

# Filled contours                
#if want plot another region than we have to replace bob to region 
cf = ax.contourf(lon_bob, lat_bob, sst_bob, levels=filled_levels, cmap='jet',   
                 transform=ccrs.PlateCarree(), zorder=0)

# Contour lines
cl = ax.contour(lon_bob, lat_bob, sst_bob, levels=line_levels, colors='black',
                linewidths=0.6, transform=ccrs.PlateCarree(), zorder=2)
ax.clabel(cl, inline=True, fontsize=9, fmt="%.0f°C")

# Gridlines and coastlines
ax.coastlines(resolution='50m', color='black', linewidth=0.5)
gl = ax.gridlines(draw_labels=True)
gl.xlines = False
gl.ylines = False


# Colorbar
cbar = plt.colorbar(cf, ax=ax, orientation='horizontal', shrink=0.7, pad=0.05)
cbar.set_label("Sea Surface Temperature (°C)", fontsize=12, weight='bold')
cbar.ax.tick_params(labelsize=10)

# Title (moved upward using plt.text)
plt.text(.5, 1.1, "Sea Surface Temperature (°C) - Bay of Bengal",
         transform=ax.transAxes,
         fontsize=17, fontweight='bold', color='black',
         ha='center', va='bottom')

plt.show()
