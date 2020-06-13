import os
import requests
import urllib.parse
import json

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup_parks(state):
    # get the NPS Key environmental variable, then try to send API request to National Park's website
    try:
        NPS_key = os.environ.get("NPS_KEY")
        request = requests.get(f"https://developer.nps.gov/api/v1/parks?stateCode={state}&limit=100&fields=images&api_key={NPS_key}",)
        request.raise_for_status()
    except requests.RequestException:
        return None

    try:
        # convert to json for processing
        park_data = request.json()
        data = park_data["data"]
        # make a list to hold a dictionary for each park
        parks = []

        for row in data:
            name = row["name"]
            park_url = row["url"]
            city = row["addresses"][0]["city"]
            latitude = row["latitude"]
            longitude = row["longitude"]
            latlong = latitude +"," + longitude

            # temporary dictionary to append to the parks list
            temp_dict = {
                    "name": name,
                    "url": park_url,
                    "city": city,
                    "latlong": latlong

            }

            parks.append(temp_dict)

        return parks
    except (KeyError, TypeError, ValueError):
        return None

def lookup_weather(lat,lon):

    try:
        # get the weather API key environmental variable, then try to make a request
        Open_weather_key = os.environ.get("Open_weather_key")
        request = requests.get(f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=imperial&appid={Open_weather_key}",)
        request.raise_for_status()
    except requests.RequestException:
        return None

    try:
        # format the data into a dictionary for display on the HTML page
        weather_data = request.json()

        # format the data into a dictionary for display on the HTML page
        data = {
        "temp": str(weather_data['main']['temp']),
        "feels_like":str(weather_data["main"]["feels_like"]),
        "description": str(weather_data['weather'][0]["description"]),
        "city": weather_data["name"],
        "icon": weather_data['weather'][0]['icon']
        }

        return data
    except (KeyError, TypeError, ValueError):
        return None
