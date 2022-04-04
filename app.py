from flask import Flask, render_template, flash, redirect, request, session
import gunicorn
from datetime import datetime
from helpers import apology
import requests
import http.client

app = Flask(__name__)


@app.route("/")
def index():
    conn = http.client.HTTPSConnection("real-estate-usa.p.rapidapi.com")

    headers = {
        'X-RapidAPI-Host': "real-estate-usa.p.rapidapi.com",
        'X-RapidAPI-Key': "5d5d38275amsh8a0dad41cfbbabcp1d9de2jsn5bb539b8005f"
    }

    conn.request(
        "GET", "/api/v1/properties?postal_code=94105&offset=0&limit=200", headers=headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))
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
