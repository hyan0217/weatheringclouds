import requests
import json

# Uses Nasa's API to get daily image of the day


def get_data(api_key):
    raw_response = requests.get(
        f"https://api.nasa.gov/planetary/apod?api_key={api_key}").text
    nasa_image = json.loads(raw_response)
    return nasa_image


def get_date(nasa_image):
    date = nasa_image["date"]
    return date


def get_explanation(nasa_image):
    explanation = nasa_image["explanation"]
    return explanation


def get_hdurl(nasa_image):
    hdurl = nasa_image["hdurl"]
    return hdurl


def get_title(nasa_image):
    title = nasa_image["title"]
    return title
