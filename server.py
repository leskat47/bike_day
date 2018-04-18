from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from helper import MorningCommute, EveningCommute
import redis

# from model import connect_to_db, db


app = Flask(__name__)
app.secret_key = "ABC"

r = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route('/get-weather')
def get_weather():

    print request.args.get("lat")
    morning_hour = int(request.args.get("morning"))
    evening_hour = int(request.args.get("evening"))
    latitude = float(request.args.get("lat"))
    longitude = float(request.args.get("lon"))

    # morning_weather = get_hour_weather(morning_hour, latitude, longitude)
    # evening_weather = get_hour_weather(evening_hour, latitude, longitude)
    #
    # if not morning_weather or not evening_weather:
    #     flash("Sorry no data was found")
    #     redirect ("/")
    #
    # ride = {"morning": True, "evening": False}
    #
    # if morning_weather["windSpeed"] > 15:
    #     report["morning"] = False
    # if evening_weather["windSpeed"] > 15:
    #     report["evening"] = False

    morning = MorningCommute(morning_hour, latitude, longitude)
    evening = EveningCommute(evening_hour, latitude, longitude)

    return render_template("recommend.html", morning=morning, evening=evening)



if __name__ == "__main__":
  app.debug = True

  # connect_to_db(app)

  DebugToolbarExtension(app)

  app.run(host="0.0.0.0")
