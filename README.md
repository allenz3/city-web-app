# city-web-app
Website Link: https://city-web-app.wl.r.appspot.com/

## Overview

Oftentimes, people need to look up information about a city, but end up juggling between multiple sources and only having access to static data. In this project, we will be building a website where the user inputs a city name and the website will display aggregated live information and data visualizations about the city, updated every time the user enters a search. This way, the user can see the dynamically updated information about a city all in one location. The website will be useful for someone looking to introduce themselves to a city’s current characteristics. Situations where someone might use our website include: someone looking to move to a city, someone going on vacation to a city, someone comparing the information of different cities, someone looking to invest in a city, and more. 

## Pages

Home: The user can search up a city in the US along with its state code. If either input is invalid, the website will respond with a notice. Upon successful input, the website will respond with a confirmation. A valid city must be inputted in order for the other pages to run.

Location: The city's latitude and longitude are displayed here. An embedded map of the city is provided as well.

Weather: The city's current temperature, sunrise time, and sunset time are provided on this page. Drop-down displays of the hourly forecast (48 hours) and daily forecast (8 days) for the city are provided as well.

Education: The inputted city and the state code are displayed on this page. A list of the Top 10 ranked school districts in the city are provided on this page.

Photos: The photos page provides a scrollable photo gallery of photos taken of the city.

## APIs Used

OpenWeatherMap API: We are using OpenWeatherMap's free Current Weather Data API to return a city's latitude and longitude, while also using their One Call API to return a city's temperature, sunrise/sunset time, and hourly/daily weather forecasts.
https://openweathermap.org/api

Google Maps API: We are using Google Maps to embed an interactive map of the city on the Location Page.
https://developers.google.com/maps/apis-by-platform

SchoolDigger API: We are using the SchoolDigger API to return information about school districts. The API can be hard to work with so we have Detroit's school districts returned by default on the page.
https://developer.schooldigger.com/

Flickr API:
We are using Flickr to return photos for our Photos page. Flickr output may be unpredictable at times, so browse at your own risk!
https://www.flickr.com/services/api/flickr.photos.search.html
https://www.flickr.com/services/api/misc.urls.html

