import requests
import os
import json
import time
from datetime import datetime

cache = {}
DARK_SKY_KEY = os.environ["DARK_SKY_KEY"]

class Commute(object):
    """ A commute hour """

    def __init__(self, hour, time, lat, lng):
        self.time = time
        self.hour = self.convert_hour(hour)
        self.lat = lat
        self.lng = lng

        self.set_weather()

    @staticmethod
    def convert_hour(hour):
        """ Convert from 24 hour to UNIX time"""

        hour = datetime.today().replace(hour=hour, minute=0, second=0, microsecond=0)
        hour = int(time.mktime(hour.timetuple()))

        return hour

    def get_hourly_weather(self):
        """ Get today's weather info from Dark Sky API """

        day = time.mktime(datetime.today().timetuple())
        base_url = "https://api.darksky.net/forecast/"
        # check cache
        if day in cache:
            print "FOUND IN CACHE"
            return cache[day]

        # ping API for today's weather
        url = "{url}{key}/{lat},{lon},{time}".format(url=base_url,
                                                          key=DARK_SKY_KEY,
                                                          lat=self.lat,
                                                          lon=self.lng,
                                                          time=self.hour)
        response = requests.get(url)
        data = json.loads(response.text)
        cache[day] = data["hourly"]["data"]

        return data["hourly"]["data"]

    def set_weather(self):
        """ Set attributes for commute time weather """

        for hour_weather in self.get_hourly_weather():
            if hour_weather["time"] == self.hour:
                self.wind = hour_weather["windSpeed"]
                self.temperature = hour_weather["temperature"]
                self.rain_probability = hour_weather["precipProbability"]
                self.rain_intensity = hour_weather["precipIntensity"]
                return
        return

    def recommendation(self):
        rec = {'recommended': True}
        if self.rain_probability > 40:
            if self.rain_intensity > 0.3:
                rec['recommended'] = False
                rec['rain'] = "Heavy rain today"
            elif self.rain_intensity > 0.1:
                rec['rain'] = "Bring a rain jacket!"
            else:
                rec['rain'] = "Drizzle likely"
        else:
            rec['rain'] = "Little to no rain expected"

        if self.wind > 13:
            rec['recommended'] = False
            rec['wind'] = "Not a good ride: too windy!"

        return rec


class MorningCommute(Commute):

    def __init__(self, hour, lat, lng):

        super(MorningCommute, self).__init__(hour, "morning", lat, lng)


class EveningCommute(Commute):

    def __init__(self, hour, lat, lng):

        super(EveningCommute, self).__init__(hour + 12, "evening", lat, lng)
