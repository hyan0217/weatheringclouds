from flask import Flask, render_template
import gunicorn
from datetime import datetime
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about/")
def about():
    return render_template("about.html")


@app.route("/contact/")
def contact():
    return render_template("contact.html")


@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")
