from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, ValidationError
from app.database import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[
        DataRequired(), Length(min=4, max=20)])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('username is taken')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class MessageForm(FlaskForm):
    message = StringField('Message', validators=[
        DataRequired(), Length(min=1, max=300)])
    submit = SubmitField('Send')
