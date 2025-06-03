import xarray as xr
import numpy as np

# Path to your NetCDF file
nc_file = '/content/cmems_mod_glo_bgc-pft_anfc_0.25deg_P1D-m_1747584288513.nc'

# Load the dataset
ds = xr.open_dataset(nc_file)

# Set your Chlorophyll-a variable name
chla_var = 'chl'

# Safely get _FillValue or missing_value attribute
fill_val = ds[chla_var].attrs.get('_FillValue', ds[chla_var].attrs.get('missing_value', None))

if fill_val is not None:
    print(f"Replacing _FillValue ({fill_val}) with NaN...")
    ds[chla_var] = ds[chla_var].where(ds[chla_var] != fill_val, np.nan)
else:
    print(f"No _FillValue or missing_value found for '{chla_var}'.")

# Remove negative and unrealistically high Chl-a values
ds[chla_var] = ds[chla_var].where(ds[chla_var] >= 0)
ds[chla_var] = ds[chla_var].where(ds[chla_var] <= 100)

# Save cleaned dataset
output_file = '/content/cleaned_chla_data.nc'
ds.to_netcdf(output_file)
print(f"✅ Cleaned data saved to: {output_file}")
