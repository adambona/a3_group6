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

from flask_login import UserMixin
from . import db
from datetime import datetime
from enum import Enum
from sqlalchemy import CheckConstraint

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
    name = db.Column(db.String(56), nullable=False)
    status = db.Column(db.String(10), CheckConstraint("status IN ('Open', 'Inactive', 'Sold Out', 'Cancelled')"), nullable=False, index=True) #checks status is valid status
    start_time = db.Column(db.DateTime, nullable=False, index=True)
    end_time = db.Column(db.DateTime, nullable=False, index=True)
    description = db.Column(db.String(500), nullable=False, index=True)
    image = db.Column(db.String(400), nullable=False, index=True)
    ticket_price = db.Column(db.Float(2), CheckConstraint('ticket_price >= 0'), nullable=False, index=True)
    num_tickets = db.Column(db.Integer, CheckConstraint('num_tickets >= 0'), nullable=False, index=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    genre = db.Column(db.Integer, db.ForeignKey('genres.id'))
    location = db.Column(db.Integer, db.ForeignKey('locations.id'))

    artist_names = db.relationship('Artist', backref='events')

    def __init__(self, eventId, userId, genre, name, Artist, status, startTime, endTime, location, ticketPrice, numTickets, description, image):
        self.eventId = eventId
        self.userId = userId
        self.genre = genre
        self.name = name
        self.Artist = Artist
        self.status = status
        self.startTime = startTime
        self.endTime = endTime
        self.location = location
        self.ticketPrice = ticketPrice
        self.numTickets = numTickets
        self.description = description
        self.image = image
        
# class User(db.Model, UserMixin):
#     __tablename__='Users' 
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), index=True, unique=True, nullable=False)
#     emailid = db.Column(db.String(100), index=True, nullable=False)
#     password_hash = db.Column(db.String(255), nullable=False)

# class Event(db.Model):

#     __tablename__ = 'Events'

#     eventId = db.Column(db.Integer, primary_key=True)
#     userId = db.Column(db.Integer, db.ForeignKey('users.id'))
#     genre = db.Column(db.String(80))
#     name = db.Column(db.String(80))
#     artistName = db.Column(db.String(80))
#     status = db.Column(db.DateTime)
#     startTime = db.Column(db.DateTime)
#     location = db.Column(db.String(80))
#     ticketPrice = db.Column(db.Float)
#     numTickets = db.Column(db.Integer)
#     description = db.Column(db.String)
#     #image = db.column(db.File)

#     def get_event(self):
#         return str(self)

#     def __repr__(self):
#         str = "eventId: {0}\n userId: {1} \n genreId: {2} \n name: {3} \n Artist: {4} \n status: {5} \n startTime: {6} \n endTime: {7} \n location: {8} \n ticketPrice: {9} \n numTickets: {10} \n description {11} \n image {12}" 
#         str =str.format( self.eventId, self.userId, self. genre, self.name, self.Artist, self.status, self.startTime, self.endTIme, self.location, self.ticketPrice, self.numTickets, self.description, self.image)
#         return str
    
    
class Location(db.Model):
    """
    location model representing a location for a music event.

    Attributes:
        id (int): The unique identifier (PK) for the location.
        venue_name (str): The venue name of for the location.
        physical_address_id (int): The foregin key referencing the corresponding physical_addresses's id.

    Relationships:
        physical_address (PhysicalAddress): The physical address associated with the location.
    """
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    venue_name = db.Column(db.String(100), nullable=False, index=True)
    physical_address_id = db.Column(db.Integer, db.ForeignKey('physical_addresses.id'))
    physical_address = db.relationship('PhysicalAddress', backref='locations')

    def __repr__(self):
        return f"Location: venue_name='{self.venue_name}', address={self.physical_address}'"


class Genre(db.Model):
    """
    genre model representing a genre for a music event.

    Attributes:
        id (int): The unique identifier (PK) for the genre.
        genre_name (str): The name of the genre.
    """
    __tablename__ = 'genres'

    id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String(100), nullable=False, index=True)

    def __repr__(self):
        return f"Genre: '{self.genre_name}'"


class PhysicalAddress(db.Model):
    """
    physical address model representing a physical address.

    Attributes:
        id (int): The unique identifier (PK) for the address.
        unit_num (int): The unit number for an address.
        street_num (int): The street number for an address.
        street_name (str): The street name for an address.
        street_suffix (str): The street suffix for an address.
        city (str): The city for an address.
        postcode (int): The postcode for an address.
        state (str): The state for an address.
    """
    MIN_POSTCODE = 1000
    MAX_POSTCODE = 9999

    __tablename__ = 'physical_addresses'

    id = db.Column(db.Integer, primary_key=True)
    unit_num = db.Column(db.Integer, nullable=True)
    street_num = db.Column(db.Integer, nullable=False)
    street_name = db.Column(db.String(100), nullable=False, index=True)
    street_suffix = db.Column(db.String(10), nullable=False, index=True)
    city = db.Column(db.String(100), nullable=False, index=True)
    postcode = db.Column(db.Integer, CheckConstraint(f'postcode >= {MIN_POSTCODE} AND postcode <= {MAX_POSTCODE}'), nullable=False, index=True)
    state = db.Column(db.String(20), CheckConstraint("state IN ('QLD')"), nullable=False, index=True)
    
    
    def __repr__(self):
        return f"PhysicalAddress: (Unit number:'{self.unit_num}', Street number:'{self.street_num}', Street name:'{self.street_name}', Street suffix:'{self.street_suffix}', City:'{self.city}', Postcode:'{self.postcode}', State:'{self.state}')"


class Artist(db.Model):
    """
    artist model representing an artist.

    Attributes:
        id (int): The unique identifier (PK) for the artist.
        event_id (int): The foregin key referencing the corresponding event's id.
        name (str): The artist's name.
    """
    __tablename__ = 'artist_names'

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False, index=True)

    def __repr__(self):
        return 'Artist Name: %r' % self.name

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
    name = db.Column(db.String(36), index=True, unique=True, nullable=False)
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
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))

    def __repr__(self):
        return "Comment: {}".format(self.text)
    

class Ticket(db.Model):
    """
    Ticket model representing a ticket for an event.

    Attributes:
        id (int): The unique identifier (PK) for a ticket.
        user_id (int): The foregin key referencing the corresponding user's id.
        event_id (int): The foregin key referencing the corresponding event's id.
    """
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))

    def __repr__(self):
        return "Ticket: {}".format(self.id)