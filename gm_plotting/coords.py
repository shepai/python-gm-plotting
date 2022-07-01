from typing import Iterable

import numpy as np

# Optional support for converting from UTM coordinates
try:
    import utm
except:
    pass


def gps_to_merc(lat, lon):
    if isinstance(lat, Iterable):
        lat = np.array(lat)
        lon = np.array(lon)

    mlat = 0.5 - np.log(np.tan(np.deg2rad(45 + lat / 2))) / (2 * np.pi)
    mlon = 0.5 + lon / 360
    return mlat, mlon

def merc_to_gps(mlat, mlon):
    if isinstance(mlat, Iterable):
        mlat = np.array(mlat)
        mlon = np.array(mlon)

    lat = np.rad2deg(2 * np.arctan(np.exp(np.pi * (1 - 2 * mlat)))) - 90
    lon = 360 * (mlon - 0.5)
    return lat, lon

def utm_to_merc(easting, northing, zone_number, zone_letter):
    return gps_to_merc(*utm.to_latlon(easting, northing, zone_number, zone_letter, strict=False))
