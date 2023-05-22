from flask import Blueprint, render_template, request, redirect, url_for
from .models import Order
from . import db

bp = Blueprint('myAccount', __name__)

@bp.route('/order-history')
def orderHistory():
    # new_order = Order(1,1,66.66) Create a new order for testing
    # db.session.add(new_order)
    # db.session.commit()
    orders = Order.query.all()
    return render_template('order-history.html', orders=orders)
