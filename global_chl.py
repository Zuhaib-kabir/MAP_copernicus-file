import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np

# Load the dataset (update path and variable name if needed)
ds = xr.open_dataset('/content/cmems_mod_glo_bgc-pft_anfc_0.25deg_P1D-m_1748593976926.nc')  # Replace with your file
chl = ds['chl']  # Replace with the actual Chl-a variable name
chl = chl.squeeze()  # Remove singleton dimensions if any

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

# Define contour levels for chlorophyll
filled_levels = np.linspace(0, 5, 50)  # Adjust max value as needed
line_levels = np.linspace(0, 5, 11)

# Plot filled contours
cf = ax.contourf(lon, lat, chl, levels=filled_levels, cmap='YlGn',
                 transform=ccrs.PlateCarree(), zorder=0)

# Plot contour lines
cl = ax.contour(lon, lat, chl, levels=line_levels, colors='black',
                linewidths=0.5, transform=ccrs.PlateCarree(), zorder=2)
ax.clabel(cl, inline=True, fontsize=8, fmt="%.1f")

# Add coastlines
ax.coastlines(color='black', linewidth=0.5)

# Colorbar
cbar = plt.colorbar(cf, ax=ax, orientation='horizontal', shrink=0.7, pad=0.05)
cbar.set_label("Chlorophyll-a Concentration (mg/m³)", fontsize=12, weight='bold')
cbar.ax.tick_params(labelsize=10)

# Title (moved upward using plt.text)
plt.text(0.5, 1.07, "Chlorophyll-a Concentration (mg/m³)",
         transform=ax.transAxes,
         fontsize=17, fontweight='bold', color='black',
         ha='center', va='bottom')

plt.show()
