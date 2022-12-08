from geopy.distance import geodesic


def ras(lat_2, lon_2):
    coords_1 = (42.870454, 74.602722)
    coords_2 = (lat_2, lon_2)

    return geodesic(coords_1, coords_2).m
