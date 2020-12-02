import os, script
import api_keys
import urllib.parse, urllib.request, urllib.error, json
import datetime

from flask import Flask, render_template, request

# absolute path to my project directory, you can comment this out
# os.chdir("E:/UW/Autumn Quarter 2020/HCDE 310/Project/city-web-app")

app = Flask(__name__)


@app.route("/")
@app.route("/home")
@app.route("/", methods=['POST', 'GET'])
def home():
    return render_template("home.html")

def get_name():
    return request.args.get('cityName')


@app.route("/location")
def location():
    return render_template("location.html")


@app.route("/weather")
def weather():
    # http://api.openweathermap.org/data/2.5/weather?q=London&appid=894aa641d6c1ca4942deb53c258952a4
    baseurl2 = 'https://api.openweathermap.org/data/2.5/weather?'
    string2 = {'q': get_name(), 'appid': api_keys.openweather_key}
    paramstr2 = urllib.parse.urlencode(string2)
    request2 = baseurl2 + paramstr2
    print('THis is the city name : ' + get_name())
    print(request2)
    reader2 = urllib.request.urlopen(request2)
    readerstr2 = reader2.read()
    data2 = json.loads(readerstr2)
    lat_city = data2.get('coord').get('lat')
    lon_city = data2.get('coord').get('lon')

    baseurl = 'https://api.openweathermap.org/data/2.5/onecall?'
    string = {'lat': str(lat_city), 'lon': str(lon_city), 'appid': api_keys.openweather_key, 'units': "imperial"}
    paramstr = urllib.parse.urlencode(string)
    rq = baseurl + paramstr
    reader = urllib.request.urlopen(rq)
    readerstr = reader.read()
    data = json.loads(readerstr)
    temp = data.get('current').get('temp')
    sr = unix_to_utc(data.get('current').get('sunrise'))
    ss = unix_to_utc(data.get('current').get('sunset'))
    return render_template("weather.html", data=data, temp_data=temp, rise_time=sr, set_time=ss)


def unix_to_utc(time_param):
    real_time = datetime.datetime.fromtimestamp(time_param).strftime('%m-%d-%Y %H:%M:%S')
    return real_time


@app.route("/walkscore")
def walkscore():
    return render_template("walkscore.html")


@app.route("/demographics")
def demographics():
    return render_template("demographics.html")


if __name__ == "__main__":
    app.run()
