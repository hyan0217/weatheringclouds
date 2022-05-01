import requests
import json


def get_data():
    raw_response = requests.get(f'https://ipapi.co/json/').text
    response = json.loads(raw_response)
    return response


def get_lat(response):
    lat = response['latitude']
    return lat


def get_lon(response):
    lon = response['longitude']
    return lon
