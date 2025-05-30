import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np

# Load dataset
ds = xr.open_dataset('/content/cmems_obs-mob_glo_phy-sss_my_multi-oi_P1W_1748597181417.nc')  # Replace with your actual file
density = ds['rho'].squeeze()  # Adjust to match the actual variable name

# Get coordinates
lon = ds['longitude']
lat = ds['latitude']

# Set up the figure
fig = plt.figure(figsize=(16, 8))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_global()
ax.set_facecolor('black')

# Add land
land = cfeature.NaturalEarthFeature('physical', 'land', '50m',
                                    edgecolor='black', facecolor='gray')
ax.add_feature(land, zorder=1)

# Define levels (adjust as needed)
filled_levels = np.arange(1020, 1030.5, 0.2)
line_levels = np.arange(1020, 1030.5, 0.5)

# Plot filled contours
cf = ax.contourf(lon, lat, density, levels=filled_levels, cmap='plasma',
                 transform=ccrs.PlateCarree(), zorder=0)

# Contour lines
cl = ax.contour(lon, lat, density, levels=line_levels, colors='black',
                linewidths=0.5, transform=ccrs.PlateCarree(), zorder=2)
ax.clabel(cl, inline=True, fontsize=8, fmt="%.1f")

# Add coastlines
ax.coastlines(color='black', linewidth=0.5)

# Colorbar
cbar = plt.colorbar(cf, ax=ax, orientation='horizontal', shrink=0.7, pad=0.05)
cbar.set_label("Sea Water Density (kg/m³)", fontsize=12, weight='bold')
cbar.ax.tick_params(labelsize=10)

# Title
plt.text(0.5, 1.07, "Global Sea Water Density (kg/m³)",
         transform=ax.transAxes,
         fontsize=17, fontweight='bold', color='black',
         ha='center', va='bottom')

plt.show()
