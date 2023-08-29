from flask import jsonify, request

from . import app
from .error_handlers import (
    InvalidAPIUsage, LinkCreationError, ShortIdExistError, ValidationError,
)
from .models import URLMap

EMPTY_REQUEST_MESSAGE = 'Отсутствует тело запроса'
EMPTY_URL_MESSAGE = '"url" является обязательным полем запроса'
SHORT_ID_NOT_EXIST_MESSAGE = 'Указанный id не найден'


@app.route('/api/id/', methods=['POST'])
def add_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(EMPTY_REQUEST_MESSAGE)
    if 'url' not in data:
        raise InvalidAPIUsage(EMPTY_URL_MESSAGE)
    short_id = data.get('custom_id')
    try:
        return (
            jsonify(URLMap.create(data.get('url'), short_id, True).to_dict()),
            201
        )
    except (ValidationError, LinkCreationError, ShortIdExistError) as error:
        raise InvalidAPIUsage(str(error))


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_short_link(short_id):
    url_map = URLMap.get(short_id)
    if url_map is None:
        raise InvalidAPIUsage(SHORT_ID_NOT_EXIST_MESSAGE, 404)
    return jsonify({'url': url_map.original}), 200
