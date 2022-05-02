import requests
import os
import json
import applications.geolocation

response = applications.geolocation.get_data()


def get_current_weather(api_key):
    lat = applications.geolocation.get_lat(response)
    lon = applications.geolocation.get_lon(response)
    raw_response = requests.get(
        f'https://api.openweathermap.org/data/2.5/onecall?appid={api_key}&units=imperial&lat={lat}&lon={lon}').text
    weather_current_data = json.loads(raw_response)
    return weather_current_data


def get_daily_weather(api_key):
    lat = applications.geolocation.get_lat(response)
    lon = applications.geolocation.get_lon(response)
    raw_response = requests.get(
        f'https://api.openweathermap.org/data/2.5/onecall?appid={api_key}&exclude=current,minutely,hourly,alerts&units=imperial&lat={lat}&lon={lon}').text
    weather_daily_data = json.loads(raw_response)
    return weather_daily_data


def get_temp(weather_current_data):
    temperature = weather_current_data['current']['temp']
    return temperature


def get_feel(weather_current_data):
    feels = round(weather_current_data['current']['feels_like'])
    return feels


def get_humid(weather_current_data):
    humidity = weather_current_data['current']['humidity']
    return humidity


def get_uvi(weather_current_data):
    uvi = weather_current_data['current']['uvi']
    return uvi


def get_clouds(weather_current_data):
    clouds = weather_current_data['current']['clouds']
    return clouds


def get_speed(weather_current_data):
    speed = weather_current_data['current']['wind_speed']
    return speed


def get_time(weather_current_data):
    timezone = weather_current_data['timezone']
    return timezone


def get_desc(weather_current_data):
    description = weather_current_data['current']['weather'][0]['description']
    return description


def get_icon(weather_current_data):
    icon = weather_current_data['current']['weather'][0]['icon']
    return icon


def get_daily_temp(weather_daily_data):
    daily_temp = weather_daily_data['daily'][1]['temp']
    return daily_temp


def get_daily_icon(weather_daily_data):
    daily_icon = weather_daily_data['weather']['icon']
    return daily_icon


def get_daily_humid(weather_daily_data):
    daily_humid = round(weather_daily_data['daily'][1]['humidity'])
    return daily_humid
