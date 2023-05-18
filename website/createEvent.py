from .forms import createEventForm
from flask import Blueprint, render_template, request, redirect, url_for

bp = Blueprint('createEvent', __name__, url_prefix='/create-event')

@bp.route('/create-event')
def createEvent():
    return render_template('create-event.html')

@bp.route('/create-event', methods = ['GET', 'POST'])
def addEvent():
  print('Method type: ', request.method)
  form = createEventForm()
  if form.validate_on_submit():
    print('Successfully created new event', 'success')
  return render_template('index.html')
