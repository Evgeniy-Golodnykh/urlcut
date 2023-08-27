from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp

from settings import SHORT_ID_MAX_LENGTH, SHORT_ID_REGEXP, URL_MAX_LENGTH

from .error_handlers import ValidationError
from .models import URLMap

ORIGINAL_URL_LABLE = 'Длинная ссылка'
SHORT_ID_LABLE = 'Ваш вариант короткой ссылки'
SUBMIT_LABLE = 'Создать'
REQUIRED_MESSAGE = 'Обязательное поле'
SHROT_ID_EXIST_ERROR_MESSAGE = 'Имя {short_id} уже занято!'


class URLForm(FlaskForm):
    original_link = URLField(
        ORIGINAL_URL_LABLE,
        validators=[
            DataRequired(message=REQUIRED_MESSAGE),
            Length(max=URL_MAX_LENGTH),
            URL()
        ]
    )
    custom_id = StringField(
        SHORT_ID_LABLE,
        validators=[
            Length(max=SHORT_ID_MAX_LENGTH),
            Regexp(regex=SHORT_ID_REGEXP),
            Optional()
        ]
    )
    submit = SubmitField(SUBMIT_LABLE)

    def validate_custom_id(self, custom_id):
        short_id = custom_id.data
        if URLMap.query.filter_by(short=short_id).first():
            raise ValidationError(
                SHROT_ID_EXIST_ERROR_MESSAGE.format(short_id=short_id)
            )
