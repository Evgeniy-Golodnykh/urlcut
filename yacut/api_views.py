import re
from urllib.parse import urlparse

from flask import jsonify, request

from settings import SHORT_LINK_MAX_LENGTH, SHORT_LINK_REGEXP

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id

EMPTY_REQUEST_MESSAGE = 'Отсутствует тело запроса'
EMPTY_URL_MESSAGE = '"url" является обязательным полем!'
WRONG_URL_MESSAGE = 'Введите корректный URL адрес'
WRONG_SHORT_LINK_MESSAGE = 'Указано недопустимое имя для короткой ссылки'
LINK_EXIST_ERROR_MESSAGE = 'Имя "{short_link}" уже занято.'


def url_validator(url):
    parsed = urlparse(url)
    return all([parsed.scheme, parsed.netloc])


@app.route('/api/id/', methods=['POST'])
def add_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(EMPTY_REQUEST_MESSAGE)
    if 'url' not in data:
        raise InvalidAPIUsage(EMPTY_URL_MESSAGE)
    original_url = data.get('url')
    if not url_validator(original_url):
        raise InvalidAPIUsage(WRONG_URL_MESSAGE)
    short_link = data.get('custom_id', None)
    if short_link:
        if not re.match(SHORT_LINK_REGEXP, short_link) \
           or len(short_link) > SHORT_LINK_MAX_LENGTH:
            raise InvalidAPIUsage(WRONG_SHORT_LINK_MESSAGE)
        if URLMap.query.filter_by(short=short_link).first():
            raise InvalidAPIUsage(
                LINK_EXIST_ERROR_MESSAGE.format(short_link=short_link)
            )
    else:
        short_link = get_unique_short_id()
    urlmap = URLMap(original=original_url, short=short_link)
    db.session.add(urlmap)
    db.session.commit()
    return jsonify(urlmap.to_dict()), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_short_link(short_id):
    urlmap = URLMap.query.filter_by(short=short_id).first()
    if urlmap is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': urlmap.original})
