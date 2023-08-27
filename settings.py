import os
import re
from string import ascii_letters, digits

ALLOWED_SYMBOLS = ascii_letters + digits
URL_MAX_LENGTH = 500
SHORT_ID_MAX_LENGTH = 16
SHORT_ID_GENERATION_LENGTH = 6
SHORT_ID_GENERATION_NUMBER = 20
SHORT_ID_REGEXP = re.compile(rf'^[{re.escape(ALLOWED_SYMBOLS)}]+$')
REDIRECT_FUNCTION_NAME = 'redirect_url'


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI',
        default='sqlite:///db.sqlite3'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', default='MY_SECRET_KEY')
