from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class AddForm(FlaskForm):
    """
    Form for adding an owner.
    """
    name = StringField(label="Name of the owner", validators=[
        DataRequired(message="Please enter the name of the owner.")])
    puppy_id = IntegerField(label="ID of the puppy", validators=[
        DataRequired(message="Please enter the ID of the puppy.")])
    submit = SubmitField(label="Add owner")
