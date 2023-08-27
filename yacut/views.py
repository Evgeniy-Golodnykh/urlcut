from flask import abort, flash, redirect, render_template, url_for

from settings import REDIRECT_FUNCTION_NAME

from . import app
from .error_handlers import LinkCreationError, ValidationError
from .forms import URLForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    try:
        if not form.validate_on_submit():
            return render_template('index.html', form=form)
        url_map = URLMap.create(form.original_link.data, form.custom_id.data)
        return render_template(
            'index.html',
            form=form,
            link=url_for(
                REDIRECT_FUNCTION_NAME,
                short_id=url_map.short,
                _external=True
            )
        )
    except (ValidationError, LinkCreationError) as error:
        flash(error.message)
    return render_template('index.html', form=form)


@app.route('/<string:short_id>', methods=['GET'])
def redirect_url(short_id):
    url_map = URLMap.get(short_id)
    if not url_map:
        abort(404)
    return redirect(url_map.original)
