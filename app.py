import os, script
import api_keys
import urllib.parse, urllib.request, urllib.error, json
import datetime

from flask import Flask, render_template, request, redirect, url_for, session
from forms import SearchForm

# absolute path to my project directory, you can comment this out
# os.chdir("E:/UW/Autumn Quarter 2020/HCDE 310/Project/city-web-app")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'citywebapp'


@app.route("/")
@app.route("/home")
@app.route("/", methods=['POST', 'GET'])
@app.route("/home", methods=['POST', 'GET'])
def home():
    form = SearchForm()
    if form.is_submitted():
        # this is the city name
        result = request.form.get('search')
        session['result'] = result
        # this code helps us get the coordinates of a city
        baseurl2 = 'https://api.openweathermap.org/data/2.5/weather?'
        string2 = {'q': session['result'], 'appid': api_keys.openweather_key}
        paramstr2 = urllib.parse.urlencode(string2)
        request2 = baseurl2 + paramstr2
        print("THIS IS THE LINK: " + request2)
        reader2 = urllib.request.urlopen(request2)
        readerstr2 = reader2.read()
        data2 = json.loads(readerstr2)
        lat_city = data2.get('coord').get('lat')
        lon_city = data2.get('coord').get('lon')
        session['lat'] = lat_city
        session['long'] = lon_city


    return render_template('home.html', form=form)


@app.route("/weather")
def weather():
    # this will help us get the coordinates of a city
    baseurl2 = 'https://api.openweathermap.org/data/2.5/weather?'
    string2 = {'q': session['result'], 'appid': api_keys.openweather_key}
    paramstr2 = urllib.parse.urlencode(string2)
    request2 = baseurl2 + paramstr2
    print("THIS IS THE LINK: " + request2)
    reader2 = urllib.request.urlopen(request2)
    readerstr2 = reader2.read()
    data2 = json.loads(readerstr2)
    lat_city = data2.get('coord').get('lat')
    lon_city = data2.get('coord').get('lon')
    session['lat'] = lat_city
    session['long'] = lon_city

    #this will help us get the weather information of a city
    baseurl = 'https://api.openweathermap.org/data/2.5/onecall?'
    string = {'lat': str(lat_city), 'lon': str(lon_city), 'appid': api_keys.openweather_key, 'units': "imperial"}
    paramstr = urllib.parse.urlencode(string)
    rq = baseurl + paramstr
    reader = urllib.request.urlopen(rq)
    readerstr = reader.read()
    data = json.loads(readerstr)
    temperature = data.get('current').get('temp')
    sunrise = unix_to_utc(data.get('current').get('sunrise'))
    date = sunrise[0:10]
    sunrise_time = sunrise[11:]
    sunset = unix_to_utc(data.get('current').get('sunset'))
    sunset_time = sunset[11:]
    raw_hourly = data.get('hourly')
    count = 1
    hourly = []
    for hour in raw_hourly:
        tempDict = {}
        weather = hour.get("weather")[0]
        tempDict['forecast'] = f"In {count} hour(s) from now: {weather.get('description')}"
        tempDict['icon_url'] = f"http://openweathermap.org/img/wn/{weather.get('icon')}@2x.png"
        hourly.append(tempDict)
        count += 1
    return render_template("weather.html", temperature=temperature, date=date, sunrise=sunrise_time, sunset=sunset_time,
                           hourly=hourly)


def unix_to_utc(time_param):
    real_time = datetime.datetime.fromtimestamp(time_param).strftime('%m-%d-%Y %H:%M:%S')
    return real_time


@app.route("/location")
def location():
    return render_template("location.html")


@app.route("/walkscore")
def walkscore():
    return render_template("walkscore.html")


@app.route("/demographics")
def demographics():
    #this has the lat and long saved
    return render_template("demographics.html", lat = session['lat'], long = session['long'])


if __name__ == "__main__":
    app.run()