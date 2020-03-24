from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, validators


class CandidateCreateForm(FlaskForm):
    name = StringField('name', [validators.Length(min=5, max=30)])
    description = StringField('description', [validators.Length(min=5, max=100)])
    cv_url = StringField('cv_url', [validators.Length(min=5, max=100), validators.URL()])
    email = StringField('email', [validators.Length(min=6, max=35), validators.Email()])
