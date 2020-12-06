import os, script
import api_keys
import urllib.parse, urllib.request, urllib.error, json
import datetime

from flask import Flask, render_template, request, redirect, url_for, session
from forms import SearchForm

# absolute path to my project directory, you can comment this out
os.chdir("E:/UW/Autumn Quarter 2020/HCDE 310/Project/city-web-app")

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
        result = request.form.get('city_search')
        session['result'] = result
        # this is the state code
        state_result = request.form.get('state_search')
        session['state_result'] = state_result
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
    coords = api_call('https://api.openweathermap.org/data/2.5/weather?',
                      {'q': session['result'], 'appid': api_keys.openweather_key})
    lat_city = coords.get('coord').get('lat')
    lon_city = coords.get('coord').get('lon')
    session['lat'] = lat_city
    session['long'] = lon_city

    # this will help us get the weather information of a city
    weatherData = api_call('https://api.openweathermap.org/data/2.5/onecall?',
                           {'lat': str(lat_city), 'lon': str(lon_city), 'appid': api_keys.openweather_key,
                            'units': "imperial"})
    temperature = weatherData.get('current').get('temp')
    sunrise = unix_to_utc(weatherData.get('current').get('sunrise'))
    date = sunrise[0:10]
    sunrise_time = sunrise[11:]
    sunset = unix_to_utc(weatherData.get('current').get('sunset'))
    sunset_time = sunset[11:]
    raw_hourly = weatherData.get('hourly')
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
    # https://api.schooldigger.com/v1.2/districts?st=MI&boxLatitudeNW=42.7&boxLongitudeNW=-83.5&boxLatitudeSE=42.2&boxLongitudeSE=-82.9&sortBy=rank&appID=73eb2e3f&appKey=969aded5acde08d49a26da440d06e372
    # districtData = api_keys('https://api.schooldigger.com/v1.2/districts?',
    #          {'st': session['state_result'], 'boxLatitudeNW': session['lat'] - 0.3,
    #           'boxLongitudeNW': session['long'] - 0.3, 'boxLatitudeSE': session['lat'] + 0.3,
    #           'boxLongitudeSE': session['long'] + 0.3, 'sortBy': 'rank', 'appID': api_keys.schooldigger_app_id,
    #           'appKey': api_keys.schooldigger_key})

    # testing using local files
    # feed = json.load(open(filename, encoding="utf-8"))
    f = open('./schooldigger_data.json', encoding="utf-8")
    data = json.load(f)
    print(data)
    # sort through JSON data and get important information
    districtList = data.get('districtList')
    districts = []
    for district in districtList:
        districtInfo = {}
        districtInfo['District Name'] = district.get("districtName")
        districtInfo['Phone Number'] = district.get("phone")
        districtInfo['Street Address'] = district.get("address").get("street")
        districtInfo['City'] = district.get("address").get("city")
        districtInfo['State Code'] = district.get("address").get("state")
        districtInfo['Zip Code'] = district.get("address").get("zip")
        districts.append(districtInfo)
    return render_template("demographics.html", data=data, lat=session['lat'], long=session['long'],
                           state=session['state_result'], districts=districts)


def api_call(baseurl, paramDict):
    paramString = urllib.parse.urlencode(paramDict)
    request = baseurl + paramString
    print("THIS IS THE LINK: " + request)
    reader = urllib.request.urlopen(request)
    readerStr = reader.read()
    data = json.loads(readerStr)
    return data


if __name__ == "__main__":
    app.run()
