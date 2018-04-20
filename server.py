from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from helper import MorningCommute, EveningCommute

app = Flask(__name__)
app.secret_key = "ABC"


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route('/get-weather')
def get_weather():

    morning_hour = int(request.args.get("morning"))
    evening_hour = int(request.args.get("evening"))
    latitude = float(request.args.get("lat"))
    longitude = float(request.args.get("lon"))

    morning = MorningCommute(morning_hour, latitude, longitude)
    evening = EveningCommute(evening_hour, latitude, longitude)

    morning_rec = morning.recommendation()
    evening_rec = evening.recommendation()
    print evening_rec

    return render_template("recommend.html", morning=morning_rec, evening=evening_rec)



if __name__ == "__main__":
  app.debug = True

  # connect_to_db(app)

  DebugToolbarExtension(app)

  app.run(host="0.0.0.0")
