from datetime import datetime

from flask import url_for

from settings import (
    REDIRECT_FUNCTION_NAME, SHORT_ID_MAX_LENGTH, URL_MAX_LENGTH,
)

from . import db


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
