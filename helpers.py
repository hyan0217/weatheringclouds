import requests
import os
import json
from datetime import datetime

# Contact API
API_KEY = 'bfq9crxRTUSWOm6ydUjze2m3l98ETJwtknrS8XN2'
url = "https://api.nasa.gov/planetary/apod"


def image_of_day():

    params = {
        'api_key': API_KEY,
        'hd': 'True',
        'date': datetime.today().strftime('%Y-%m-%d')
    }

    response = requests.get(url, params=params)
    json_data = json.loads(response.text)
    image_url = json_data['url']
    return(image_url)
