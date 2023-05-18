
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, SelectField, TimeField, IntegerField, FileField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from wtforms.validators import Email


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
    eventId=id("Event ID")
    userId=id("User ID")
    genre=SelectField("Genre", choices=["Pop", "DanceEDM","Hiphop & Rap", "R&B","Latin","Rock", "Metal", "Country", "Folk/Acoustic", "Classical", "Jazz", "Blues", "Easy Listening", "New Age","World/Traditional Folk", "Others"])
    name=StringField("Event Name", validators=[InputRequired()]) 
    artistName=StringField("Artist Name", validators=[InputRequired()]) 
    status=SelectField("Event Status", choices=["Open", "Inactive", "Soldout", "Canceled"]) 
    startTime=TimeField("Start Time") 
    endTime=TimeField("End Time") 
    location=StringField("Location/Venue", validators=[InputRequired()]) 
    ticketPrice=StringField("Price per Ticket", validators=[InputRequired()]) 
    numTickets=IntegerField("Total Number of Tickets Available", validators=[InputRequired()]) 
    description=StringField("Detailed Description of the Event", validators=[InputRequired()]) 
    image=FileField("Thumbnail Image for the Event")

    submit=SubmitField("Create Event")