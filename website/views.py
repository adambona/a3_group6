from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event
from . import db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    events = db.session.query(Event).filter(Event.status == 'Open').order_by(Event.event_date).all()
    return render_template('index.html', events=events)

@bp.route('/search')
def search():
    if request.args['search'] and request.args['search'] != "":
        query = "%" + request.args['search'] + "%" # search is the name of the form in the html file
        events = Event.query.filter(Event.description.like(query)).all()
        events = Event.query.filter(Event.name.like(query)).all()
        # quesry the Destination table and use the filter - like(similar to query)
        return render_template('index.html', events=events)
    return redirect(url_for('main.index'))

@bp.route('/searchGenre')
def searchGenre():
    if request.args['search'] and request.args['search'] != "":
        query = "%" + request.args['search'] + "%" # search is the name of the form in the html file
        events = Event.query.filter(Event.genre.like(query)).all()
        # add filter
        # quesry the Destination table and use the filter - like(similar to query)
        return render_template('index.html', events=events)
    return redirect(url_for('main.index'))
