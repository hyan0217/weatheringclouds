import os
from flask import Flask, render_template, flash, redirect, request, url_for
import gunicorn
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, current_user,  logout_user, login_required
from flask_migrate import Migrate
import secrets
from datetime import date
from PIL import Image
from applications.config import Config
import applications.apod
import applications.weather
import applications.geolocation

# Nasa's API key
nasa_image = applications.apod.get_data("DEMO_KEY")
# OpenWeatherMap's API key
weather_current_data = applications.weather.get_current_weather(
    os.environ.get("API_KEY"))

weather_daily_data = applications.weather.get_daily_weather(
    os.environ.get("API_KEY"))

cur_location = applications.weather.get_location(
    os.environ.get("API_KEY"))


app = Flask(__name__)
# Connecting to the Database
# app.config.from_object(Config)
# Secret Key for Postgresql stored local environment
SECRET_KEY = os.environ.get("SECRET_KEY")
# Connecting to the Database stored local environment
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")
# Ensure templates are auto-reloaded
app.config['TEMPLATES_AUTO_RELOAD'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# Generates hashed passwords
bcrypt = Bcrypt(app)
# Remembers the users login credentials
login_manager = LoginManager(app)
# Requires user to login to access info
login_manager.login_view = "login"
# Flashier blue alert message
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Makes sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("OpenWeatherMap Api Key not set")


class User(db.Model, UserMixin):
    # Creates users inside the database
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default="default.jpg")
    password = db.Column(db.String(60), nullable=False)

    # Creating a string
    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.username}', '{self.email}', '{self.image_file}')"


class RegistrationForm(FlaskForm):
    # Creates the required fields for creating a user
    first_name = StringField("First Name", validators=[
        DataRequired(), Length(min=2, max=30)])
    last_name = StringField("Last Name", validators=[
        DataRequired(), Length(min=2, max=30)])
    username = StringField("Username", validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[
        DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up Now")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "Username is already taken. Please choose a different username.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                "Email is already taken. Please choose a different email.")


class LoginForm(FlaskForm):
    # Creates the required fields for logging in user
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class UpdateAccountForm(FlaskForm):
    # Allows user to update account information
    first_name = StringField("First Name", validators=[
        DataRequired(), Length(min=2, max=30)])
    last_name = StringField("Last Name", validators=[
        DataRequired(), Length(min=2, max=30)])
    username = StringField("Username", validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    picture = FileField("Update Profile Picture", validators=[
                        FileAllowed(["jpg", "png"])])
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    "Username is already taken. Please choose a different username.")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    "Email is already taken. Please choose a different email.")


class RequestResetForm(FlaskForm):
    # Validates to see if account exists first
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(
                "There is no account with that email. You must register first.")


class ResetPasswordForm(FlaskForm):
    # Allows users to change passwords
    password = PasswordField("New Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm New Password", validators=[
        DataRequired(), EqualTo("password")])
    submit = SubmitField("Reset Password")


@app.route("/", methods=["GET", "POST"])
# Homepage
def index():
    today = date.today()
    return render_template("index.html", today=today)


@app.route("/apod", methods=["GET", "POST"])
# Gets Nasa's Image of the day - APOD
@login_required
def apod():
    dates = applications.apod.get_date(nasa_image)
    explanation = applications.apod.get_explanation(nasa_image)
    hdurl = applications.apod.get_hdurl(nasa_image)
    title = applications.apod.get_title(nasa_image)

    return render_template("apod.html", dates=dates, explanation=explanation, hdurl=hdurl, title=title)


@app.route("/weather", methods=["GET", "POST"])
# Gets weather from OpenWeatherApp's API for 7 day forecast
@login_required
def weather():
    if request.method == "POST":
        # Pulls the current temperature of users location
        temp = applications.weather.get_temp(weather_current_data)
        feels = applications.weather.get_feel(weather_current_data)
        humid = applications.weather.get_humid(weather_current_data)
        uvi = applications.weather.get_uvi(weather_current_data)
        clouds = applications.weather.get_clouds(weather_current_data)
        speed = applications.weather.get_speed(weather_current_data)
        city = applications.weather.get_city(cur_location)
        country = applications.weather.get_country(cur_location)
        desc = applications.weather.get_desc(weather_current_data)
        icon = applications.weather.get_icon(weather_current_data)
        # Pulls day one of temperature of users location
        first_day = applications.weather.day_one(weather_daily_data)
        first_day_temp = applications.weather.today_day_temp(
            weather_daily_data)
        first_night_temp = applications.weather.today_night_temp(
            weather_daily_data)
        first_day_icon = applications.weather.today_icon(weather_daily_data)
        first_day_desc = applications.weather.today_desc(weather_daily_data)
        first_day_humidity = applications.weather.today_humidity(
            weather_daily_data)
        # Pulls day two of temperature of users location
        second_day = applications.weather.day_two(weather_daily_data)
        second_day_icon = applications.weather.day_two_icon(weather_daily_data)
        second_day_desc = applications.weather.day_two_desc(weather_daily_data)
        second_max_temp = applications.weather.day_two_max_temp(
            weather_daily_data)
        second_min_temp = applications.weather.day_two_min_temp(
            weather_daily_data)
        second_day_humidity = applications.weather.day_two_humidity(
            weather_daily_data)
        # Pulls day three of temperature of users location
        third_day = applications.weather.day_three(weather_daily_data)
        third_day_icon = applications.weather.day_three_icon(
            weather_daily_data)
        third_day_desc = applications.weather.day_three_desc(
            weather_daily_data)
        third_max_temp = applications.weather.day_three_max_temp(
            weather_daily_data)
        third_min_temp = applications.weather.day_three_min_temp(
            weather_daily_data)
        third_day_humidity = applications.weather.day_three_humidity(
            weather_daily_data)
        # Pulls day four of temperature of users location
        fourth_day = applications.weather.day_four(weather_daily_data)
        fourth_day_icon = applications.weather.day_four_icon(
            weather_daily_data)
        fourth_day_desc = applications.weather.day_four_desc(
            weather_daily_data)
        fourth_max_temp = applications.weather.day_four_max_temp(
            weather_daily_data)
        fourth_min_temp = applications.weather.day_four_min_temp(
            weather_daily_data)
        fourth_day_humidity = applications.weather.day_four_humidity(
            weather_daily_data)
        # Pulls day five of temperature of users location
        fifth_day = applications.weather.day_five(weather_daily_data)
        fifth_day_icon = applications.weather.day_five_icon(
            weather_daily_data)
        fifth_day_desc = applications.weather.day_five_desc(
            weather_daily_data)
        fifth_max_temp = applications.weather.day_five_max_temp(
            weather_daily_data)
        fifth_min_temp = applications.weather.day_five_min_temp(
            weather_daily_data)
        fifth_day_humidity = applications.weather.day_five_humidity(
            weather_daily_data)
        # Pulls day six of temperature of users location
        sixth_day = applications.weather.day_six(weather_daily_data)
        sixth_day_icon = applications.weather.day_six_icon(
            weather_daily_data)
        sixth_day_desc = applications.weather.day_six_desc(
            weather_daily_data)
        sixth_max_temp = applications.weather.day_six_max_temp(
            weather_daily_data)
        sixth_min_temp = applications.weather.day_six_min_temp(
            weather_daily_data)
        sixth_day_humidity = applications.weather.day_six_humidity(
            weather_daily_data)
        # Pulls day seven of temperature of users location
        seventh_day = applications.weather.day_seven(weather_daily_data)
        seventh_day_icon = applications.weather.day_seven_icon(
            weather_daily_data)
        seventh_day_desc = applications.weather.day_seven_desc(
            weather_daily_data)
        seventh_max_temp = applications.weather.day_seven_max_temp(
            weather_daily_data)
        seventh_min_temp = applications.weather.day_seven_min_temp(
            weather_daily_data)
        seventh_day_humidity = applications.weather.day_seven_humidity(
            weather_daily_data)

        return render_template("weather.html", temp=temp, feels=feels, humid=humid, uvi=uvi, clouds=clouds, speed=speed, city=city, country=country,
                               desc=desc, icon=icon, first_day=first_day, first_day_temp=first_day_temp, first_night_temp=first_night_temp,
                               first_day_humidity=first_day_humidity, first_day_desc=first_day_desc, first_day_icon=first_day_icon,
                               second_day=second_day, second_day_desc=second_day_desc, second_day_icon=second_day_icon,
                               second_max_temp=second_max_temp, second_day_humidity=second_day_humidity, third_day_icon=third_day_icon,
                               third_day_desc=third_day_desc, second_min_temp=second_min_temp, third_day=third_day,
                               third_max_temp=third_max_temp, third_min_temp=third_min_temp, third_day_humidity=third_day_humidity,
                               fourth_day=fourth_day, fourth_day_icon=fourth_day_icon, fourth_day_desc=fourth_day_desc, fourth_max_temp=fourth_max_temp,
                               fourth_min_temp=fourth_min_temp, fourth_day_humidity=fourth_day_humidity, fifth_day=fifth_day, fifth_day_icon=fifth_day_icon,
                               fifth_day_desc=fifth_day_desc, fifth_max_temp=fifth_max_temp, fifth_min_temp=fifth_min_temp, fifth_day_humidity=fifth_day_humidity,
                               sixth_day=sixth_day, sixth_day_icon=sixth_day_icon, sixth_day_desc=sixth_day_desc, sixth_max_temp=sixth_max_temp, sixth_min_temp=sixth_min_temp,
                               sixth_day_humidity=sixth_day_humidity, seventh_day=seventh_day, seventh_day_icon=seventh_day_icon,
                               seventh_day_desc=seventh_day_desc, seventh_max_temp=seventh_max_temp, seventh_min_temp=seventh_min_temp, seventh_day_humidity=seventh_day_humidity)
    return render_template("weather.html")


@app.route("/register", methods=["GET", "POST"])
# User creates an account to gain access
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
        flash("Your account has been created! You are now able to log in.", "success")
        return redirect("/login")
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
# Logs users in and remembers users login info
def login():
    if current_user.is_authenticated:
        return redirect("/")
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect("/")
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")
    return render_template("login.html", title="Login", form=form)


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
        app.root_path, "static/profile_pics", picture_fn)
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
        flash("Your account has been updated!", "success")
        return redirect("/account")
    elif request.method == "GET":
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for(
        "static", filename="profile_pics/" + current_user.image_file)
    return render_template("account.html", title="Account", image_file=image_file, form=form)


@app.route("/reset_request", methods=["GET", "POST"])
# Allows user to reset their passwords
def reset_request():
    form = ResetPasswordForm()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(
                form.password.data).decode("utf-8")
            form.password.data = hashed_password
            current_user.password = form.password.data
            db.session.commit()
            flash(
                "You password has been updated!", "success")
            return redirect("/reset_request")
        return render_template("reset_request.html", title="Reset Password", form=form)


@app.route("/about")
# The about page
@login_required
def about():
    return render_template("about.html")


@app.route("/articles")
# Articles page
@login_required
def articles():
    return render_template("articles.html")


@app.route("/angelnumber33")
@login_required
def angelnumber33():
    return render_template("angelnumber33.html")


@app.route("/firespiritual")
@login_required
def firespiritual():
    return render_template("firespiritual.html")


@app.route("/lovesigns")
@login_required
def lovesigns():
    return render_template("lovesigns.html")


@app.route("/lifepath7")
@login_required
def lifepath7():
    return render_template("lifepath7.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.app(debug=True)
