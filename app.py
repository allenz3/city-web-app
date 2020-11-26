import os, script

from flask import Flask, render_template

# absolute path to my project directory, you can comment this out
os.chdir("E:/UW/Autumn Quarter 2020/HCDE 310/Project/city-web-app")

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/location")
def location():
    return render_template("location.html")

@app.route("/weather")
def weather():
    return render_template("weather.html")

@app.route("/walkscore")
def walkscore():
    return render_template("walkscore.html")

@app.route("/demographics")
def demographics():
    return render_template("demographics.html")

if __name__ == "__main__":
    app.run()