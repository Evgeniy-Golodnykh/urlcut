from datetime import datetime

from flask import url_for

from settings import SHORT_LINK_MAX_LENGTH

from . import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(), nullable=False)
    short = db.Column(db.String(SHORT_LINK_MAX_LENGTH), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                'redirect_url',
                short_link=self.short,
                _external=True
            )
        )
