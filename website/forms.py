
from flask_wtf import FlaskForm, Form
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, SelectField, TimeField, IntegerField, DateField, RadioField, BooleanField, FormField, FieldList
from wtforms.validators import InputRequired, Length, Email, EqualTo, NumberRange, Regexp, ValidationError

from flask_wtf.file import FileRequired, FileField, FileAllowed
ALLOWED_FILE = ['PNG','JPG','png','jpg', 'jpeg', 'JPEG']
PASSWORD_REGEX="^.*(?=.{8,})(?=.*\\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z\\d\\s:]).*$"
PASSWORD_ERROR_MESSAGE="Password must be a text string of arbitrary length, at least 8 non-white-space characters which must contain at least one uppercase letter, one lowercase letter, one digit, one non-alphanumeric character (e.g., !@#$%^&*)"
MOBILE_NUM_REGEX = "^(\+?61|0)[2-478](?:[ -]?[0-9]){8}$"
MOBILE_ERROR_MESSAGE="Mobile number must be a valid Australian mobile number. It must be in the form of 04XXXXXXXX or +61XXXXXXXXX."

#custom length validator
def validate_length(min=-1,max=-1, min_error_message="Field length too short", max_error_message="Field length too long"):
  def _validate_length(form, field):
    if len(field.data) < min :
        raise ValidationError(min_error_message) 
    elif len(field.data) > max:
        raise ValidationError(max_error_message)   
  return _validate_length   


#creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Please enter a user name')])
    password=PasswordField("Password", validators=[InputRequired('Please enter a password')])
    submit = SubmitField("Login")

  
 # this is the registration form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired("Please enter a user name"), validate_length(min=1, max=36, min_error_message='User name must be atleast 1 character',max_error_message='User name must be 36 characters or less')])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email"), Length(min=1,max=254), InputRequired()])
    mobile_number = StringField("Mobile Number", validators=[InputRequired("Please enter a mobile number"), Regexp(MOBILE_NUM_REGEX, message=MOBILE_ERROR_MESSAGE)])
    #linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match"), Regexp(PASSWORD_REGEX, message=PASSWORD_ERROR_MESSAGE)])
    confirm = PasswordField("Confirm Password")

    #submit button
    submit = SubmitField("Register")


class createEventForm(FlaskForm):
    genre=SelectField("Genre", choices=["Pop", "DanceEDM","Hiphop & Rap", "R&B","Latin","Rock", "Metal", "Country", "Folk/Acoustic", "Classical", "Jazz", "Blues", "Easy Listening", "New Age","World/Traditional Folk", "Others"])
    name=StringField("Event name", validators=[InputRequired()]) 
    artist_names=StringField("Artists", validators=[InputRequired()])
    status=SelectField("Event status", choices=["Open", "Inactive", "Sold Out", "Cancelled"])
    event_date=DateField("Event date", validators=[InputRequired()])
    start_time=TimeField("Start time")
    end_time=TimeField("End time")
    location=StringField("Location/venue", validators=[InputRequired()]) 
    ticket_price=StringField("Price per ticket", validators=[InputRequired()]) 
    num_tickets=IntegerField("Total number of tickets available", validators=[InputRequired()]) 
    description=TextAreaField("Detailed Description of the Event", validators=[InputRequired()]) 
    image=FileField("Thumbnail image for the event", validators=[FileRequired(), FileAllowed(ALLOWED_FILE)])
    submit=SubmitField("Create Event")
    
    
class orderForm(FlaskForm):
    num_tickets=IntegerField("Number of tickets", validators=[InputRequired(), NumberRange(min=1,max=5)])
    first_name=StringField("First name", validators=[InputRequired(), Length(min=1,max=20)])
    last_name=StringField("Last name", validators=[InputRequired(), Length(min=1,max=20)])
    email=StringField("Email address", validators=[InputRequired(), Email()])
    pay_type=RadioField("Select payment type", choices=[('Credit Card'), ('Debit Card'), ('PayPal')], validators=[InputRequired()])
    card_number=StringField("Card number", validators=[InputRequired(), Regexp('^\\d{16}$', message='Must contain 16 digits only'), Length(min=16, max=16)])
    expiration=StringField('Expiration', validators=[InputRequired(), Regexp('^(0[1-9]|1[0-2])\/(0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]|6[0-9]|7[0-9]|8[0-9]|9[0-9])$', message='Example: Febuary 2023 = 02/23')])
    cvv=StringField("CVV", validators=[InputRequired(), Regexp('^\\d{3}$', message='Must contain 3 digits only'), Length(min=3,max=3)])
    confirm=BooleanField("Brisbane Live Terms of Service", validators=[InputRequired()])
    confirm2=BooleanField("I confirm my details are correct", validators=[InputRequired()])
    submit=SubmitField('Process Payment')
