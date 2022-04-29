import configparser
import os
from flask import Flask, render_template, flash, redirect, request, session, url_for
import gunicorn
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, current_user,  logout_user, login_required
from flask_migrate import Migrate
from datetime import datetime
import secrets
from PIL import Image
import requests
import applications.apod
import applications.NeoWs.asteroids
import applications.epic
from requests import get

# Nasa's API key and url
response = applications.apod.get_data(
    'DEMO_KEY')


# def get_api_key():
#     # Openweathermap's API
#     config = configparser.ConfigParser()
#     config.read('config.ini')
#     return config['openweathermap']['weather_api']


app = Flask(__name__)
# Connecting to the Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://fqynupfmgfwmad:11761e23bb9545022e3b1d45555fc6155ff7e31c7e42fa6b2dd1a99623b60447@ec2-18-214-134-226.compute-1.amazonaws.com:5432/d191cjrfl7dcnm'
# Secret Key
app.config['SECRET_KEY'] = "2c1b9360123f14339ae48bcd70433bf3"
app.config['SECRET_KEY'] = "11761e23bb9545022e3b1d45555fc6155ff7e31c7e42fa6b2dd1a99623b60447"
# Initialize Database
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# Generates hashed passwords
bcrypt = Bcrypt(app)
# Remembers the users login credentials
login_manager = LoginManager(app)
# Requires user to login to access info
login_manager.login_view = 'login'
# Flashier blue alert message
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Make sure API key is set
if not os.environ.get("WEATHER_KEY"):
    raise RuntimeError("WEATHER_KEY not set")


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    # Creating a string
    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.username}', '{self.email}', '{self.image_file}')"


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[
        DataRequired(), Length(min=2, max=30)])
    last_name = StringField('Last Name', validators=[
        DataRequired(), Length(min=2, max=30)])
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up Now')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'Username is already taken. Please choose a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'Email is already taken. Please choose a different email.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    first_name = StringField('First Name', validators=[
        DataRequired(), Length(min=2, max=30)])
    last_name = StringField('Last Name', validators=[
        DataRequired(), Length(min=2, max=30)])
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[
                        FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    'Username is already taken. Please choose a different username.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    'Email is already taken. Please choose a different email.')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(
                'There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


@app.route("/", methods=["GET", "POST"])
def index():

    return render_template("index.html")


@app.route("/apod", methods=["GET", "POST"])
def apod():

    dates = applications.apod.get_date(response)
    explanation = applications.apod.get_explanation(response)
    hdurl = applications.apod.get_hdurl(response)
    title = applications.apod.get_title(response)

    return render_template("apod.html", dates=dates, explanation=explanation, hdurl=hdurl, title=title)


@app.route("/asteroids", methods=["GET", "POST"])
def asteroids():

    asteroids = applications.NeoWs.asteroids.Asteroids()

    return render_template("asteroids.html", asteroids=asteroids)


@app.route("/epic", methods=["GET", "POST"])
def epic():

    image = applications.epic.get_data(response)
    date = applications.epic.get_date(response)

    return render_template("epic.html", image=image, date=date)


@app.route("/weather", methods=["GET", "POST"])
def weather():

    if request.method == "POST":
        city = request.form['city']
        country = request.form['country']
        api_key = os.environ.get("WEATHER_KEY")
        url = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?appid={api_key}&units=imperial&q={city},{country}')

        weather_data = url.json()
        icon = weather_data['weather'][0]['icon']
        city = weather_data['name']
        description = weather_data['weather'][0]['description']
        temperature = round(weather_data['main']['temp'])
        humidity = weather_data['main']['humidity']
        feels = round(weather_data['main']['feels_like'])
        clouds = weather_data['clouds']['all']
        speed = weather_data['wind']['speed']

        return render_template("weather.html", city=city, description=description, icon=icon, temperature=temperature, humidity=humidity, speed=speed, feels=feels, clouds=clouds)
    return render_template("weather.html")


@app.route("/forecast_week", methods=["GET", "POST"])
def forecast_week():

    if request.method == "POST":
        api_key = os.environ.get("WEATHER_KEY")
        lat = get('https://ipapi.co/latitude/')
        lon = get('https://ipapi.co/longitude/')
        url = requests.get(
            f'https://api.openweathermap.org/data/2.5/onecall?appid={api_key}&units=imperial&lat={lat}&lon={lon}')

        weather_data = url.json()
        icon = weather_data['current']['weather'][0]['icon']
        timezone = weather_data['timezone']
        description = weather_data['current']['weather'][0]['description']
        temperature = round(weather_data['current']['temp'])
        humidity = weather_data['current']['humidity']
        feels = round(weather_data['current']['feels_like'])
        clouds = weather_data['current']['clouds']
        speed = weather_data['current']['wind_speed']

        return render_template("forecast_week.html", timezone=timezone, description=description, icon=icon, temperature=temperature, humidity=humidity, speed=speed, feels=feels, clouds=clouds)
    return render_template("forecast_week.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect("/")
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect("/login")
    return render_template("register.html", title='Register', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/")
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect("/")
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template("login.html", title='Login', form=form)


@app.route("/logout")
# Logs user out
def logout():
    logout_user()
    return redirect("/")


def save_picture(form_picture):
    # Allows user to update and saves avatar pictures
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/profile_pics', picture_fn)
    # Scales down images to prevent server overload
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=["GET", "POST"])
@login_required
# Allows user to update their account information
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect("/account")
    elif request.method == "GET":
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
    return render_template("account.html", title='Account', image_file=image_file, form=form)


@app.route("/reset_password", methods=["GET", "POST"])
@login_required
# Allows user to reset their passwords
def reset_request():
    if current_user.is_authenticated:
        return redirect("/")
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect("/login")
    return render_template("reset_request.html", title='Reset Password', form=form)


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
