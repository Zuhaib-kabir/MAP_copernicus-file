import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np

# Load the dataset
ds = xr.open_dataset('/content/cmems_obs-mob_glo_phy-sss_my_multi-oi_P1W_1748596056160.nc')  # Replace with actual filename

# Extract salinity (assumed to be in g/kg, usually 'sa')
salinity = ds['SA'].squeeze()

# Subset for Bay of Bengal: lon (80–100°E), lat (0–25°N)
bob = salinity.sel(longitude=slice(80, 100), latitude=slice(0, 25))
lon = bob['longitude']
lat = bob['latitude']

# Set up the figure
fig = plt.figure(figsize=(10, 8))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([80, 100, 0, 25], crs=ccrs.PlateCarree())  # Bay of Bengal bounds
ax.set_facecolor('black')

# Add land features
land = cfeature.NaturalEarthFeature('physical', 'land', '50m',
                                    edgecolor='black', facecolor='gray')
ax.add_feature(land, zorder=1)

# Define levels
filled_levels = np.arange(30, 38.5, 0.25)
line_levels = np.arange(30, 38.5, 0.5)

# Plot filled contours
cf = ax.contourf(lon, lat, bob, levels=filled_levels, cmap='viridis',
                 transform=ccrs.PlateCarree(), zorder=0)

# Contour lines
cl = ax.contour(lon, lat, bob, levels=line_levels, colors='black',
                linewidths=0.5, transform=ccrs.PlateCarree(), zorder=2)
ax.clabel(cl, inline=True, fontsize=8, fmt="%.1f")

# Coastlines
ax.coastlines(color='black', linewidth=0.5)

# Colorbar
cbar = plt.colorbar(cf, ax=ax, orientation='horizontal', shrink=0.7, pad=0.05)
cbar.set_label("Sea Surface Salinity (g/kg)", fontsize=12, weight='bold')
cbar.ax.tick_params(labelsize=10)

# Title (1cm upward with underline style)
plt.text(0.5, 1.07, "Sea Surface Salinity (g/kg) - Bay of Bengal",
         transform=ax.transAxes,
         fontsize=17, fontweight='bold', color='black',
         ha='center', va='bottom', style='normal', family='sans-serif')

plt.show()
