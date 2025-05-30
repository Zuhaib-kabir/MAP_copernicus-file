import xarray as xr

# Open the file
ds = xr.open_dataset('/content/cmems_obs-mob_glo_phy-sss_my_multi-oi_P1W_1748597181417.nc')

# Print all variables
print(ds.data_vars)
