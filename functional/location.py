from geopy.distance import geodesic

from urllib.request import urlopen
import json


def get_ip_data():
    url = 'http://ipinfo.io/json'
    response = urlopen(url)
    return json.load(response)


def get_coordinates():
    """Returns current coordinates using IP address"""
    data = get_ip_data()
    latitude = data['loc'].split(',')[0]
    longitude = data['loc'].split(',')[1]

    return latitude, longitude, data
# print(get_ip_data())

# print(get_coordinates())


def ras(user_loc1, user_loc2, org_loc1, org_loc2):
    try:
        coords_1 = (user_loc1, user_loc2)
        coords_2 = (org_loc1, org_loc2)
        return geodesic(coords_1, coords_2).m
    except Exception:
        return False

