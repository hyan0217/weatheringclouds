# WEATHERING CLOUDS

####  Youtube video instructions
TODO

#### Live Server Webpage Link
https://weatheringclouds.herokuapp.com/

## Description: 

I started this project with Flask in mind due to <b>CS50s Flask project</b>. I wanted to build my own Flask app from scratch. My idea was to implement a minimum of two different API calls along with a section of manifestation articles as an added bonus.

I followed the same concept from week 9s Flask app as a starting template in order to build out my flask framework, starting with setting up the virtual enviroment server(.venv) and sqlite for storing the database locally following up with the templates folder for the html files, static folder for the images and css, applications folder for the APOD, geolocation and weather API calls and lastly the app.py file.

I decided to split my navigational and footer bars in order to make my layout html cleaner with the use of <b>Jinja</b>. The main via Index page also contains all the projects and API websites that made this project possible.

I then created the User class with the basic information a user would usually have in order to register for an account like ex: <b>id, first name, last name, username, email, password, and avatar image</b>(which converts an image to a maximizing size of 125x125) and storing them into a database unique to that specific user.

Next, I created a registration form with a class for users to create accounts with the use of <b>FlaskForm</b> inside the register page before passing data into the database. I've also created a login with the <b>remember me</b> checkmark and logout routes for users. Additionally, the account form page allows users to update their account information including the image avatar and reseting passwords as well.

After setting up my page. My idea was to implement <b>NASAs API</b> to extract the <b>Image of the Day</b> API parameter from NASAs database based on the current day with the help of <b>Requests</b> and <b>JSON</b> libaries. In order to get started, I first used the google extension <b>JSON Formatter</b> in the browser to pass in the parameters from NASAs API call site to grab the data ex: date, description, image, and title of the image.

Before diving into the next project. I needed a way to locate the current users location for which I can obtain the current weather along with the next few days of forecast with just a simple click of a <b>button</b>!

I did some searching on the web and discovered a free to use location tracker without an API key named <b>IPAPI</b>. With IPAPI... I was able to extract the current users <b>Latitude</b> and <b>Longitude</b> parameters with JSON and Requests as well.

I then passed the data parameters into <b>OpenWeatherMaps One Call Dark Sky API</b> in order to return data of the current temperature, UV, humidity, wind speed, feels like, and cloud movements. I decided to go further by implementing the weather for the next 6 days including the current day as well.

For my last project, I've had previous manifestation articles that I've owned. This one was simple as it only required additional html pages for storing the articles(4 in total).

After finishing everything locally on my computer, I created a <b>Procfile</b> that specifies certain commands that are executed by the app on startup for <b>Heroku</b> along with the <b>requirements.txt</b> file to let Heroku know what import libaries are being used. I then installed <b>Postgres</b> on my Heroku server in order to have an online database which will allow everyone to have access to when they create their own accounts. 

Next, I created a proxy server to make an request to my website which will then make a request to the original source: the API site. <b>Original source code is provided by https://github.com/MauricioRobayo/api-key-proxy-server</b> The proxy server is powered by Express.

The last part of this project was to upload my flask application onto Heroku server itself. Heroku is a free web hosting service for students which I <b>highly recommend!</b>

## Libraries Used In This Project

#### -Flask Library which is main framework responsible for this web application.
#### -Gunicorn in order for Python Flask application to function on Heroku servers.
#### -Flask_wtf for providing a user interface.
#### -WTForms to render text fields, field requirements and buttons.
#### -SQLAlchemy to communicate and store databases.
#### -Bcrypt for a stronger password encryption.
#### -Flask_Login provides a log-in, log-out, while storing active user's ID in session while logged in.
#### -Flask_Migrate provides proper functioning between Flask and SQLAlchemy.
#### -Secret provides a secret key to protect against cookie data tampering.
#### -Python PIL helps open and manipulate images for users profile avatar.
#### -Requests allows the sending of HTTP requests and returns a response data with Python.
#### -JSON encodes data into JSON format and deserializes back into readable code.
#### -API-Key-Proxy-Server makes a request from your own webpage to the API call site and returns the parameters requested.
