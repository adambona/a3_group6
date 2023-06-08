from .forms import createEventForm, orderForm, CommentForm
from .models import Event, Order, Comment
from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from sqlalchemy.sql import func
from datetime import datetime

bp = Blueprint('createEvent', __name__)

@bp.route('/event/<int:id>', methods=['GET', 'POST'])
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
    cform = CommentForm()

    return render_template('event-details.html', event=event, form=form, remaining=tickets_remaining, cform=cform)

@bp.route('/event/<int:id>/checkout', methods=['GET', 'POST'])
def show_modal(id):

    event = db.session.scalar(db.select(Event).where(Event.id==id))
    open_modal = True

    # Sum of tickets sold for specific event
    tickets_sold = db.session.query(func.sum(Order.num_tickets)).filter(Order.event_id==id).scalar()
    total_tickets = db.session.query(Event.num_tickets).filter(Event.id==id).scalar()

    if tickets_sold is not None:
        tickets_remaining = total_tickets - tickets_sold
    else:
        tickets_remaining = total_tickets
    
    form = orderForm()
    cform = CommentForm() 

    if form.validate_on_submit():
        order = Order(event_id = id, booked_by = current_user.id, first_name = form.first_name.data, last_name = form.last_name.data,
        email = form.email.data, pay_type= form.pay_type.data, card_number= form.card_number.data, expiration=form.expiration.data, cvv= form.cvv.data, num_tickets= form.num_tickets.data, total_cost = form.num_tickets.data * event.ticket_price, ordered_at=datetime.now())

        if form.num_tickets.data > tickets_remaining :
            message = 'Order Cannot be placed - Not enough tickets remaining, there are - {} remaining'.format(tickets_remaining)
            flash(message, 'text-danger')
            return redirect(url_for('createEvent.show', id=id))

        if form.num_tickets.data == tickets_remaining:

            event.status = 'Sold Out'
            db.session.add(order)
            db.session.commit()
            order_no = order.order_id
            return redirect(url_for('createEvent.summary', id=id , order=order_no))

        else:
            
            db.session.add(order)
            db.session.commit()
            order_no = order.order_id
            return redirect(url_for('createEvent.summary', id=id , order=order_no))
        
    open_modal_checkout = False  # Default to not showing checkout modal

    if form.errors:  # Validation errors occurred
        open_modal_checkout = True  # Set flag to show checkout modal

    return render_template('event-details.html', event=event, form=form, remaining=tickets_remaining,
                           cform=cform, open_modal_checkout=open_modal_checkout, open_modal=open_modal)
    
@bp.route('/event/<int:id>/<int:order>', methods=['GET', 'POST'])
def summary(id, order):
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    order = db.session.scalar(db.select(Order).where(Order.order_id==order))
    open_modal = True




    return render_template('summary.html', event=event, open_modal=open_modal, order=order)


@bp.route('/createEvent', methods=['GET', 'POST'])
@login_required
def createEvent():
    form = createEventForm()

    if form.validate_on_submit():

        db_file_path = check_upload_file(form)

        event = Event(user_id=current_user.id, status = form.status.data, start_date=form.start_date.data, end_date=form.end_date.data, genre=form.genre.data, name=form.name.data, artist_names=form.artist_names.data, start_time=form.start_time.data, end_time=form.end_time.data,
                      ticket_price=form.ticket_price.data, num_tickets=form.num_tickets.data, description=form.description.data, image=db_file_path, venue_name=form.venue_name.data, street_address=form.street_address.data)

        db.session.add(event)
        db.session.commit()


        return redirect(url_for('main.index'))   


    return render_template('createEvent.html', form=form)

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

@bp.route('/event/<event>/comment', methods=['GET', 'POST'])
@login_required
def comment(event):
    form = CommentForm()
    
    event_obj = Event.query.filter_by(id=event).first()
    if form.validate_on_submit():
        
        comment = Comment(text=form.text.data,
                          events=event_obj,
                          user_id=current_user.name, date_posted=datetime.now()
                          )
        db.session.add(comment)
        db.session.commit()

        
    return redirect(url_for('createEvent.show', id=event))


@bp.route('/updateEvent/<int:id>', methods=['GET', 'POST'])
@login_required
def updateEvent(id):

    events = Event.query.filter(Event.id==id).first()
    form = createEventForm()

    if current_user.id == events.user_id:
    
        if form.validate_on_submit():
            update_event = Event.query.filter(Event.id==id).first()

            # Update Image
            db_file_path = check_upload_file(form)



            update_event.name = form.name.data
            update_event.status = form.status.data
            update_event.start_time = form.start_time.data
            update_event.end_time = form.end_time.data
            update_event.end_date = form.end_date.data
            update_event.start_date = form.start_date.data
            update_event.description = form.description.data
            update_event.ticket_price = form.ticket_price.data
            update_event.venue_name = form.venue_name.data
            update_event.street_address = form.street_address.data
            update_event.genre = form.genre.data
            update_event.image = db_file_path


            # Appends tickets
            update_event.num_tickets += form.num_tickets.data
            

            db.session.commit()

            return redirect(url_for('createEvent.show', id=id))

    else:
        flash('You cannot update an event you are not the owner of please create your own event below', 'text-danger')
        return redirect(url_for('createEvent.createEvent'))

    return render_template('update-event.html', form=form, event=events)