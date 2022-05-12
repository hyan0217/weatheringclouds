import requests
import json

from applications import geolocation

response = geolocation.get_data()


def get_location(api_key):
    lat = geolocation.get_lat(response)
    lon = geolocation.get_lon(response)
    raw_response = requests.get(
        f'http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&limit=5&appid={api_key}').text
    location_area = json.loads(raw_response)
    return location_area


get_location()
