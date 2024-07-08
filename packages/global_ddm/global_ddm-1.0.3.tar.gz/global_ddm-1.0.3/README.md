# Install
Install using pip:
```shell
pip install global_ddm
```
# Description
Python has a library called global_land_mask, which contains sea and land masks with a global resolution of 1km, using GLOBE's DEM dataset（ https://www.ngdc.noaa.gov/mgg/topo/gltiles.html ）. It should be made with an altitude greater than 0 indicating land and less than 0 indicating ocean.
Based on his dataset, first sparsify the spatial accuracy of the dataset from 1km to 5km. Then apply this calculation method: calculate the distance to the nearest sea grid point on land, and calculate the distance to the nearest land grid point on the ocean.
# Simple example
```python
from global_ddm import globe
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import CenteredNorm

lat = np.linspace(-90,90,181)
lon = np.linspace(-180,180,361)

lat,lon = np.meshgrid(lat,lon)
ddm = globe.get_ddm(lat, lon)

plt.figure(figsize=(16,8))
plt.pcolormesh(lon, lat, ddm, cmap='bwr', norm=CenteredNorm())
plt.colorbar()
plt.tight_layout()
plt.show()
```
# API Reference
```python
from global_ddm import globe
globe.xxxx(args)
```
## 1. get_ddm
This function is used to retrieve a boolean array indicating whether the given coordinates are in the ocean.
### Parameters
- `lat`: ndarray or float, latitude in degrees.
- `lon`: ndarray or float, longitude in degrees.
### Returns
- `is_ocean_mask`: ndarray or float, a boolean array denoting whether the corresponding point is in the ocean.
## 2. is_land
This function is used to determine whether the given coordinates are on land.
### Parameters
- `lat`: ndarray or float, latitude in degrees.
- `lon`: ndarray or float, longitude in degrees.
### Returns
- Boolean value indicating whether the coordinates are on land.
## 3. is_ocean
This function is used to determine whether the given coordinates are in the ocean.
### Parameters
- `lat`: ndarray or float, latitude in degrees.
- `lon`: ndarray or float, longitude in degrees.
### Returns
- Boolean value indicating whether the coordinates are in the ocean.

## 4. off_coastline

This function is used to determine whether the distance from the coastline exceeds the specified distance.

### Parameters
- `lat`: ndarray or float, latitude in degrees.
- `lon`: ndarray or float, longitude in degrees.
- `distance`: ndarray or float, distance away from the coastline in kilometers.

### Returns
- Boolean value indicating whether the distance from the coastline exceeds the specified distance.

## 5. on_coastline

This function is used to determine whether the distance from the coastline does not exceed the specified distance.

### Parameters
- `lat`: ndarray or float, latitude in degrees.
- `lon`: ndarray or float, longitude in degrees.
- `distance`: ndarray or float, distance away from the coastline in kilometers.

### Returns
- Boolean value indicating whether the distance from the coastline does not exceed the specified distance.
