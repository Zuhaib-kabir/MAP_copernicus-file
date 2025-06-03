import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np

# STEP 3: Load dataset
ds = xr.open_dataset('/content/cleaned_chla_data.nc')

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

# Create a meshgrid from lon and lat to match the shape of mhw_intensity
lon, lat = np.meshgrid(lon, lat)

# Add land
land = cfeature.NaturalEarthFeature('physical', 'land', '50m',
                                    edgecolor='black', facecolor='gray')
ax.add_feature(land, zorder=1)

# Contour levels
filled_levels = np.linspace(0, 0.5, 10)
line_levels = np.linspace(0, 0.5, 10)

# Plot filled contours
cf = ax.contourf(lon2d, lat2d, chl_values, levels=filled_levels, cmap='viridis',
                 transform=ccrs.PlateCarree(), zorder=0)

# Plot contour lines
cl = ax.contour(lon2d, lat2d, chl_values, levels=line_levels, colors='black',
                linewidths=0.1, transform=ccrs.PlateCarree(), zorder=1)
ax.clabel(cl, inline=True, fontsize=8, fmt="%.1f")

# Add a custom ash-colored mask for coastal land areas
ash_color = 'lightgray'  # Ash color for the coastal land fill
land_feature = cfeature.NaturalEarthFeature(
    category='physical', name='land', scale='10m',
    facecolor=ash_color, edgecolor='black'
)
ax.add_feature(land_feature)

# Coastlines
ax.coastlines(resolution='50m', color='black', linewidth=0.4)

# Add gridlines and disable top and right labels
gl = ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
gl.top_labels = False  # Remove top axis labels
gl.right_labels = False  # Remove right axis labels
gl.bottom_labels = True  # Keep bottom axis labels
gl.left_labels = True    # Keep left axis labels

# Plot the MHW Intensity data
vmin, vmax = 0, 0.3  # Set the range for MHW Intensity
levels = np.linspace(vmin, vmax, 21)  # Levels for the contour





# Colorbar
cbar = plt.colorbar(cf, ax=ax, orientation='vertical', shrink=0.8, pad=0.05)
cbar.set_label("Chlorophyll-a (mg/m³)", fontsize=12, weight='bold')
cbar.set_ticks(np.arange(vmin, vmax + 0.1, 0.1))
cbar.ax.yaxis.set_tick_params(color='black')


# Multi-line title moved upward
plt.text(0.5, 1.07, "Chlorophyll-a Concentration (mg/m³) - Bay of Bengal\nWinter - 2024",
         transform=ax.transAxes, fontsize=16, weight='bold', ha='center', va='bottom')



plt.tight_layout()
plt.show()
