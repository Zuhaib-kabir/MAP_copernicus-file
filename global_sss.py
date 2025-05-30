import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np

# Load the dataset
ds = xr.open_dataset('/content/cmems_obs-mob_glo_phy-sss_my_multi-oi_P1W_1748596056160.nc')  # Replace with your actual file name

# Extract salinity variable (g/kg)
salinity = ds['SA'].squeeze()  # Replace 'sa' if your salinity variable is named differently

# Extract coordinates
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

# Define contour levels (adjust if needed for your data range)
filled_levels = np.arange(30, 38.5, 0.25)
line_levels = np.arange(30, 38.5, 1)

# Plot filled contours
cf = ax.contourf(lon, lat, salinity, levels=filled_levels, cmap='viridis',
                 transform=ccrs.PlateCarree(), zorder=0)

# Plot contour lines
cl = ax.contour(lon, lat, salinity, levels=line_levels, colors='black',
                linewidths=0.5, transform=ccrs.PlateCarree(), zorder=2)
ax.clabel(cl, inline=True, fontsize=9, fmt="%.1f")

# Add coastlines
ax.coastlines(color='black', linewidth=0.5)

# Colorbar
cbar = plt.colorbar(cf, ax=ax, orientation='horizontal', shrink=0.7, pad=0.05)
cbar.set_label("Sea Surface Salinity (g/kg)", fontsize=12, weight='bold')
cbar.ax.tick_params(labelsize=10)

# Title (moved upward using plt.text)
plt.text(0.5, 1.07, "Global Sea Surface Salinity (g/kg)",
         transform=ax.transAxes,
         fontsize=17, fontweight='bold', color='black',
         ha='center', va='bottom')

plt.show()
