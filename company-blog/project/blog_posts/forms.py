from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class BlogPostForm(FlaskForm):
    """
    Form for submitting a blog post.
    """
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Body", validators=[DataRequired()])
    submit = SubmitField("Submit")
