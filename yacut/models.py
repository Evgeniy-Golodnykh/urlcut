import re
from datetime import datetime
from random import choices
from urllib.parse import urlparse

from flask import url_for

from settings import (
    ALLOWED_SYMBOLS, REDIRECT_FUNCTION_NAME, SHORT_ID_GENERATION_LENGTH,
    SHORT_ID_GENERATION_NUMBER, SHORT_ID_MAX_LENGTH, SHORT_ID_REGEXP,
    URL_MAX_LENGTH,
)

from . import db
from .error_handlers import LinkCreationError, ShortExistError, ValidationError

SHORT_ID_CREATION_ERROR_MESSAGE = 'Ошибка создания короткой ссылки'
SHORT_ID_EXIST_MESSAGE = 'Имя {short} уже занято!'
WRONG_URL_MESSAGE = 'Введите корректный URL адрес'
WRONG_SHORT_ID_MESSAGE = 'Указано недопустимое имя для короткой ссылки'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(URL_MAX_LENGTH), nullable=False)
    short = db.Column(db.String(SHORT_ID_MAX_LENGTH), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                REDIRECT_FUNCTION_NAME,
                short_id=self.short,
                _external=True
            )
        )

    @staticmethod
    def get_unique_short_id():
        for _ in range(SHORT_ID_GENERATION_NUMBER):
            short_id = ''.join(
                choices(ALLOWED_SYMBOLS, k=SHORT_ID_GENERATION_LENGTH)
            )
            if not URLMap.get(short_id):
                return short_id
        raise LinkCreationError(SHORT_ID_CREATION_ERROR_MESSAGE)

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def create(original, short):
        if len(original) > URL_MAX_LENGTH or not url_validator(original):
            raise ValidationError(WRONG_URL_MESSAGE)
        if short:
            if (len(short) > SHORT_ID_MAX_LENGTH or
               not re.match(SHORT_ID_REGEXP, short)):
                raise ValidationError(WRONG_SHORT_ID_MESSAGE)
            if URLMap.get(short):
                raise ShortExistError(
                    SHORT_ID_EXIST_MESSAGE.format(short=short)
                )
        else:
            short = URLMap.get_unique_short_id()
        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map


def url_validator(url):
    parsed = urlparse(url)
    return all([parsed.scheme, parsed.netloc])
