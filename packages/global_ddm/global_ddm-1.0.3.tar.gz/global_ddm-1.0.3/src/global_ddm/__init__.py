from netCDF4 import Dataset
import os
import numpy as np

current_dir = os.path.dirname(__file__)
ncfile = os.path.join(current_dir, "ddm_5km.nc")
data = Dataset(ncfile, "r")
dlat = data['lat'][:][::-1]
dlon = data['lon'][:]
ddm = data['ddm'][:][::-1, :]

def lat_to_index(lat):
    """
    Convert latitude to index on the mask

    Parameters
    ----------
    lat : numeric
        Latitude to get in degrees

    Returns
    -------
    index : numeric
        index of the latitude axis.

    """
    lat = np.array(lat)

    if np.any(lat>90):
        raise ValueError('latitude must be <= 90')

    if np.any(lat<-90):
        raise ValueError('latitude must be >= -90')


    lat[lat > dlat.max()] = dlat.max()
    lat[lat < dlat.min()] = dlat.min()

    return np.round(((lat - dlat[0])/(dlat.max()-dlat.min())*(dlat.size - 1)), 0).astype(int)

def lon_to_index(lon):
    """
    Convert longitude to index on the mask

    Parameters
    ----------
    lon : numeric
        Longitude to get in degrees

    Returns
    -------
    index : numeric
        index of the longitude axis.

    """

    lon = np.array(lon)

    if np.any(lon > 180):
        raise ValueError('longitude must be <= 180')

    if np.any(lon < -180):
        raise ValueError('longitude must be >= -180')


    lon[lon > dlon.max()] = dlon.max()
    lon[lon < dlon.min()] = dlon.min()

    return np.round(((lon - dlon[0])/(dlon.max()-dlon.min())*(dlon.size - 1)), 0).astype(int)


class globe:
    @staticmethod
    def get_ddm(lat,lon):
        """

        Return boolean array of whether the coordinates are in the ocean

        Parameters
        ----------
        lat : ndarray or float

            latitude in degrees

        lon : ndarray or float

            longitude in degrees

        Returns
        -------
        is_ocean_mask : ndarray or float

            boolean array denoting whether the corresponding point is in the ocean.
        """
        lat_i = lat_to_index(lat)
        lon_i = lon_to_index(lon)

        return ddm[lat_i, lon_i]
    
    def is_land(lat, lon):
        return globe.get_ddm(lat, lon)>0
    
    def is_ocean(lat, lon):
        return globe.get_ddm(lat, lon)<0
    
    def off_coastline(lat, lon, distance):
        """
        Return whether the distance from the coastline exceeds the distance

        Parameters
        ----------
        distance : ndarray or float
            distance away from the coastline in km
        """
        return abs(globe.get_ddm(lat, lon)) > distance
    
    def on_coastline(lat, lon, distance):
        return abs(globe.get_ddm(lat, lon)) <= distance
    
