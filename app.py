from flask import Flask, render_template, flash, redirect, request, session
import gunicorn
from datetime import datetime
from helpers import apology
import requests

app = Flask(__name__)


@app.route("/")
def index():
    url = "https://real-estate-usa.p.rapidapi.com/api/v1/properties"

    querystring = {"postal_code": "94105", "offset": "0", "limit": "200"}

    headers = {
        "X-RapidAPI-Host": "real-estate-usa.p.rapidapi.com",
        "X-RapidAPI-Key": "5d5d38275amsh8a0dad41cfbbabcp1d9de2jsn5bb539b8005f"
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)

    print(response.text)
    return render_template("index.html")


if __name__ == '__main__':
    app.app(debug=True)

# @app.route("/about/")
# def about():
#     return render_template("about.html")


# @app.route("/contact/")
# def contact():
#     return render_template("contact.html")


# @app.route("/hello/")
# @app.route("/hello/<name>")
# def hello_there(name=None):
#     return render_template(
#         "hello_there.html",
#         name=name,
#         date=datetime.now()
#     )


# @app.route("/api/data")
# def get_data():
#     return app.send_static_file("data.json")
