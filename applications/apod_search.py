import requests
import json


def get_data(api_key):
    raw_response = requests.get(
        f"https://epic.gsfc.nasa.gov/api/enhanced/").text
    response = json.loads(raw_response)
    return response


def get_date(response):
    date = response['2015-10-31']
    return date
