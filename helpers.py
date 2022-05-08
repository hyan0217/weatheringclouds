import requests
import json

from applications import geolocation

response = geolocation.get_data()


def get_data():
    lat = geolocation.get_lat(response)
    lon = geolocation.get_lon(response)
    raw_response = requests.get(
        f'https://api.openweathermap.org/data/2.5/onecall?appid={api_key}&exclude=current,minutely,hourly,alerts&units=imperial&lat={lat}&lon={lon}').text
    weather_current_data = json.loads(raw_response)
    return weather_current_data


def get_daily_temp(weather_current_data):
    daily_temp = response['daily']['temp']
    return daily_temp


print(get_daily_temp)
