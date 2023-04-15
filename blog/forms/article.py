from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, validators, SelectMultipleField

class CreateArticleForm(FlaskForm):
    title = StringField(
        "Title",
        [validators.DataRequired()],
    )
    brief = StringField(
        "Brief",
        [validators.DataRequired()],
    )
    text = TextAreaField(
        "Text",
        [validators.DataRequired()],
    )
    tags = SelectMultipleField("Tags", coerce=int)

    submit = SubmitField("Publish")