from flask import jsonify, request

from . import app
from .error_handlers import (
    InvalidAPIUsage, LinkCreationError, ShortExistError, ValidationError,
)
from .models import URLMap

EMPTY_REQUEST_MESSAGE = 'Отсутствует тело запроса'
EMPTY_SHORT_ID_MESSAGE = 'Указанный id не найден'
EMPTY_URL_MESSAGE = '"url" является обязательным полем!'
SHORT_ID_EXIST_MESSAGE = 'Имя "{short_id}" уже занято.'


@app.route('/api/id/', methods=['POST'])
def add_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(EMPTY_REQUEST_MESSAGE)
    if 'url' not in data:
        raise InvalidAPIUsage(EMPTY_URL_MESSAGE)
    original_url = data.get('url')
    short_id = data.get('custom_id', None)
    try:
        urlmap = URLMap.create_urlmap_instance(original_url, short_id)
    except ShortExistError:
        raise InvalidAPIUsage(SHORT_ID_EXIST_MESSAGE.format(short_id=short_id))
    except ValidationError as error:
        raise InvalidAPIUsage(error.message)
    except LinkCreationError as error:
        raise InvalidAPIUsage(error.message)
    return jsonify(urlmap.to_dict()), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_short_link(short_id):
    urlmap = URLMap.get_urlmap_instance(short_id)
    if urlmap is None:
        raise InvalidAPIUsage(EMPTY_SHORT_ID_MESSAGE, 404)
    return jsonify({'url': urlmap.original}), 200
