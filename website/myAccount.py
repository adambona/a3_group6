from flask import Blueprint, render_template, request, redirect, url_for
from .models import Order
from .models import Event
from . import db
from flask_login import login_required, current_user

bp = Blueprint('myAccount', __name__)

@bp.route('/order-history')
@login_required
def orderHistory():

    result = (
    db.session.query(Event, Order)
    .join(Order, Event.id == Order.event_id)
    .filter(Event.id == Order.event_id, Order.booked_by == current_user.id)
    .all()
)
    # Add current user filter to results

    return render_template('order-history.html', result=result)

@bp.route('/my-events')
def myEvents():
    events = Event.query.filter(Event.user_id==current_user.id).all()
    return render_template('my-events.html', events=events)


@bp.route('/order-history/search')
def search():


    if request.args['search'] and request.args['search'] != "":
        query = "%" + request.args['search'] + "%" # search is the name of the form in the html file

        # Search order history
        result = (
        db.session.query(Event, Order)
        .join(Order, Event.id == Order.event_id)
        .filter(Event.id == Order.event_id, Order.booked_by == current_user.id, Event.name.like(query))
        .all()
        )


        # quesry the Destination table and use the filter - like(similar to query)
        return render_template('order-history.html', result=result)
    return redirect(url_for('order-history.html'))