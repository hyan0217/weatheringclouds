import requests
import os
import geolocation

response = geolocation.get_data()


def get_weather():
    api_key = os.environ.get('API_KEY')
    lat = geolocation.get_lat(response)
    lon = geolocation.get_lon(response)
    url = requests.get(
        f'https://api.openweathermap.org/data/2.5/onecall?appid={api_key}&units=imperial&lat={lat}&lon={lon}')

    weather_data = url.json()
    icon = weather_data['current']['weather'][0]['icon']
    timezone = weather_data['timezone']
    description = weather_data['current']['weather'][0]['description']
    temperature = round(weather_data['current']['temp'])
    humidity = weather_data['current']['humidity']
    feels = round(weather_data['current']['feels_like'])
    clouds = weather_data['current']['clouds']
    uvi = weather_data['current']['uvi']
    speed = weather_data['current']['wind_speed']
