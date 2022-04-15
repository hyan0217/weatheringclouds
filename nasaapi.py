import webbrowser
import requests
import json

# API KEY

API_KEY = 'bfq9crxRTUSWOm6ydUjze2m3l98ETJwtknrS8XN2'

# API URL
url = 'https://api.nasa.gov/planetary/apod'

# Parameteres

params = {
    'date': '2015-04-12',
    'hd': 'True',
    'api_key': API_KEY
}

response = requests.get(url, params=params)
json_data = json.loads(response.text)
image_url = json_data['hdurl']
webbrowser.open(image_url)
