from .forms import createEventForm, orderForm
from .models import Event, Order, Artist
from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from sqlalchemy.sql import func

bp = Blueprint('createEvent', __name__)

@bp.route('/<int:id>', methods=['GET', 'POST'])
def show(id):
    
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    

    # Sum of tickets sold for specific event
    tickets_sold = db.session.query(func.sum(Order.num_tickets)).filter(Order.event_id==id).scalar()
    total_tickets = db.session.query(Event.num_tickets).filter(Event.id==id).scalar()

    if tickets_sold is not None:
        tickets_remaining = total_tickets - tickets_sold
    else:
        tickets_remaining = total_tickets

    form = orderForm()
    
    if form.validate_on_submit():
        order = Order(event_id = id, booked_by = current_user.id, first_name = form.first_name.data, last_name = form.last_name.data,
        email = form.email.data, pay_type= form.pay_type.data, card_number= form.card_number.data, expiration=form.expiration.data, cvv= form.cvv.data, num_tickets= form.num_tickets.data, total_cost = form.num_tickets.data * event.ticket_price)

        if form.num_tickets.data > tickets_remaining :
            flash('Number of Tickets Exceeded amount remaining')
            return redirect(url_for('createEvent.show', id=id))


        
        else:
            db.session.add(order)
            db.session.commit()
            flash('Tickets Purchased Succesfully')
            return redirect(url_for('createEvent.show', id=id))

# Remove remaining tickets ?
    return render_template('event-details.html', event=event, form=form, remaining=tickets_remaining)


@bp.route('/createEvent', methods=['GET', 'POST'])
@login_required
def createEvent():
    form = createEventForm()

    if form.validate_on_submit():
        db_file_path = check_upload_file(form)
        artist_list = []
        
        artist = Artist(event_id = 0, name = form.artist_names.data)
        db.session.add(artist) 
        artist_list.append(artist)

        event = Event(user_id=current_user.id, status = form.status.data, event_date=form.event_date.data, genre=form.genre.data, name=form.name.data, artist_names=artist_list, start_time=form.start_time.data, end_time=form.end_time.data, location=form.location.data, ticket_price=form.ticket_price.data, num_tickets=form.num_tickets.data, description=form.description.data, image=db_file_path)
        
        for artist in artist_list:
            artist.event_id = event.id

        db.session.add(event)
        db.session.commit()
        return redirect(url_for('createEvent.createEvent'))

    return render_template('createEvent.html', form=form)

@bp.route('/updateStatus<id>/<status>')
def updateStatusInactive(id, status):
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    if status == 'open':
        event.status = 'Open'
    if status == 'inactive':
        event.status = 'Inactive'
    if status == 'soldout':
        event.status = 'Sold Out'
    if status == 'cancelled':
        event.status = 'Cancelled'

    db.session.commit()

    events = Event.query.all()
    return render_template('my-events.html', events=events)


def check_upload_file(form):
  #get file data from form  
  fp = form.image.data
  filename = fp.filename
  #get the current path of the module file… store image file relative to this path  
  BASE_PATH = os.path.dirname(__file__)
  #upload file location – directory of this file/static/image
  upload_path = os.path.join(BASE_PATH,'static/image',secure_filename(filename))
  #store relative path in DB as image location in HTML is relative
  db_upload_path = '/static/image/' + secure_filename(filename)
  #save the file and return the db upload path  
  fp.save(upload_path)
  return db_upload_path
