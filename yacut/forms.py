from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp

from settings import SHORT_LINK_MAX_LENGTH, SHORT_LINK_REGEXP

ORIGINAL_URL_LABLE = 'Длинная ссылка'
SHORT_LINK_LABLE = 'Ваш вариант короткой ссылки'
SUBMIT_LABLE = 'Создать'
REQUIRED_MESSAGE = 'Обязательное поле'


class URLForm(FlaskForm):
    original_link = URLField(
        ORIGINAL_URL_LABLE,
        validators=[DataRequired(message=REQUIRED_MESSAGE), URL()]
    )
    custom_id = StringField(
        SHORT_LINK_LABLE,
        validators=[
            Length(max=SHORT_LINK_MAX_LENGTH),
            Regexp(regex=SHORT_LINK_REGEXP),
            Optional()
        ]
    )
    submit = SubmitField(SUBMIT_LABLE)
