# WEATHERING CLOUDS
####  Youtube video instructions
#### Description: 

<p>I started this project with Flask in mind due to CS50s Flask project. I wanted to build my own Flask app from scratch. My idea was to implement a minimum of two different API calls along with a section of manifestation articles as an added bonus.</p>

<p>I followed the same concept from week 9s Flask app in order to build out the same framework with a few upgrades on my side.</p>

<p><b>Besides the default flask libary, I am also using the following imports below:</b><p>

<h4>-Gunicorn in order for my Python Flask application to function on Heroku servers.</h4>
-Flask_wtf for providing a user interface for users.
-WTForms to render text fields, field requirements and buttons.
-SQLAlchemy to communicate and store with my database.
-Bcrypt for a stronger password encryption.
-Flask_Login in order to provide a log-in, log-out, and storing active user's ID in session for users while logged in.
-Flask_Migrate in order for Flask and SQLAlchemy to work together properly.
-Secret in order to generate a secret key to protect against cookie data tampering.
-Python PIL to open and manipulate images for users profile avatar.
-Requests 


<p>My first idea was to implement NASAs API to extract the <b>Image of the Day</b> from NASAs database based on the current day by using the requests and json libaries. I started by using the google extension JSON Formatter on the browser to get the parameters from NASAs API call address before deciding which parameters I would like to extract into my own web application.</p>

<p>Next up, Before I started working on my next API project. I needed a way to locate the current users location for which I can then populate the current weather along with the next few days of forecast with only just a simple click of a button!</p>

I did some searching on the web and discovered a free to use location tracker without having to sign up for an API called IPAPI. With IPAPI... I was able to extract the users current latitude and longitude by using the imports libraries JSON and Requests. 

I was able to pass in the data into OpenWeatherMaps One Call Dark Sky API in order to return data of the current temperature, UV, humidity, wind speed, feels like, and cloud movements. I decided to go further by implementing the weather for the next 6 days including the current day as well.

For the last project, I've had previous manifestation articles that I hired someone to write for me for my old website that I used to run as an added bonus. This one was simple as it just required additional html pages for storing the articles(4 in total).