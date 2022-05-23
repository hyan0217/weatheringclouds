# WEATHERING CLOUDS

####  Youtube video instructions

#### Direct Webpage Link

## Description: 

I started this project with Flask in mind due to <b>CS50s Flask project</b>. I wanted to build my own Flask app from scratch. My idea was to implement a minimum of two different API calls along with a section of manifestation articles as an added bonus.

I followed the same concept from week 9s Flask app as a starting template in order to build out my flask framework, starting with setting up the virtual enviroment server(.venv) and sqlite for storing the database locally following up with the templates folder for the html files, static folder for the images and css, applications folder for the APOD, geolocation and weather API calls and lastly the app.py file.

I decided to split my navigational and footer bars in order to make my layout.html cleaner with the use of <b>Jinja</b>. I also decided to place all my projects including the API companies that made my project possible on my main page via Index.html page.

I then created the User class with the basic information a user would usually have after registering for an account like an <b>id, first name, last name, username, email, password, and a customizible avatar image</b> and storing them into a database unique to the specific user.

Next, I created a registration form and class for the user to create their accounts by requiring the StringField, PasswordField, and SubmitField from <b>FlaskForm</b> and passing them into the register.html page while adding the data into the database.

After that, I created a login with the <b>remember me</b> checkmark and logout routes for the users. I've also added additional form features like allowing the users to update their account information including the changing the image avatar and reseting passwords using FlaskForm as well.

After setting up my webpage. My first idea was to implement <b>NASAs API</b> to extract the <b>Image of the Day</b> from NASAs database based on the current day by using the <b>Requests</b> and <b>JSON</b> libaries. To get started, I used the google extension <b>JSON Formatter</b> on the browser to get the parameters from NASAs API call address before deciding which parameters I would like to extract into my own flask application. I then passed in the date, explanation, high definition image, and title of the image that is shown.

Before getting onto the next project. I needed a way to locate the current users location for which I can then obtain the current weather along with the next few days of forecast with just a simple click of a <b>button</b>!

I did some searching on the web and discovered a free to use location tracker without having to sign up for an API key called <b>IPAPI</b>. With IPAPI... I was able to extract the users current <b>Latitude</b> and <b>Longitude</b> parameters by also using the imports libraries JSON and Requests. 

I then passed the data parameters into <b>OpenWeatherMaps One Call Dark Sky API</b> in order to return data of the current temperature, UV, humidity, wind speed, feels like, and cloud movements. I decided to go further by implementing the weather for the next 6 days including the current day as well.

For my last project, I've had previous manifestation articles that I hired someone to write for me for my old website that I've never got the chance to work on. This one was simple as it only required additional html pages for storing the articles(4 in total).

After finishing everything locally, I added the <b>Procfile</b> that specifies certain commands that are executed by the app on startup for <b>Heroku</b> along with the <b>requirements.txt</b> file to let Heroku know what import libaries are being used. I then installed <b>Postgres</b> on my Heroku server in order to have an online database so everyone will have access when they create an account of their own.  

The last part of this project was to upload the flask application onto Heroku. Heroku is a free web hosting service for students which I <b>highly recommend!</b>

## Libraries Used In This Project

#### -Flask Library which is main framework responsible for this web application.
#### -Gunicorn in order for my Python Flask application to function on Heroku servers.
#### -Flask_wtf for providing a user interface for users.
#### -WTForms to render text fields, field requirements and buttons.
#### -SQLAlchemy to communicate and store with my database.
#### -Bcrypt for a stronger password encryption.
#### -Flask_Login in order to provide a log-in, log-out, and storing active user's ID in session for users while logged in.
#### -Flask_Migrate in order for Flask and SQLAlchemy to work together properly.
#### -Secret in order to generate a secret key to protect against cookie data tampering.
#### -Python PIL to open and manipulate images for users profile avatar.
#### -Requests 