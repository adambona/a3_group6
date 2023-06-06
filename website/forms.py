
from flask_wtf import FlaskForm, Form
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, SelectField, TimeField, IntegerField, DateField, RadioField, BooleanField, FormField, FieldList
from datetime import datetime, date
from wtforms.validators import InputRequired, Length, Email, EqualTo, NumberRange, Regexp, ValidationError
from .models import User
from flask_wtf.file import FileRequired, FileField, FileAllowed
from flask import url_for, Markup
from werkzeug.security import check_password_hash

ALLOWED_FILE = ['PNG','JPG','png','jpg', 'jpeg', 'JPEG']

PASSWORD_REGEX="^.*(?=.{8,})(?=.*\\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z\\d\\s:]).*$"
PASSWORD_ERROR_MESSAGE="Password must be a text string of arbitrary length, at least 8 non-white-space characters which must contain at least one uppercase letter, one lowercase letter, one digit, one non-alphanumeric character (e.g., !@#$%^&*)"

MOBILE_NUM_REGEX = "^(\+?61|0)[2-478](?:[ -]?[0-9]){8}$"
MOBILE_ERROR_MESSAGE="Mobile number must be a valid Australian mobile number. It must be in the form of 04XXXXXXXX or +61XXXXXXXXX (You can use spaces or hypens to seperate the digits eg. 04XX XXX XXX +61XX-XXX-XXX)."

#custom length validator
def validate_length(min=-1,max=-1, min_error_message="Field length too short", max_error_message="Field length too long"):
  def _validate_length(form, field):
    if len(field.data) < min :
        raise ValidationError(min_error_message) 
    elif len(field.data) > max:
        raise ValidationError(max_error_message)   
  return _validate_length   

#checks to see if email already in use
def validate_unique_email(form, field):
    email = field.data
    if email_exists(email) is not None:
        url = url_for('auth.login')
        message = 'This email address is already in use. Please use a different email address or log in with your existing account <a href="' + url + '">here.</a>'
        raise ValidationError(Markup(message))

#query database for email
def email_exists(email):
    u1 = User.query.filter_by(email_address=email).first()
    return u1

#creates the login information
class LoginForm(FlaskForm):
    email_id = StringField("Email Address", validators=[Email(message="Please enter a valid email address."), Length(min=1,max=254), InputRequired(message="Please enter an email address.")])
    #email_id=StringField("User Name", validators=[InputRequired(message='Please enter a user name.')])
    password=PasswordField("Password", validators=[InputRequired(message='Please enter a password.')])
    submit = SubmitField("Login")

    def validate_email_id(self, field):
        # Custom email validation logic
        email = field.data
        user = User.query.filter_by(email_address=email).first()

        if user is None:
            raise ValidationError('There is no matching email address in our system. Please try again.')

    def validate_password(self, field):
        # Custom password validation logic
        password = field.data
        user = User.query.filter_by(email_address=self.email_id.data).first()

        if user is not None and not check_password_hash(user.password_hash, password):
            raise ValidationError('There is no matching password in our system. Please try again.')
  
 # this is the registration form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired(message="Please enter a user name."), validate_length(min=1, max=36, min_error_message='User name must be at least 1 character.',max_error_message='User name must be 36 characters or less.')])
    email_id = StringField("Email Address", validators=[Email(message="Please enter a valid email address."), Length(min=1,max=254), InputRequired(message="Please enter an email address."), validate_unique_email])
    mobile_number = StringField("Mobile Number", validators=[InputRequired(message="Please enter a mobile number."), Regexp(MOBILE_NUM_REGEX, message=MOBILE_ERROR_MESSAGE)])
    #linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(message="Please enter a password."),
                  EqualTo('confirm', message="Passwords do not match. Please Try again."), Regexp(PASSWORD_REGEX, message=PASSWORD_ERROR_MESSAGE), Length(max=254, message="Password must be 254 characters or less.")])
    confirm = PasswordField("Confirm Password", validators=[InputRequired(message="Please confirm your password.")])

    #submit button
    submit = SubmitField("Register")

class createEventForm(FlaskForm):
    genre = SelectField("Genre", choices=[
        ("Pop", "Pop"),
        ("DanceEDM", "Dance/EDM"),
        ("Hiphop & Rap", "Hip-hop & Rap"),
        ("R&B", "R&B"),
        ("Latin", "Latin"),
        ("Rock", "Rock"),
        ("Metal", "Metal"),
        ("Country", "Country"),
        ("Folk/Acoustic", "Folk/Acoustic"),
        ("Classical", "Classical"),
        ("Jazz", "Jazz"),
        ("Blues", "Blues"),
        ("Easy Listening", "Easy Listening"),
        ("New Age", "New Age"),
        ("World/Traditional Folk", "World/Traditional Folk"),
        ("Others", "Others")
    ])

    name = StringField("Event Name", validators=[InputRequired()])
    artist_names = StringField("Artists", validators=[InputRequired()])

    description = TextAreaField("Detailed Description of the Event", validators=[
        InputRequired("You must enter a description and it must be at least 6 characters"),
        validate_length(min=6, max=500, min_error_message="Description must be 6 characters or greater",
                        max_error_message="Description must be 500 characters or less")
    ])

    image = FileField("Thumbnail Image for the Event", validators=[
        FileRequired(),
        FileAllowed(ALLOWED_FILE)
    ])

    venue_name = StringField("Venue Name", validators=[InputRequired()])
    street_address = StringField("Street Address", validators=[InputRequired()])

    start_date = DateField("Event Starts", validators=[InputRequired()])
    end_date = DateField("Event Ends", validators=[InputRequired()])
    start_time = TimeField("Start Time",
                           description="Let people know when the event starts and ends so they can make sure to attend.")
    end_time = TimeField("End Time")

    ticket_price = StringField("Price per Ticket", validators=[InputRequired()])
    num_tickets = IntegerField("Total Number of Tickets Available", validators=[InputRequired()])

    status = SelectField("Event Status", choices=[
        ("Open", "Open"),
        ("Inactive", "Inactive"),
        ("Sold Out", "Sold Out"),
        ("Cancelled", "Cancelled")
    ])

    submit=SubmitField("Create Event")

    def validate_event_date(self, event_date):
        if event_date.data < date.today():
            raise ValidationError('Date must be in the future')

    
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

class CommentForm(FlaskForm):
  text = TextAreaField('Comment', [InputRequired(), Length(min=6, max=500)])
  submit = SubmitField('Create')

class updateForm(FlaskForm):
    
    status = SelectField("Event Status", choices=[
        ("Open", "Open"),
        ("Inactive", "Inactive"),
        ("Sold Out", "Sold Out"),
        ("Cancelled", "Cancelled")
    ])


    submit = SubmitField('update')