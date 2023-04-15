from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, SubmitField


class LoginForm(FlaskForm):
    email = StringField(
        'E-mail',
        [
            validators.DataRequired(),
            validators.Email(),
            validators.Length(min=6, max=200),
        ],
        filters=[lambda data: data and data.lower()],
    )
    password = PasswordField(
        'Password',
        [
            validators.DataRequired(),
            validators.EqualTo('confirm_password', message='Field must be equal to password'),
        ],
    )
    submit = SubmitField('Login')