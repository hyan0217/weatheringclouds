from flask import render_template
from datetime import datetime
import requests
import json


def get_data(api_key):
    raw_response = requests.get(
        f'https://api.nasa.gov/planetary/apod?api_key={api_key}').text
    response = json.loads(raw_response)
    return response


def get_date(response):
    date = response['date(%Y-%m-%d)']
    return date


def get_explanation(response):
    explanation = response['explanation']
    return explanation


def get_hdurl(response):
    hdurl = response['hdurl']
    return hdurl


def get_title(response):
    title = response['title']
    return title
