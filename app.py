import os
from flask import Flask, render_template, flash, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
import gunicorn
from datetime import datetime
from helpers import apology

app = Flask(__name__)
db = SQLAlchemy(app)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.text, nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.app()

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
