from flask import Blueprint, flash, render_template, request, url_for, redirect, session
from werkzeug.security import generate_password_hash,check_password_hash
#from .models import User
from .forms import LoginForm, RegisterForm
from flask_login import login_user, login_required, logout_user
from . import db
from .models import User

#create a blueprint
bp = Blueprint('auth', __name__)

# @bp.route('/login', methods=['GET', 'POST'])
# def authenticate(): #view function
#     print('In Login View function')
#     login_form = LoginForm()
#     error=None
#     if(login_form.validate_on_submit()==True):
#         user_name = login_form.user_name.data
#         password = login_form.password.data
#         user = User.query.filter_by(name=user_name).first()
#         if user is None:
#             error='Incorrect credentials supplied'
#         elif not check_password_hash(user.password_hash, password): # takes the hash and password
#             error='Incorrect credentials supplied'
#         if error is None:
#             login_user(user)
#             nextp = request.args.get('next') #this gives the url from where the login page was accessed
#             print(nextp)
#             if next is None or not nextp.startswith('/'):
#                 return redirect(url_for('index'))
#             return redirect(nextp)
#         else:
#             flash(error)
#     return render_template('user.html', form=login_form, heading='Login')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    register = RegisterForm()
    #the validation of form submis is fine
    if (register.validate_on_submit() == True):
            #get username, password and email from the form
            uname =register.user_name.data
            pwd = register.password.data
            email=register.email_id.data
            mobile_number = register.mobile_number.data
            #check if a user exists
            u1 = User.query.filter_by(name=uname).first()
            if u1:
                flash('User name already exists, please login')
                return redirect(url_for('auth.login'))
            pwd_hash = generate_password_hash(pwd)
            new_user = User(name=uname, password_hash=pwd_hash, email_address=email, mobile_number=mobile_number)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('main.index'))
    else:
        return render_template('user.html', form=register, heading='Register')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    error=None
    if(login_form.validate_on_submit()==True):
        user_name = login_form.user_name.data
        password = login_form.password.data
        user = User.query.filter_by(name=user_name).first()
        
        #check if there is a user with that name
        if user is None:
            error='There is no matching user name in our system. Please try again'
        #check the password
        elif not check_password_hash(user.password_hash, password):
            error='There is no matching password in our system. Please try again'
        if error is None:
        #sign in and set the login user
            flash('You logged in successfully')
            login_user(user)
            session['user'] = user
            return redirect(url_for('main.index'))
        else:
            flash(error,'danger')
    return render_template('user.html', form=login_form, heading='Login')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been successfully signed out. See you next time", 'success')
    return redirect(url_for('main.index'))