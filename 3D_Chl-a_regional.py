import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np

# STEP 3: Load dataset
ds = xr.open_dataset('/content/cmems_mod_glo_bgc-pft_anfc_0.25deg_P1D-m_1747584288513.nc')

# STEP 4: Extract the chlorophyll variable (auto-removes singleton dims)
chl = ds['chl'].squeeze()  # dims: (time, latitude, longitude)

# STEP 5: Subset Bay of Bengal region and select first time step
chl_bob = chl.sel(longitude=slice(80, 100), latitude=slice(5, 25)).isel(time=0)

# Get lon/lat values and create meshgrid
lon = chl_bob.longitude.values
lat = chl_bob.latitude.values
lon2d, lat2d = np.meshgrid(lon, lat)

# Get 2D chlorophyll values
chl_values = chl_bob.values

# STEP 6: Plotting
plt.figure(figsize=(10, 8))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([80, 100, 5, 25], crs=ccrs.PlateCarree())
ax.set_facecolor('black')

# Add land
land = cfeature.NaturalEarthFeature('physical', 'land', '50m',
                                    edgecolor='black', facecolor='gray')
ax.add_feature(land, zorder=1)

# Contour levels
filled_levels = np.linspace(0, 5, 50)
line_levels = np.linspace(0, 5, 20)

# Plot filled contours
cf = ax.contourf(lon2d, lat2d, chl_values, levels=filled_levels, cmap='YlGn',
                 transform=ccrs.PlateCarree(), zorder=0)

# Plot contour lines
cl = ax.contour(lon2d, lat2d, chl_values, levels=line_levels, colors='black',
                linewidths=0.5, transform=ccrs.PlateCarree(), zorder=2)
ax.clabel(cl, inline=True, fontsize=8, fmt="%.1f")

# Coastlines
ax.coastlines(resolution='50m', color='black', linewidth=0.6)

# Colorbar
cbar = plt.colorbar(cf, ax=ax, orientation='horizontal', shrink=0.7, pad=0.05)
cbar.set_label("Chlorophyll-a (mg/m³)", fontsize=12, weight='bold')
cbar.ax.tick_params(labelsize=10)

# Title moved ~1cm upward
plt.text(0.5, 1.05, "Chlorophyll-a Concentration (mg/m³) -Bay of Bengal-Winter-2024",
         transform=ax.transAxes, fontsize=19, weight='bold', ha='center')


plt.tight_layout()
plt.show()
