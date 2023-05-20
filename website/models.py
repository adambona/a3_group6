from flask_login import UserMixin
from . import db
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__='Users' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
class Event:

    def __init__(self, eventId, userId, genre, name, artistName, status, startTime, endTime, location, ticketPrice, numTickets, description, image):
        self.eventId = eventId
        self.userId = userId
        self.genre = genre
        self.name = name
        self.artistName = artistName
        self.status = status
        self.startTime = startTime
        self.endTIme = endTime
        self.location = location
        self.ticketPrice = ticketPrice
        self.numTickets = numTickets
        self.description = description
        self.image = image

    
    def get_event(self):
        return str(self)

    def __repr__(self):
        str = "eventId: {0}\n userId: {1} \n genreId: {2} \n name: {3} \n artistName: {4} \n status: {5} \n startTime: {6} \n endTime: {7} \n location: {8} \n ticketPrice: {9} \n numTickets: {10} \n description {11} \n image {12}" 
        str =str.format( self.eventId, self.userId, self. genre, self.name, self.artistName, self.status, self.startTime, self.endTIme, self.location, self.ticketPrice, self.numTickets, self.description, self.image)
        return str