from forms import createEventForm
from flask import Blueprint, render_template, request, redirect, url_for


bp = Blueprint('createEvent', __name__, url_prefix='/createEvent')

@bp.route('/')
def createEvent():
    return render_template('create-event.html')

@bp.route('/createEvent', methods = ['GET', 'POST'])
def createEvent():
  print('Method type: ', request.method)
  form = createEventForm()
  if form.validate_on_submit():
    print('Successfully created new event', 'success')
  return render_template('index.html')
