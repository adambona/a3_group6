from flask_login import UserMixin
from . import db
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__='Users' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

class Event(db.Model):

    __tablename__ = 'Events'

    eventId = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'))
    genre = db.Column(db.String(80))
    name = db.Column(db.String(80))
    artistName = db.Column(db.String(80))
    status = db.Column(db.DateTime)
    startTime = db.Column(db.DateTime)
    location = db.Column(db.String(80))
    ticketPrice = db.Column(db.Float)
    numTickets = db.Column(db.Integer)
    description = db.Column(db.String)
    #image = db.column(db.File)

    def get_event(self):
        return str(self)

    def __repr__(self):
        str = "eventId: {0}\n userId: {1} \n genreId: {2} \n name: {3} \n artistName: {4} \n status: {5} \n startTime: {6} \n endTime: {7} \n location: {8} \n ticketPrice: {9} \n numTickets: {10} \n description {11} \n image {12}" 
        str =str.format( self.eventId, self.userId, self. genre, self.name, self.artistName, self.status, self.startTime, self.endTIme, self.location, self.ticketPrice, self.numTickets, self.description, self.image)
        return str