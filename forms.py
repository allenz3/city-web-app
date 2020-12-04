from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class SearchForm(FlaskForm):
    city_search = StringField("Enter a city name")
    state_search = StringField("Enter the city's state code")
    submit = SubmitField("Search")