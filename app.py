from flask import Flask, render_template, flash, redirect, request, session
import gunicorn
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests

# test

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://fqynupfmgfwmad:11761e23bb9545022e3b1d45555fc6155ff7e31c7e42fa6b2dd1a99623b60447@ec2-18-214-134-226.compute-1.amazonaws.com:5432/d191cjrfl7dcnm'


@app.route("/")
def index():
    return render_template("index.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


if __name__ == '__main__':
    app.app(debug=True)

# @app.route("/about/")
# def about():
#     return render_template("about.html")


# @app.route("/contact/")
# def contact():
#     return render_template("contact.html")


# @app.route("/api/data")
# def get_data():
#     return app.send_static_file("data.json")
