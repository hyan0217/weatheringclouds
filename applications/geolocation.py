import requests
import json

# Uses Ipapi to grab users current location with latitude and longitude


def get_data():
    raw_response = requests.get(f'https://ipapi.co/json/').text
    response = json.loads(raw_response)
    return response


def get_lat(response):
    lat = response['latitude']
    try:
        lat
    except KeyError:
        pass
    return lat


def get_lon(response):
    lon = response['longitude']
    try:
        lon
    except KeyError:
        pass
    return lon
