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
    short_id = data.get('custom_id', None)
    try:
        return (
            jsonify(URLMap.create(data.get('url'), short_id, True).to_dict()),
            201
        )
    except ShortExistError:
        raise InvalidAPIUsage(SHORT_ID_EXIST_MESSAGE.format(short_id=short_id))
    except (ValidationError, LinkCreationError) as error:
        raise InvalidAPIUsage(str(error))


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_short_link(short_id):
    url_map = URLMap.get(short_id)
    if url_map is None:
        raise InvalidAPIUsage(EMPTY_SHORT_ID_MESSAGE, 404)
    return jsonify({'url': url_map.original}), 200
