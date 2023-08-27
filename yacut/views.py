from flask import abort, flash, redirect, render_template, url_for

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
        urlmap = URLMap.create_urlmap_instance(
            original=form.original_link.data,
            short=form.custom_id.data,
        )
        return render_template(
            'index.html',
            form=form,
            link=url_for(
                redirect_url.__name__,
                short_id=urlmap.short,
                _external=True
            )
        )
    except ValidationError as error:
        flash(error.message)
    except LinkCreationError as error:
        flash(error.message)
    return render_template('index.html', form=form)


@app.route('/<string:short_id>', methods=['GET'])
def redirect_url(short_id):
    urlmap = URLMap.get_urlmap_instance(short_id)
    if not urlmap:
        abort(404)
    return redirect(urlmap.original)
