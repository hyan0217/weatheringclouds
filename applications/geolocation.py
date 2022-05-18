import requests
import json

# Uses Ipapi to grab users current location with latitude and longitude


def get_data():
    raw_response = requests.get(f'https://ipapi.co/json/').text
    response = json.loads(raw_response)
    return response


def get_lat(response):
    try:
        lat = response['latitude']
    except KeyError:
        lat
    return lat


def get_lon(response):
    try:
        lon = response['longitude']
    except KeyError:
        lon
    return lon

    # try:
    #     lat = response['latitude']
    # except KeyError:
    #     lat
    # return lat
