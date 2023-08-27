from random import choices

from flask import abort, flash, redirect, render_template, url_for

from settings import (
    ALLOWED_SYMBOLS, SHORT_ID_GENERATION_LENGTH, SHORT_ID_GENERATION_NUMBER,
)

from . import app, db
from .error_handlers import LinkCreationError
from .forms import URLForm
from .models import URLMap

SHROT_ID_CREATION_ERROR_MESSAGE = 'Ошибка создания короткой ссылки'
SHROT_ID_EXIST_ERROR_MESSAGE = 'Имя {short_id} уже занято!'


def get_unique_short_id():
    for _ in range(SHORT_ID_GENERATION_NUMBER):
        short_id = ''.join(
            choices(ALLOWED_SYMBOLS, k=SHORT_ID_GENERATION_LENGTH)
        )
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id
    raise LinkCreationError(SHROT_ID_CREATION_ERROR_MESSAGE)


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        original_url, short_id = form.original_link.data, form.custom_id.data
        if short_id:
            if URLMap.query.filter_by(short=short_id).first():
                flash(SHROT_ID_EXIST_ERROR_MESSAGE.format(short_id=short_id))
                return render_template('index.html', form=form)
        else:
            short_id = get_unique_short_id()
        urlmap = URLMap(
            original=original_url,
            short=short_id,
        )
        db.session.add(urlmap)
        db.session.commit()
        return render_template(
            'index.html',
            form=form,
            link=url_for(
                redirect_url.__name__,
                short_id=short_id,
                _external=True
            )
        )
    return render_template('index.html', form=form)


@app.route('/<string:short_id>', methods=['GET'])
def redirect_url(short_id):
    urlmap = URLMap.query.filter_by(short=short_id).first()
    if not urlmap:
        abort(404)
    return redirect(urlmap.original)
