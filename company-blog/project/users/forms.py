from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, EqualTo, Length, \
    InputRequired
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed
from project.models import User


class RegistrationForm(FlaskForm):
    """
    Form for user registration.
    """
    username = StringField("Username",
                           validators=[DataRequired(), Length(min=8)])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password",
                             validators=[InputRequired(),
                                         EqualTo(fieldname="confirm_password",
                                                 message="Passwords must match."),
                                         Length(min=8)])
    confirm_password = PasswordField("Confirm Password",
                                     validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_email(self, email):
        if User.query.filter_by(email=self.email.data).first():
            raise ValidationError("Email registered already exists.")

    def validate_username(self, username):
        if User.query.filter_by(username=self.username.data).first():
            raise ValidationError("Username registered already exists.")


class UpdateUserForm(FlaskForm):
    """
    Form for updating user information.
    """
    username = StringField("Username",
                           validators=[DataRequired(), Length(min=8)])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    picture = FileField("Update Profile Picture",
                        validators=[FileAllowed(["jpg", "png"])])
    submit = SubmitField("Update")

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Email registered already exists.")

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("Username registered already exists.")


class LoginForm(FlaskForm):
    """
    Form for login.
    """
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")
