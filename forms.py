from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class SearchForm(FlaskForm):
    search = StringField("Enter a City Name")
    submit = SubmitField("Search")