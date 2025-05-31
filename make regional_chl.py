import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np

# Load your dataset
ds = xr.open_dataset('/content/cmems_mod_glo_bgc-pft_anfc_0.25deg_P1D-m_1748593976926.nc')  # <-- Change to your filename

# Inspect your dataset to find the variable name if unknown
# print(ds)

# Extract Chlorophyll-a and subset BoB region (80–100°E, 5–25°N)
chl = ds['chl'].squeeze()  # <-- Replace with your actual variable name
chl_bob = chl.sel(longitude=slice(80, 100), latitude=slice(5, 25))    #if want plot another region than we have to replace bob to region 

# Get lon/lat
lon = chl_bob['longitude']
lat = chl_bob['latitude']

# Set up the plot
fig = plt.figure(figsize=(10, 8))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([80, 100, 5, 25], crs=ccrs.PlateCarree())  # Zoom to BoB

# Set background color
ax.set_facecolor('black')

# Add land
land = cfeature.NaturalEarthFeature('physical', 'land', '50m',
                                    edgecolor='black', facecolor='gray')
ax.add_feature(land, zorder=1)

# Contour levels
filled_levels = np.linspace(0, 5, 50)
line_levels = np.linspace(0, 5, 20)

# Plot filled contours
#if want plot another region than we have to replace bob to region 
cf = ax.contourf(lon, lat, chl_bob, levels=filled_levels, cmap='YlGn',
                 transform=ccrs.PlateCarree(), zorder=0)

# Plot contour lines
cl = ax.contour(lon, lat, chl_bob, levels=line_levels, colors='black',
                linewidths=0.5, transform=ccrs.PlateCarree(), zorder=2)
ax.clabel(cl, inline=True, fontsize=8, fmt="%.1f")

# Coastlines and features
ax.coastlines(color='black', linewidth=0.5)

# Colorbar
cbar = plt.colorbar(cf, ax=ax, orientation='horizontal', shrink=0.7, pad=0.05)
cbar.set_label("Chlorophyll-a (mg/m³)", fontsize=12, weight='bold')
cbar.ax.tick_params(labelsize=10)

# Title
plt.text(0.5, 1.07, "Chlorophyll-a Concentration (mg/m³) - Bay of Bengal",
         transform=ax.transAxes, fontsize=17, fontweight='bold', color='black',
         ha='center', va='bottom')

plt.show()

