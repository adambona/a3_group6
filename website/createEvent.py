from .forms import createEventForm, CommentForm
from .models import Event, Comment
from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

#bp = Blueprint('createEvent', __name__)
bp = Blueprint('createEvent', __name__, url_prefix='/event')

@bp.route('/<id>')
def show(id):
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    # create the comment form
    cform = CommentForm()    
    return render_template('event-details.html', event=event, form=cform)

@bp.route('/createEvent', methods=['GET', 'POST'])
def createEvent():
    form = createEventForm()
    if form.validate_on_submit():
        # db_file_path = check_upload_file(form)
        event = Event(event_id = form.event_id.data, user_id=form.user_id.data, status = form.status.data, event_date=form.event_date.data, genre=form.genre.data, name=form.name.data, artist_name=form.artist_name.data, start_time=form.start_time.data, end_time=form.end_time.data, location=form.location.data, ticket_price=form.ticket_price.data, num_tickets=form.num_tickets.data, description=form.description.data, image=form.image.data)

        db.session.add(event)
        db.session.commit()

        print('Successfully created new event', 'success')
        return redirect(url_for('createEvent.createEvent'))
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

@bp.route('/<event>/comment', methods=['GET', 'POST'])
#@login_required
def comment(event):
    form = CommentForm()
    # get the destination object associated to the page and the comment
    event_obj = Event.query.filter_by(id=event).first()
    if form.validate_on_submit():
        # read the comment from the form
        comment = Comment(text=form.text.data,
                          events=event_obj,
                          #user=current_user
                          )
        db.session.add(comment)
        db.session.commit()

        # flashing a message which needs to be handled by the html
        flash('Your comment has been added', 'success')
        print('Your comment has been added', 'success')
    return redirect(url_for('createEvent.show', id=event))