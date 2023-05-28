
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, SelectField, TimeField, IntegerField, DateField, RadioField, BooleanField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from wtforms.validators import Email
from flask_wtf.file import FileRequired, FileField, FileAllowed
ALLOWED_FILE = ['PNG','JPG','png','jpg', 'jpeg', 'JPEG']

#creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email()])
    mobile_number = StringField("Mobile Number", validators=[InputRequired()])
    #linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    #submit button
    submit = SubmitField("Register")

class createEventForm(FlaskForm):
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
    image=FileField("Thumbnail image for the event", validators=[FileRequired(), FileAllowed(ALLOWED_FILE)])
    submit=SubmitField("Create Event")
    
class paymentEventForm(FlaskForm):
    first_name=StringField("First name", validators=[InputRequired()])
    last_name=StringField("Last name", validators=[InputRequired()])
    email=StringField("Email address", validators=[InputRequired()])
    pay_type=RadioField("Select payment type", choices=[('Credit Card'), ('Debit Card'), ('PayPal')], validators=[InputRequired()])
    card_number=StringField("Card number", validators=[InputRequired()])
    expiration=StringField('Expiration', validators=[InputRequired()])
    cvv=StringField("CVV", validators=[InputRequired()])
    confirm=BooleanField("Brisbane Live Terms of Service", validators=[InputRequired()])
    confirm2=BooleanField("I confirm my details are correct", validators=[InputRequired()])
    submit=SubmitField('Process Payment')