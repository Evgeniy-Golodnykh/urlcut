from random import choices

from flask import abort, flash, redirect, render_template, url_for

from settings import (
    ALLOWED_SYMBOLS, SHORT_LINK_GENERATION_LENGTH,
    SHORT_LINK_GENERATION_NUMBER,
)

from . import app, db
from .error_handlers import LinkCreationError
from .forms import URLForm
from .models import URLMap

LINK_CREATION_ERROR_MESSAGE = 'Ошибка создания короткой ссылки'
LINK_EXIST_ERROR_MESSAGE = 'Имя {short_link} уже занято!'


def get_unique_short_id():
    for _ in range(SHORT_LINK_GENERATION_NUMBER):
        short_link = ''.join(
            choices(ALLOWED_SYMBOLS, k=SHORT_LINK_GENERATION_LENGTH)
        )
        if not URLMap.query.filter_by(short=short_link).first():
            return short_link
    raise LinkCreationError(LINK_CREATION_ERROR_MESSAGE)


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        original_url, short_link = form.original_link.data, form.custom_id.data
        if short_link:
            if URLMap.query.filter_by(short=short_link).first():
                flash(LINK_EXIST_ERROR_MESSAGE.format(short_link=short_link))
                return render_template('index.html', form=form)
        else:
            short_link = get_unique_short_id()
        urlmap = URLMap(
            original=original_url,
            short=short_link,
        )
        db.session.add(urlmap)
        db.session.commit()
        return render_template(
            'index.html',
            form=form,
            link=url_for(
                redirect_url.__name__,
                short_link=short_link,
                _external=True
            )
        )
    return render_template('index.html', form=form)


@app.route('/<string:short_link>', methods=['GET'])
def redirect_url(short_link):
    urlmap = URLMap.query.filter_by(short=short_link).first()
    if not urlmap:
        abort(404)
    return redirect(urlmap.original)
