import requests
import os
import json
from datetime import datetime
import applications.geolocation

response = applications.geolocation.get_data()


def get_location(api_key):
    lat = applications.geolocation.get_lat(response)
    lon = applications.geolocation.get_lon(response)
    raw_response = requests.get(
        f'http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&limit=5&appid={api_key}').text
    location_area = json.loads(raw_response)
    return location_area


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

# Current Weather Forecast


def get_location(location_area):
    cur_location = location_area['name']
    return cur_location


def get_temp(weather_current_data):
    temperature = round(weather_current_data['current']['temp'])
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


def get_desc(weather_current_data):
    description = weather_current_data['current']['weather'][0]['description']
    return description


def get_icon(weather_current_data):
    icon = weather_current_data['current']['weather'][0]['icon']
    return icon

# Daily Weather Forecasts Below


def day_one(weather_daily_data):
    timestamp = weather_daily_data['daily'][0]['dt']
    date_time = datetime.fromtimestamp(timestamp)
    first_day = date_time.strftime(
        '%A' + ' ' + '%b %d')
    return first_day


def today_day_temp(weather_daily_data):
    first_day_temp = round(
        weather_daily_data['daily'][0]['temp']['day'])
    return first_day_temp


def today_night_temp(weather_daily_data):
    first_night_temp = round(
        weather_daily_data['daily'][0]['temp']['night'])
    return first_night_temp


def today_icon(weather_daily_data):
    first_day_icon = weather_daily_data['daily'][0]['weather'][0]['icon']
    return first_day_icon


def today_desc(weather_daily_data):
    first_day_desc = weather_daily_data['daily'][0]['weather'][0]['description']
    return first_day_desc


def today_humidity(weather_daily_data):
    first_day_humidity = weather_daily_data['daily'][0]['humidity']
    return first_day_humidity


def day_two(weather_daily_data):
    timestamp = weather_daily_data['daily'][1]['dt']
    date_time = datetime.fromtimestamp(timestamp)
    second_day = date_time.strftime(
        '%A' + ' ' + '%b %d')
    return second_day


def day_two_icon(weather_daily_data):
    second_day_icon = weather_daily_data['daily'][1]['weather'][0]['icon']
    return second_day_icon


def day_two_desc(weather_daily_data):
    second_day_desc = weather_daily_data['daily'][1]['weather'][0]['description']
    return second_day_desc


def day_two_max_temp(weather_daily_data):
    second_max_temp = round(weather_daily_data['daily'][1]['temp']['max'])
    return second_max_temp


def day_two_min_temp(weather_daily_data):
    second_min_temp = round(weather_daily_data['daily'][1]['temp']['min'])
    return second_min_temp


def day_two_humidity(weather_daily_data):
    second_day_humidity = weather_daily_data['daily'][1]['humidity']
    return second_day_humidity


def day_three(weather_daily_data):
    timestamp = weather_daily_data['daily'][2]['dt']
    date_time = datetime.fromtimestamp(timestamp)
    third_day = date_time.strftime(
        '%A' + ' ' + '%b %d')
    return third_day


def day_three_icon(weather_daily_data):
    third_day_icon = weather_daily_data['daily'][2]['weather'][0]['icon']
    return third_day_icon


def day_three_desc(weather_daily_data):
    third_day_desc = weather_daily_data['daily'][2]['weather'][0]['description']
    return third_day_desc


def day_three_max_temp(weather_daily_data):
    third_max_temp = round(weather_daily_data['daily'][2]['temp']['max'])
    return third_max_temp


def day_three_min_temp(weather_daily_data):
    third_min_temp = round(weather_daily_data['daily'][2]['temp']['min'])
    return third_min_temp


def day_three_humidity(weather_daily_data):
    third_day_humidity = weather_daily_data['daily'][2]['humidity']
    return third_day_humidity


def day_four(weather_daily_data):
    timestamp = weather_daily_data['daily'][3]['dt']
    date_time = datetime.fromtimestamp(timestamp)
    fourth_day = date_time.strftime(
        '%A' + ' ' + '%b %d')
    return fourth_day


def day_four_icon(weather_daily_data):
    fourth_day_icon = weather_daily_data['daily'][3]['weather'][0]['icon']
    return fourth_day_icon


def day_four_desc(weather_daily_data):
    fourth_day_desc = weather_daily_data['daily'][3]['weather'][0]['description']
    return fourth_day_desc


def day_four_max_temp(weather_daily_data):
    fourth_max_temp = round(weather_daily_data['daily'][3]['temp']['max'])
    return fourth_max_temp


def day_four_min_temp(weather_daily_data):
    fourth_min_temp = round(weather_daily_data['daily'][3]['temp']['min'])
    return fourth_min_temp


def day_four_humidity(weather_daily_data):
    fourth_day_humidity = weather_daily_data['daily'][3]['humidity']
    return fourth_day_humidity


def day_five(weather_daily_data):
    timestamp = weather_daily_data['daily'][4]['dt']
    date_time = datetime.fromtimestamp(timestamp)
    fifth_day = date_time.strftime(
        '%A' + ' ' + '%b %d')
    return fifth_day


def day_five_icon(weather_daily_data):
    fifth_day_icon = weather_daily_data['daily'][4]['weather'][0]['icon']
    return fifth_day_icon


def day_five_desc(weather_daily_data):
    fifth_day_desc = weather_daily_data['daily'][4]['weather'][0]['description']
    return fifth_day_desc


def day_five_max_temp(weather_daily_data):
    fifth_max_temp = round(weather_daily_data['daily'][4]['temp']['max'])
    return fifth_max_temp


def day_five_min_temp(weather_daily_data):
    fifth_min_temp = round(weather_daily_data['daily'][4]['temp']['min'])
    return fifth_min_temp


def day_five_humidity(weather_daily_data):
    fifth_day_humidity = weather_daily_data['daily'][4]['humidity']
    return fifth_day_humidity
