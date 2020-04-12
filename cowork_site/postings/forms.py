from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, TextAreaField, validators

length_error_message = "должно быть от %(min)d до %(max)d символов"


class PostingCreateForm(FlaskForm):
    name = StringField('Название', [validators.Length(min=5, max=30, message=length_error_message)])
    oneliner = StringField('Заголовок', [validators.Length(min=5, max=40,  message=length_error_message)])
    description = TextAreaField('описание', [validators.Length(min=5, max=300, message=length_error_message)])
    cv_url = StringField('Ссылка на CV/Портфолио', [validators.Length(min=5, max=100, message=length_error_message),
                                                    validators.URL(message="Это точно ссылка?")])


class TeamPostingCreateForm(FlaskForm):
    name = StringField('Название', [validators.Length(min=5, max=50, message=length_error_message)])
    oneliner = StringField('Заголовок', [validators.Length(min=5, max=80, message=length_error_message)])
    description = TextAreaField('Описание', [validators.Length(min=5, max=500, message=length_error_message)])
    url = StringField('Ссылка', [validators.Optional(), validators.Length(max=100, message=length_error_message),
                                 validators.URL(message="Это точно ссылка?")], )
    contact = StringField('Контакт', [validators.Optional(), validators.Length(max=100, message=length_error_message)])
