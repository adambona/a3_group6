from .forms import createEventForm
from .models import Event
from flask import Blueprint, render_template, request, redirect, url_for
from . import db
import os
from werkzeug.utils import secure_filename

bp = Blueprint('createEvent', __name__)

@bp.route('/createEvent', methods=['GET', 'POST'])
def createEvent():
    form = createEventForm()
    if form.validate_on_submit():
        db_file_path = check_upload_file(form)
        event = Event(genre=form.genre.data, name=form.name.data, artistName=form.artistName.data, startTime=form.startTime.data, endTime=form.endTime.data, location=form.location.data, ticketPrice=form.ticketPrice.data, numTickets=form.numTickets.data, description=form.description.data, image=form.image.data)

        db.session.add(Event)
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
