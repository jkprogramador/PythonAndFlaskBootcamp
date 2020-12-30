from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class AddForm(FlaskForm):
    """
    Form for creating a puppy.
    """
    name = StringField(label="Puppy name", validators=[
        DataRequired(message="Please enter the name of the puppy.")])
    submit = SubmitField(label="Add puppy")


class DeleteForm(FlaskForm):
    """
    Form for deleting a puppy.
    """
    id = IntegerField(label="ID number of puppy", validators=[DataRequired(
        message="Please enter the id of the puppy to be removed.")])
    submit = SubmitField(label="Remove puppy")
