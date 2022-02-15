from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import TextAreaField, SubmitField

class PostQuoteForm(FlaskForm):
    content = TextAreaField('Write a quote',validators=[DataRequired()])
    submit = SubmitField('Post Quote')

class UpdatePostForm(FlaskForm):
    content = TextAreaField('Update Your Quote',validators=[DataRequired()])
    submit = SubmitField('Update Quote')


class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Send')