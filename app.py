import http.client
import requests
from flask import Flask, render_template, flash, redirect, request, session
import gunicorn
from datetime import datetime
from helpers import apology
import http.client

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    req = requests.get("https://findrealestate.herokuapp.com/")
    print(req.content)
    # return render_template("index.html")


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

conn = http.client.HTTPSConnection("zillow-com1.p.rapidapi.com")

headers = {
    'X-RapidAPI-Host': "zillow-com1.p.rapidapi.com",
    'X-RapidAPI-Key': "5d5d38275amsh8a0dad41cfbbabcp1d9de2jsn5bb539b8005f"
}

conn.request(
    "GET", "/propertyExtendedSearch?location=santa%20monica%2C%20ca&home_type=Houses", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
