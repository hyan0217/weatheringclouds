import webbrowser
import requests
import json
from datetime import datetime

# Contact API
API_KEY = 'bfq9crxRTUSWOm6ydUjze2m3l98ETJwtknrS8XN2'
url = "https://api.nasa.gov/planetary/apod"


params = {
    'api_key': API_KEY,
    'hd': 'True',
    'date': datetime.today().strftime('%Y-%m-%d')
}

# params = {
#     'api_key': API_KEY,
#     'start_date': '2020-01-22',
#     'end_date': '2020-01-23'
# }

response = requests.get(url, params=params)
json_data = json.loads(response.text)
print(json_data)
