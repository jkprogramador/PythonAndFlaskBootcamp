from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, BooleanField, \
    RadioField, SelectField, TextAreaField
from wtforms.validators import DataRequired


class InfoForm(FlaskForm):
    breed = StringField(label="What breed are you?")
    submit = SubmitField(label="Submit")


class MyForm(FlaskForm):
    breed = StringField(label="What breed are you?",
                        validators=[DataRequired()])
    neutered = BooleanField(label="Have you been neutered?")
    mood = RadioField(label="Please choose your mood:",
                      choices=[("mood_one", "Happy"), ("mood_two", "Excited")])
    food_choice = SelectField(label="Pick your favorite food:",
                              choices=[("chi", "Chicken"), ("bf", "Beef"),
                                       ("fish", "Fish")])
    feedback = TextAreaField(label="Give us your feedback")
    submit = SubmitField(label="Submit")
