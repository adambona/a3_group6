from .forms import createEventForm
from .models import Event
from flask import Blueprint, render_template, request, redirect, url_for

bp = Blueprint('createEvent', __name__)

@bp.route('/createEvent', methods=['GET', 'POST'])
def createEvent():
    form = createEventForm()
    if form.validate_on_submit():
        print('Successfully created new event', 'success')
        return redirect(url_for('createEvent.createEvent'))
    return render_template('createEvent.html', form=form)

  

