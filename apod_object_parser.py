
import requests
import json
import os
from PIL import Image


def get_data(api_key):
    raw_response = requests.get(
        f'https://api.nasa.gov/planetary/apod?api_key={api_key}').text
    response = json.loads(raw_response)
    return response


def get_date(response):
    date = response['date']
    return date


def get_explaination(response):
    explaination = response['explanation']
    return explaination


def get_hdurl(response):
    hdurl = response['hdurl']
    return hdurl


def get_media_type(response):
    media_type = response['media_type']
    return media_type


def get_service_version(response):
    service_version = response['service_version']
    return service_version


def get_title(response):
    service_version = response['title']
    return service_version


def get_url(response):
    url = response['url']
    return url
