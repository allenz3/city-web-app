# city-web-app
Project Proposal

Overview

Oftentimes, people need to look up information about a city, but end up juggling between multiple sources and only having access to static data. In this project, we will be building a website where the user inputs a city name and the website will display aggregated live information and data visualizations about the city, updated every time the user enters a search. This way, the user can see the dynamically updated information about a city all in one location. The website will be useful for someone looking to introduce themselves to a city’s current characteristics. Situations where someone might use our website include: someone looking to move to a city, someone going on vacation to a city, someone comparing the information of different cities, someone looking to invest in a city, and more. 

APIs Used

OpenWeatherMap API: The first page our website will have is a weather forecast section. Every time a user searches for a city, the weather forecast is updated with live weather information for the current day and the following days. The OpenWeatherMap API has a “One Call API” that can give minute forecasts for 1 hour, hourly forecasts for 48 hours, daily forecasts for 7 days, and historical data for 5 previous days. The user can choose which forecast to display with a drop-down list.
https://openweathermap.org/api

Google Maps Platform APIs, Sunset and sunrise times API: We want to use the Google Maps API to find the latitude and the longitude of a city, and list it out on this page. After that, we want to display a Mercator Projection map of the world with the city labelled (name, latitude, and longitude). This page will also list out the sunrise and sunset times of the selected city. If time permits, we want the map to divided into day/night sections (the areas of the world that are currently in day time are bright and the areas of the world currently in nighttime are shaded). We’d also like to add a new page to show places of interest with the Google Maps API (if we have enough time). Showing the user cool locations in the city will help give them a better picture of the city’s environment and generate interest.
https://developers.google.com/maps/apis-by-platform
https://sunrise-sunset.org/api

Climate Data API: Using this API, we want to track the monthly and annual rainfall and temperature changes of a city. If it’s possible, we can compare the average rainfall and temperature to cities around the world, and give the city an average rainfall and precipitation percentile rating.
https://datahelpdesk.worldbank.org/knowledgebase/articles/902061-climate-data-api#:~:text=The%20Climate%20Data%20API%20provides%20programmatic%20access%20to,abide%20by%20the%20World%20Bank%E2%80%99s%20Terms%20of%20Use.

Walk Score API: Displaying the Walk Score of a city will help users determine how walker-friendly the area is. Besides a walk score, a useful statistic for the user will also be a Transit score. This metric will indicate how effective public transportation is in the city. To get the Walk Score and the Transit Score, we will use the Walk Score API” provided to us for free as long as we adhere to their branding requirements.
https://api.walkscore.com/score?format=json&address=1119%8th%20Avenue%20Seattle%20WA%2098101&lat=47.6085&lon=-122.3295&transit=1&bike=1&wsapikey=<YOUR-WSAPIKEY>

SchoolDigger API, Census.gov API: Understanding the demography of a city will give insight on how the city is structured. That is why we plan to use the Census API to display vital information like population density, median age, and more. Additionally, we will use the SchoolDigger API to inform the user of school district rankings.
https://developer.schooldigger.com/
https://www.census.gov/data/developers/data-sets.html

Output Format

The output format will be a website. We will have a home page where the user inputs a city they are trying to look up information for. After a successful confirmation, the user is free to browse the navigation bar and tab to the page with the information they want to view. One big advantage of this format over having one large page is that the user will only see what they want to see. Since we only have to make an API call once a tab is selected, the user doesn’t have to load everything at once, and it will be less taxing on the client and server. Our output format is a website because of how accessible and functional it is to our users. Computers and other internet-connected digital devices are prevalent throughout the world today and many people can access websites through them. Using a website allows us to be flexible with our design without sacrificing functionality.

Development Timeline

Week 1: We first plan to make the HTML pages for our home page and our intended sections using Flask and Jinja. Afterwards, we plan on using CSS to give our pages a consistent and aesthetically pleasing theme. During this time we will also be attempting to retrieve data from the APIs and research their contents. By the end of this week, we should have an empty website up and running and have our APIs be functional.

Week 2: After we get the data from the APIs, we will start writing Python scripts to process, extract, and display the data onto the website tabs. When a search is performed and a tab is clicked, relevant information should be shown. By the end of this week, our website should be an interactive aggregation of the data we have gathered. 

Week 3: We will work on implementing transformative work on the data, such as building a map or a chart. Our data visualization will take data, analyze it, and then turn it into something that is meaningful to view. By the end of this week, we should have at least one transformative data visualization to display on our website. If possible, we should try to finish at least one of our stretch goals.

