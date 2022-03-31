import os
from flask import Flask, render_template, flash, redirect, request, session
import gunicorn
from datetime import datetime
from helpers import apology

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()

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


@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")
