from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from datetime import datetime
import time
import os
import timezonefinder
import requests
import json

# from model import connect_to_db, db


app = Flask(__name__)

app.secret_key = "ABC"


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route('/get-weather')
def get_weather():

    print request.args.get("lat")
    morning_hour = int(request.args.get("morning"))
    evening_hour = int(request.args.get("evening")) + 12
    latitude = float(request.args.get("lat"))
    longitude = float(request.args.get("lon"))
    # import pdb; pdb.set_trace()

    morning_weather = get_hour_weather(morning_hour, latitude, longitude)
    evening_weather = get_hour_weather(evening_hour, latitude, longitude)
    print "MORNING", morning_weather

    if not morning_weather or not evening_weather:
        flash("Sorry no data was found")
        redirect ("/")

    ride = {"morning": True, "evening": False}

    if morning_weather["windSpeed"] > 15:
        report["morning"] = False
    if evening_weather["windSpeed"] > 15:
        report["evening"] = False

    return render_template("recommend.html", ride=ride)


def get_hourly_weather(day, lat, lon, time):
    """ Get today's weather info from Dark Sky API """

    # check cache
    # ping API for today's weather

    key = os.environ["DARK_SKY_KEY"]

    url = "https://api.darksky.net/forecast/{key}/{lat},{lon},{time}".format(key=key,
                                                                             lat=lat,
                                                                             lon=lon,
                                                                             time=time)
    print url
    response = requests.get(url)
    data = json.loads(response.text)


    return data["hourly"]["data"]


def get_hour_weather(hour, lat, lon):
    day = time.mktime(datetime.today().timetuple())
    hour = datetime.today().replace(hour=hour, minute=0, second=0, microsecond=0)
    hour = int(time.mktime(hour.timetuple()))

    # tf = timezonefinder.TimezoneFinder()
    # tz_str = tf.certain_timezone_at(lat=lat, lng=lon)
    hourly_weather = get_hourly_weather(hour,lat, lon, hour)
    print "HOUR", hour
    for obj in hourly_weather:
        print obj["time"]
        if obj["time"] == hour:
            return obj

    return None


if __name__ == "__main__":
  app.debug = True

  # connect_to_db(app)

  DebugToolbarExtension(app)

  app.run(host="0.0.0.0")
