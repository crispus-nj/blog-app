from wtforms.validators import DataRequired, Email
from flask_wtf import FlaskForm
from wtforms import EmailField, SubmitField

class SuscribeForm(FlaskForm):
    content = EmailField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Subscribe')