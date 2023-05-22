
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, SelectField, TimeField, IntegerField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from wtforms.validators import Email
from flask_wtf.file import FileRequired, FileField, FileAllowed
ALLOWED_FILE = ['PNG','JPG','png','jpg']

#creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email()])
    #linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    #submit button
    submit = SubmitField("Register")

class createEventForm(FlaskForm):
    eventId=IntegerField("Event ID") # was previously id("Event ID")
    userId=IntegerField("User ID") #was previously id("User ID")
    genre=SelectField("Genre", choices=["Pop", "DanceEDM","Hiphop & Rap", "R&B","Latin","Rock", "Metal", "Country", "Folk/Acoustic", "Classical", "Jazz", "Blues", "Easy Listening", "New Age","World/Traditional Folk", "Others"])
    name=StringField("Event name", validators=[InputRequired()]) 
    artistName=StringField("Artist name", validators=[InputRequired()]) 
    status=SelectField("Event status", choices=["Open", "Inactive", "Soldout", "Canceled"]) 
    startTime=TimeField("Start time") 
    endTime=TimeField("End time") 
    location=StringField("Location/venue", validators=[InputRequired()]) 
    ticketPrice=StringField("Price per ticket", validators=[InputRequired()]) 
    numTickets=IntegerField("Total number of tickets available", validators=[InputRequired()]) 
    description=StringField("Detailed Description of the Event", validators=[InputRequired()]) 
    image=FileField("Thumbnail image for the event", validators=[FileRequired(), FileAllowed(ALLOWED_FILE)]) #Cant iterate over FileAllowed fields
    #image=FileField("Thumbnail image for the event")
    submit=SubmitField("Create Event")