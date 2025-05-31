import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np

# Load dataset
ds = xr.open_dataset('/content/cmems_obs-mob_glo_phy-sss_my_multi-oi_P1W_1748597181417.nc')  # Replace with actual file
density = ds['rho'].squeeze()  # Replace 'rho' with actual variable name if different

# Subset for Bay of Bengal region: 5°N–25°N, 80°E–100°E
#if want plot another region than we have to replace bob to region 
ds_bob = ds.sel(latitude=slice(5, 25), longitude=slice(80, 100))
density_bob = ds_bob['rho'].squeeze()

lon = ds_bob['longitude']
lat = ds_bob['latitude']

# Set up the figure
fig = plt.figure(figsize=(10, 8))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([80, 100, 5, 25], crs=ccrs.PlateCarree())
ax.set_facecolor('black')

# Add land
land = cfeature.NaturalEarthFeature('physical', 'land', '50m',
                                    edgecolor='black', facecolor='gray')
ax.add_feature(land, zorder=1)

# Define levels
filled_levels = np.arange(1020, 1030.5, 0.2)
line_levels = np.arange(1020, 1030.5, 0.5)

# Plot filled contours
cf = ax.contourf(lon, lat, density_bob, levels=filled_levels, cmap='plasma',
                 transform=ccrs.PlateCarree(), zorder=0)

# Contour lines
#if want plot another region than we have to replace bob to region 
cl = ax.contour(lon, lat, density_bob, levels=line_levels, colors='black',
                linewidths=0.5, transform=ccrs.PlateCarree(), zorder=2)
ax.clabel(cl, inline=True, fontsize=8, fmt="%.1f")

# Coastlines
ax.coastlines(color='black', linewidth=0.5)

# Colorbar
cbar = plt.colorbar(cf, ax=ax, orientation='horizontal', shrink=0.75, pad=0.06)
cbar.set_label("Sea Water Density (kg/m³)", fontsize=12, weight='bold')
cbar.ax.tick_params(labelsize=10)

# Title
plt.text(0.5, 1.07, "Sea Water Density (kg/m³) - Bay of Bengal",
         transform=ax.transAxes,
         fontsize=17, fontweight='bold', color='black',
         ha='center', va='bottom')

plt.show()
