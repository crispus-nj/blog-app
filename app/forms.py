from xml.dom import ValidationErr
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms import StringField, EmailField, PasswordField, SubmitField
from app.models import User

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=50)])
    submit = SubmitField("Log In")

class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired(), Length(min=6, max=30)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=50)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Sign Up")

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationErr('Email already taken!')
