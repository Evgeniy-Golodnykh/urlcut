from flask import abort, flash, redirect, render_template, url_for

from settings import REDIRECT_FUNCTION_NAME

from . import app
from .error_handlers import (
    LinkCreationError, ShortIdExistError, ValidationError,
)
from .forms import URLForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        return render_template(
            'index.html',
            form=form,
            link=url_for(
                REDIRECT_FUNCTION_NAME,
                short_id=URLMap.create(form.original_link.data,
                                       form.custom_id.data).short,
                _external=True
            )
        )
    except (ValidationError, LinkCreationError, ShortIdExistError) as error:
        flash(str(error))
    return render_template('index.html', form=form)


@app.route('/<string:short_id>', methods=['GET'])
def redirect_url(short_id):
    url_map = URLMap.get(short_id)
    if not url_map:
        abort(404)
    return redirect(url_map.original)
