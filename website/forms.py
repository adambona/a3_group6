
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, SelectField, TimeField, IntegerField, DateField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from wtforms.validators import Email
from flask_wtf.file import FileRequired, FileField, FileAllowed
# ALLOWED_FILE = ['PNG','JPG','.png','jpg']

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
    event_id=IntegerField("Event ID") # was previously id("Event ID")
    user_id=IntegerField("User ID") #was previously id("User ID")
    genre=SelectField("Genre", choices=["Pop", "DanceEDM","Hiphop & Rap", "R&B","Latin","Rock", "Metal", "Country", "Folk/Acoustic", "Classical", "Jazz", "Blues", "Easy Listening", "New Age","World/Traditional Folk", "Others"])
    name=StringField("Event name", validators=[InputRequired()]) 
    artist_name=StringField("Artist name", validators=[InputRequired()]) 
    status=SelectField("Event status", choices=["Open", "Inactive", "Soldout", "Canceled"])
    event_date=DateField("Event date", validators=[InputRequired()])
    start_time=TimeField("Start time")
    end_time=TimeField("End time")
    location=StringField("Location/venue", validators=[InputRequired()]) 
    ticket_price=StringField("Price per ticket", validators=[InputRequired()]) 
    num_tickets=IntegerField("Total number of tickets available", validators=[InputRequired()]) 
    description=TextAreaField("Detailed Description of the Event", validators=[InputRequired()]) 
    # image=FileField("Thumbnail image for the event", validators=[FileRequired(), FileAllowed(ALLOWED_FILE)]) #File storage not supported temp comment
    image = StringField('Cover Image', validators=[InputRequired()])
    submit=SubmitField("Create Event")
    
#comment form 
class CommentForm(FlaskForm):
  text = TextAreaField('Comment', [InputRequired()])
  submit = SubmitField('Create')