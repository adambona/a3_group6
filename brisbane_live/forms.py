from flask_wtf import FlaskForm, Form
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, SelectField, TimeField, IntegerField, DateField, RadioField, BooleanField, FormField, FieldList, FloatField
from datetime import datetime, date
from wtforms.validators import InputRequired, Length, Email, EqualTo, NumberRange, Regexp, ValidationError
from .models import User
from flask_wtf.file import FileRequired, FileField, FileAllowed
from flask import url_for, Markup
from werkzeug.security import check_password_hash
from datetime import timedelta
import re

ALLOWED_FILE = ['PNG','JPG','png','jpg', 'jpeg', 'JPEG']

PASSWORD_REGEX="^.*(?=.{8,})(?=.*\\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z\\d\\s:]).*$"
PASSWORD_ERROR_MESSAGE="Password must be a text string of arbitrary length, at least 8 non-white-space characters which must contain at least one uppercase letter, one lowercase letter, one digit, one non-alphanumeric character (e.g., !@#$%^&*)"

MOBILE_NUM_REGEX = "^(\+?61|0)[2-478](?:[ -]?[0-9]){8}$"
MOBILE_ERROR_MESSAGE="Mobile number must be a valid Australian mobile number. It must be in the form of 04XXXXXXXX or +61XXXXXXXXX (You can use spaces or hypens to seperate the digits eg. 04XX XXX XXX +61XX-XXX-XXX)."

#custom length validator
def validate_length(min=-1,max=-1, min_error_message="Field length too short", max_error_message="Field length too long"):
  def _validate_length(form, field):
    if len(field.data.strip()) < min :
        raise ValidationError(min_error_message) 
    elif len(field.data.strip()) > max:
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
    email_id = StringField("Email Address", validators=[Email(message="Please enter a valid email address."), Length(min=1,max=254), InputRequired(message="Please enter an email address.")], filters=[lambda x: x.strip() if x else None])
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
    user_name = StringField("User Name", validators=[InputRequired(message="Please enter a user name."), validate_length(min=1, max=36, min_error_message='User name must be at least 1 character.', max_error_message='User name must be 36 characters or less.')], filters=[lambda x: x.strip() if x else None])
    email_id = StringField("Email Address", validators=[Email(message="Please enter a valid email address."), Length(min=1,max=254), InputRequired(message="Please enter an email address."), validate_unique_email], filters=[lambda x: x.strip() if x else None])
    mobile_number = StringField("Mobile Number", validators=[InputRequired(message="Please enter a mobile number."), Regexp(MOBILE_NUM_REGEX, message=MOBILE_ERROR_MESSAGE)], filters=[lambda x: x.strip() if x else None])
    #linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password", validators=[InputRequired(message="Please enter a password."),
                  EqualTo('confirm', message="Passwords do not match. Please Try again."), Regexp(PASSWORD_REGEX, message=PASSWORD_ERROR_MESSAGE), Length(max=254, message="Password must be 254 characters or less.")], filters=[lambda x: x.strip() if x else None])
    confirm = PasswordField("Confirm Password", validators=[InputRequired(message="Please confirm your password.")], filters=[lambda x: x.strip() if x else None])
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
    ])

    name = StringField("Event Name", validators=[InputRequired(message="Please enter a name for the event"), validate_length(min=2, max=100, min_error_message='Event name must be 2 characters or greater', max_error_message='Event name must be 100 characters or less')], filters=[lambda x: x.strip() if x else None])
    artist_names = StringField("Artists", validators=[InputRequired(message="Please enter the artist/s name")], filters=[lambda x: x.strip() if x else None])

    description = TextAreaField("Detailed Description of the Event", validators=[
        InputRequired(message="Please enter a description for the event."),
        validate_length(min=6, max=500, min_error_message="Description must be 6 characters or greater.",
                        max_error_message="Description must be 500 characters or less.")
    ], filters=[lambda x: x.strip() if x else None])

    image = FileField("Thumbnail Image for the Event", validators=[
        FileRequired("Please upload an image for the event."),
        FileAllowed(ALLOWED_FILE, message="File type must be either PNG or JPG")
    ])

    venue_name = StringField("Venue Name", validators=[InputRequired(message="Please enter a venue name."), validate_length(min=1, max=100, min_error_message='Venue name must be at least 1 character.',max_error_message='Venue name must be 100 characters or less.')], filters=[lambda x: x.strip() if x else None])
    street_address = StringField("Street Address", validators=[InputRequired(message="Please enter a street address."), Regexp('\A\s*(\d+)(?:[\s,-]+([a-zA-Z\s]+?)(?:[\s,-]+(Alley|Ally|Arcade|Arc|Bypass|Bypa|Close|Cl|Corner|Crn|Cul-de-sac|Cds|Green|Grn|Esplanade|Esp|Grove|Gr|Junction|Jnc|Lane|Link|Street|St|Road|Rd|Avenue|Ave|Lane|Ln|Rigge|Rdge|Boulevard|Blvd|Drive|Dr|Court|Ct|Place|Pl|Terrace|Tce|Crescent|Cres|Highway|Hwy|Parade|Pde|Square|Sq|Circuit|Cct))?)?(?:[\s,-]+(Unit|Apt|Suite)\s+(\d+))?\s*,\s*([a-zA-Z\s]+?)\s*,\s*([A-Za-z]{2,})\s*,\s*(\d{4})\s*\Z', message="Invalid street address format. Example 2 George St, Brisbane, QLD, 4000'" )],  filters=[lambda x: x.strip() if x else None])

    start_date = DateField("Event Starts", validators=[InputRequired(message="Please enter a start date.")])
    end_date = DateField("Event Ends", validators=[InputRequired(message="Please enter an end date.")])
    start_time = TimeField("Start Time", validators=[InputRequired(message="Please enter a start time.")])
    end_time = TimeField("End Time", validators=[InputRequired(message="Please enter an end time.")])


    ticket_price = FloatField("Price per Ticket", validators=[InputRequired(message="Please enter ticket price") , NumberRange(min=1)])

    num_tickets = IntegerField("Total Number of Tickets Available", validators=[InputRequired("Please enter the number of tickets."), NumberRange(min=1, message="Number of tickets must be at least 1.")])

    status = SelectField("Event Status", choices=[
        ("Open", "Open"),
        ("Inactive", "Inactive"),
        ("Sold Out", "Sold Out"),
        ("Cancelled", "Cancelled")
    ])

    submit=SubmitField("Create Event")

    def validate_start_date(self, field):
        start = field.data
        if start < date.today():
            raise ValidationError('The event start date must be in the future.')
        
    def validate_end_date(self, field):
        end = field.data
        start_date = self.start_date.data
        if end < start_date:
            raise ValidationError('The event end date must be in the future.')

    def validate_start_time(self, field):
        start_time = self.start_time.data
        current_datetime = datetime.now()

        start_date = self.start_date.data
        start_datetime = datetime.combine(start_date, start_time)

        min_start_time = current_datetime + timedelta(hours=1)

        if start_datetime < min_start_time:
            raise ValidationError('Start time must be at least 1 hour into the future.')


    def validate_end_time(self, field):

        start_time = self.start_time.data
        end_time = field.data

        start_date = self.start_date.data
        end_data = self.end_date.data
        start_datetime = datetime.combine(start_date, start_time)
        end_datetime = datetime.combine(end_data, end_time)

        min_end_time = start_datetime + timedelta(hours=1)

        if end_datetime < min_end_time:
            raise ValidationError('The event end time must be at least 1 hour after the event start time.')

    def validate_artist_names(self, field):
        names = re.split(r'\s*,\s*|\s+', field.data.strip().strip(','))
        if len(names) < 1 or all(name == '' for name in names):
            raise ValidationError('Please enter at least one artist name.')
        for name in names:
            name = re.sub(r'\s+', ' ', name.strip())
            if not name:
                raise ValidationError('Invalid artist name.')
            if len(name) < 2:
                raise ValidationError('Each artist name must have at least two characters.') 
            
class orderForm(FlaskForm):

    num_tickets=IntegerField("Number of tickets", validators=[InputRequired("Please enter the number of tickets you would like to purchase."), NumberRange(min=1)])
    first_name=StringField("First name", validators=[InputRequired(message="Please enter your first name."), Length(min=1,max=20)])
    last_name=StringField("Last name", validators=[InputRequired(message="Please enter your last name."), Length(min=1,max=20)])
    email=StringField("Email address", description = "Example - email@gmail.com", validators=[Email(message="Please enter a valid email address."), Length(min=1,max=254), InputRequired(message="Please enter an email address.")])
    pay_type=RadioField("Select payment type", choices=[('Credit Card'), ('Debit Card')], validators=[InputRequired("Please enter a payment method")])
    card_number=StringField("Card number", validators=[InputRequired("Please enter your card number"), Regexp('^\\d{16}$', message='Must contain 16 digits only'), Length(min=16, max=16)])
    expiration=StringField('Expiration', description = "Example - 12/22", validators=[InputRequired("Please enter your the expiration date."), Regexp('^(0[1-9]|1[0-2])\/(0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]|6[0-9]|7[0-9]|8[0-9]|9[0-9])$', message='Example: Febuary 2023 = 02/23')])
    cvv=StringField("CVV", description = "3 Digits on the back of your card", validators=[InputRequired("Please enter a CVV value."), Regexp('^\\d{3}$', message='Must contain 3 digits only'), Length(min=3,max=3)])
    confirm=BooleanField("Brisbane Live Terms of Service", validators=[InputRequired("Please accept our Terms of Service.")])
    confirm2=BooleanField("I confirm my details are correct", validators=[InputRequired("Please confirm your details are correct.")])

    submit=SubmitField('Process Payment')


    
    def validate_expiration(self, field):
        data = field.data

        if not re.match('^(0[1-9]|1[0-2])\/(0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]|6[0-9]|7[0-9]|8[0-9]|9[0-9])$', data):
            raise ValidationError('Invalid expiration date.')

class CommentForm(FlaskForm):

  text = TextAreaField('Add a comment', [InputRequired(), Length(min=5, max=100)])
  submit = SubmitField('Add')


class updateForm(FlaskForm):
    
    status = SelectField("Event Status", choices=[
        ("Open", "Open"),
        ("Inactive", "Inactive"),
        ("Sold Out", "Sold Out"),
        ("Cancelled", "Cancelled")
    ])

    submit = SubmitField('update')