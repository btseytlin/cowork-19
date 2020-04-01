from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, TextAreaField, validators


class PostingCreateForm(FlaskForm):
    name = StringField('name', [validators.Length(min=5, max=30)])
    oneliner = StringField('oneliner', [validators.Length(min=5, max=40)])
    description = TextAreaField('description', [validators.Length(min=5, max=300)])
    cv_url = StringField('cv_url', [validators.Length(min=5, max=100), validators.URL()])
