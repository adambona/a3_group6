from .forms import createEventForm
from .models import Event
from flask import Blueprint, render_template, request, redirect, url_for
from . import db

bp = Blueprint('createEvent', __name__)

@bp.route('/createEvent', methods=['GET', 'POST'])
def createEvent():
    form = createEventForm()
    if form.validate_on_submit():
        Event = Event(genre=form.genre.data, name=form.name.data, artistName=form.artistName.data, startTime=form.startTime.data, endTime=form.endTime.data, location=form.location.data, ticketPrice=form.ticketPrice.data, numTickets=form.numTickets.data, description=form.description.data, image=form.image.data)
        db.session.add(Event)
        db.session.commit()
        print('Successfully created new event', 'success')
        return redirect(url_for('createEvent.createEvent'))
    return render_template('createEvent.html', form=form)
