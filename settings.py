import os
import re
from string import ascii_letters, digits

ALLOWED_SYMBOLS = ascii_letters + digits
SHORT_LINK_MAX_LENGTH = 16
SHORT_LINK_GENERATION_LENGTH = 6
SHORT_LINK_GENERATION_NUMBER = 20
SHORT_LINK_REGEXP = re.compile(rf'^[{re.escape(ALLOWED_SYMBOLS)}]+$')


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI',
        default='some_db_url'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', default='MY_SECRET_KEY')
