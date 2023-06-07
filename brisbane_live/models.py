"""
models.py

This module contains the data models for the application.

The data models define the structure and behavior of the database tables
and represent the entities and relationships within the application's domain.

Classes:
- User: Represents a user in the system with attributes such as name, email, mobile number, password hash.
- Event: Represents a an event with attributes like name, status, artist names, genre, start time, end time, locations, description and image.
- Location: Represents a location for an event with attributes like physical address and venue name.
- PhysicalAddress: Represents a physical address with attributes like unit num, st num, st name, st suffix, postcode, city and state
- Genre: Represents a genre for an event with attributes like genre name.
- Artist: Represents an artist for an event with attributes like name.
- Comment: Represents a comment for an event with attributes like text, date posted.
- Ticket: Represents a ticket for an event with attributes like ticket number.  
- EventStatus: Represents the status of an event.
"""

from sqlalchemy import CheckConstraint
from datetime import datetime
from flask_login import UserMixin
from . import db
from enum import Enum

class EventStatus(Enum):
    """
    Enum representing the status of an event.

    The EventStatus enum defines different statuses that an event can have,
    such as 'OPEN', 'INACTIVE', 'SOLD_OUT'and 'CANCELLED'.

    Attributes:
        OPEN: Indicates that the event is scheduled some time in the future and there is available tickets for purchase.
        INACTIVE: Indicates that the event is in the past.
        SOLD_OUT: Indicates that the event has been sold out and there is no tickets available for purchase.
        CANCELLED: Indicates that the event has been cancelled and no tickets available for purchase.

    Example usage:
        status = EventStatus.SOLD_OUT
        if status == EventStatus.SOLD_OUT:
            print("The event is currently sold out. You can not purchase any tickets at the moment!")
    """
    OPEN = 'Open'
    INACTIVE = 'Inactive'
    SOLD_OUT = 'Sold Out'
    CANCELLED = 'Cancelled'


class Event(db.Model):
    """
    Event model representing a music event.

    Attributes:
        id (int): The unique identifier (PK) for the event.
        name (str): The name of the event.
        start_time (DateTime): The start time of the event.
        end_time (DateTime): The end/finish time of the event.
        description (str): The description of the event.
        image (str): The URL or path to the image of the event.
        user_id (int): The foregin key referencing the corresponding user's id.
        genre (int): The foregin key referencing the corresponding genre's id.
        location (int): The foregin key referencing the corresponding location's id.

    Relationships:
        artist_names (List[Artist]): The artists associated with the event.

    """
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(10), CheckConstraint("status IN ('Open', 'Inactive', 'Sold Out', 'Cancelled')"), nullable=False, index=True) #checks status is valid status
    start_time = db.Column(db.Time, nullable=False, index=True)
    end_time = db.Column(db.Time, nullable=False, index=True)
    description = db.Column(db.String(500), nullable=False, index=True)
    image = db.Column(db.String(400), nullable=False, index=True)
    ticket_price = db.Column(db.Float(2), CheckConstraint('ticket_price >= 0'), nullable=False, index=True)
    num_tickets = db.Column(db.Integer, CheckConstraint('num_tickets >= 0'), nullable=False, index=True)
    end_date = db.Column(db.Date, nullable=False, index=True)
    start_date = db.Column(db.Date, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    artist_names = db.Column(db.String(100), nullable=False, index=True)
    venue_name = db.Column(db.String(100), nullable=False, index=True)
    street_address = db.Column(db.String(100), nullable=False, index=True)

    comments = db.relationship('Comment', backref='events')
    # artist_names = db.relationship('Artist', backref='events')

class User(db.Model, UserMixin):
    """
    User model representing a user.

    Attributes:
        id (int): The unique identifier (PK) for a user.
        name (str): The name of the user.
        mobile_number (str): The mobile number of the user.
        email_address (str): The email address of the user.
        password_hash (str): The hashed password of the user.

    Relationships:
        comments (Comment): The comments associated with the user.
    """
    __tablename__='users' 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(36), index=True, unique=False, nullable=False)
    mobile_number = db.Column(db.String(15), index=True, nullable=False)
    email_address = db.Column(db.String(254), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    comments = db.relationship('Comment', backref='user')

    def __repr__(self):
        return 'User: %r' % self.username
    

class Comment(db.Model):
    """
    Comment model representing a comment on an event.

    Attributes:
        id (int): The unique identifier (PK) for a user.
        text (str): The text associated with the comment.
        date_posted (DateTime): The date the comment was posted. 
        user_id (int): The foregin key referencing the corresponding user's id.
        event_id (int): The foregin key referencing the corresponding event's id.
    """
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))


class Order(db.Model):
    """ Payment model representing the payment details of a user

    Attributes: 

    """
    __tablename__ = 'orders'

    order_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    pay_type = db.Column(db.String)
    card_number = db.Column(db.String) 
    expiration = db.Column(db.String)
    cvv = db.Column(db.String)
    num_tickets = db.Column(db.Integer)
    booked_by = db.Column(db.String)
    total_cost  = db.Column(db.Float(2))
    ordered_at = db.Column(db.DateTime, default=datetime.now, nullable=False)