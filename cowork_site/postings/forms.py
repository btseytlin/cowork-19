from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, validators


class PostingCreateForm(FlaskForm):
    name = StringField('name', [validators.Length(min=5, max=30)])
    description = StringField('description', [validators.Length(min=5, max=100)])
    cv_url = StringField('cv_url', [validators.Length(min=5, max=100), validators.URL()])
