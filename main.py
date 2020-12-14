import os, api_keys, urllib.parse, urllib.request, urllib.error, json, datetime, Photo
from flask import Flask, render_template, request, redirect, url_for, session
from forms import SearchForm

# absolute path to my project directory, you can comment this out
# os.chdir("E:/UW/Autumn Quarter 2020/HCDE 310/Project/city-web-app")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'citywebapp'


@app.route("/")
@app.route("/", methods=['POST', 'GET'])
@app.route("/home")
@app.route("/home", methods=['POST', 'GET'])
# def home(form, isValid):
def home():
    form = SearchForm()
    session['render_invalid_input'] = False
    if session['render_invalid_input']:
        return render_template('home.html', form=form, isValid=-1)
    # Search button pressed
    if form.is_submitted():
        city_result = request.form.get('city_search')
        state_result = request.form.get('state_search')
        # some text inputted in both boxes
        if city_result != "" and state_result != "":
            # this will help us get the coordinates of a city
            session['city_result'] = city_result.strip()
            session['state_result'] = state_result.strip()
            coords = api_call('https://api.openweathermap.org/data/2.5/weather?',
                              {'q': session['city_result'], 'appid': api_keys.openweather_key})
            # valid input
            if coords is not None:
                latitude_city = coords.get('coord').get('lat')
                longitude_city = coords.get('coord').get('lon')
                session['latitude'] = latitude_city
                session['longitude'] = longitude_city
                return render_template('home.html', form=form, isValid=1)
            # invalid input
            else:
                return render_template('home.html', form=form, isValid=-1)
        # one or both boxes empty when submitted
        else:
            return render_template('home.html', form=form, isValid=-1)
    # Search button not pressed, normal loading
    else:
        return render_template('home.html', form=form, isValid=0)


# gives the temperature, date, sunrise/sunset, and hourly forecast of a city
@app.route("/weather")
def weather():
    try:
        weatherData = api_call('https://api.openweathermap.org/data/2.5/onecall?',
                               {'lat': session['latitude'], 'lon': session['longitude'],
                                'appid': api_keys.openweather_key,
                                'units': "imperial"})
    except:
        # data was not successfully retrieved, return to home page with invalid input reminder
        return render_template('home.html', form=SearchForm(), isValid=-1)
        # return redirect(url_for('home', form=SearchForm(), isValid=-1))
    else:
        # if the data was successfully retrieved
        if weatherData is not None:
            temperature = weatherData.get('current').get('temp')
            sunrise = unix_to_utc(weatherData.get('current').get('sunrise'))
            date = sunrise[0:10]
            sunrise_time = sunrise[11:]
            sunset = unix_to_utc(weatherData.get('current').get('sunset'))
            sunset_time = sunset[11:]
            # hourly forecast
            raw_hourly = weatherData.get('hourly')
            count = 1
            hourly = []
            for hour in raw_hourly:
                tempDict = {}
                weather = hour.get("weather")[0]
                tempDict['temperature'] = hour.get("temp")
                tempDict['forecast'] = f"In {count} hour(s) from now: {weather.get('description')}"
                tempDict['icon_url'] = f"http://openweathermap.org/img/wn/{weather.get('icon')}@2x.png"
                hourly.append(tempDict)
                count += 1
            # daily forecast
            raw_daily = weatherData.get('daily')
            count = 1
            daily = []
            for day in raw_daily:
                tempDict = {}
                weather = day.get("weather")[0]
                tempDict['min_temperature'] = day.get("temp").get("min")
                tempDict['max_temperature'] = day.get("temp").get("max")
                tempDict['forecast'] = f"In {count} day(s) from now: {weather.get('description')}"
                tempDict['icon_url'] = f"http://openweathermap.org/img/wn/{weather.get('icon')}@2x.png"
                daily.append(tempDict)
                count += 1
            return render_template("weather.html", temperature=temperature, date=date, sunrise=sunrise_time,
                                   sunset=sunset_time,
                                   hourly=hourly, daily=daily)
        else:
            # return render_template('home.html', form=SearchForm(), isValid=-1)
            session['render_invalid_input'] = True
            return redirect('/home')


def unix_to_utc(time_param):
    real_time = datetime.datetime.fromtimestamp(time_param).strftime('%m-%d-%Y %H:%M:%S')
    return real_time


@app.route("/location")
def location():
    try:
        temp_city = session['city_result']
    except:
        return render_template('home.html', form=SearchForm(), isValid=-1)
    else:
        temp_city = temp_city.replace(' ', '+')
        return render_template("location.html", latitude=session['latitude'], longitude=session['longitude'],
                               url=f"https://www.google.com/maps/embed/v1/search?key={api_keys.google_maps_key}&q={temp_city}")


# gives the top ten school districts in a city
@app.route("/education")
def education():
    try:
        # API Call for school digger
        # https://api.schooldigger.com/v1.2/districts?st=MI&boxLatitudeNW=42.7&boxLongitudeNW=-83.5&boxLatitudeSE=42.2&boxLongitudeSE=-82.9&sortBy=rank&appID=73eb2e3f&appKey=969aded5acde08d49a26da440d06e372
        # districtData = api_call('https://api.schooldigger.com/v1.2/districts?',
        #                         {'st': session['state_result'], 'boxLatitudeNW': session['latitude'] - 0.5,
        #                          'boxLongitudeNW': session['longitude'] - 0.5,
        #                          'boxLatitudeSE': session['latitude'] + 0.5,
        #                          'boxLongitudeSE': session['longitude'] + 0.5, 'sortBy': 'rank',
        #                          'appID': api_keys.schooldigger_app_id,
        #                          'appKey': api_keys.schooldigger_key})
        # using data from local files
        if session['city_result'] is not None and session['state_result'] is not None:
            districtData = json.load(open('./json/schooldigger_data.json', encoding="utf-8"))
    except:
        return render_template('home.html', form=SearchForm(), isValid=-1)
    else:
        # if the data was successfully retrieved
        if districtData is not None:
            districtList = districtData.get('districtList')
            districts = []
            if len(districtList) == 0:
                return render_template("education.html", city=session['city_result'], state=session['state_result'],
                                       districts=districts)
            else:
                for district in districtList:
                    districtInfo = {}
                    districtInfo['District Name'] = district.get("districtName")
                    districtInfo['Phone Number'] = district.get("phone")
                    districtInfo['Street Address'] = district.get("address").get("street")
                    districtInfo['City'] = district.get("address").get("city")
                    districtInfo['State Code'] = district.get("address").get("state")
                    districtInfo['Zip Code'] = district.get("address").get("zip")
                    districts.append(districtInfo)
                return render_template("education.html", city=session['city_result'], state=session['state_result'],
                                       districts=districts)
        # data was not successfully retrieved, return to home page with invalid input reminder
        else:
            return render_template('home.html', form=SearchForm(), isValid=-1)


@app.route("/photos")
def photos():
    try:
        photos_info = Photo.get_photo_info(session['city_result'], session['city_result'], 10)
        photos = [Photo.Photo(photo_info) for photo_info in photos_info]
    except:
        return render_template('home.html', form=SearchForm(), isValid=-1)
    else:
        return render_template("photos.html", photos=photos, city=session['city_result'], state=session['state_result'])


def api_call(baseurl, paramDict):
    paramString = urllib.parse.urlencode(paramDict)
    request = baseurl + paramString
    print("THIS IS THE LINK: " + request)
    reader = safe_get(request)
    if reader is not None:
        readerStr = reader.read()
        data = json.loads(readerStr)
        return data
    else:
        return None


def safe_get(url):
    try:
        return urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        print("The server couldn't fulfill the request.")
        print("Error code: ", e.code)
    except urllib.error.URLError as e:
        print("We failed to reach a server")
        print("Reason: ", e.reason)
    return None


if __name__ == "__main__":
    app.run(debug=True)