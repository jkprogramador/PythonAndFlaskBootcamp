from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length, InputRequired
from wtforms.validators import ValidationError
from myproject.models import User


class RegistrationForm(FlaskForm):
    """
    Form for registering a user.
    """
    username = StringField(label="Username", validators=[
        DataRequired()])
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[InputRequired(),
                                                           Length(min=8),
                                                           EqualTo(
                                                               fieldname="confirm_password",
                                                               message="Passwords must match.")])
    confirm_password = PasswordField(label="Confirm Password",
                                     validators=[DataRequired()])
    submit = SubmitField(label="Register")

    def validate_email(self, email):
        if User.query.filter_by(email=self.email.data).first():
            raise ValidationError("Email has been already registered.")

    def validate_username(self, username):
        if User.query.filter_by(username=self.username.data).first():
            raise ValidationError("Username has already been registered.")


class LoginForm(FlaskForm):
    """
    Form for loging user.
    """
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Login")
