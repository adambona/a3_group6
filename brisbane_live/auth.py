from flask import Blueprint, flash, render_template, request, url_for, redirect, session
from werkzeug.security import generate_password_hash,check_password_hash
#from .models import User
from .forms import LoginForm, RegisterForm
from flask_login import login_user, login_required, logout_user
from . import db
from .models import User

#create a blueprint
bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    register = RegisterForm()
    #the validation of form submission is fine
    if (register.validate_on_submit() == True):
            #get username, password and email from the form
            uname =register.user_name.data
            pwd = register.password.data
            email=register.email_id.data
            mobile_number = register.mobile_number.data

            pwd_hash = generate_password_hash(pwd)
            new_user = User(name=uname, password_hash=pwd_hash, email_address=email, mobile_number=mobile_number)
            db.session.add(new_user)
            db.session.commit()

            flash('You have successfully registered.', 'text-success')
            return redirect(url_for('auth.login'))
    else:
        return render_template('user.html', form=register, heading='Register')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    #error = None
     #the validation of form submission is fine
    if(login_form.validate_on_submit()==True):
        email = login_form.email_id.data
        #password = login_form.password.data
        user = User.query.filter_by(email_address=email).first()

        flash('You logged in successfully', 'text-success')

        login_user(user)
        return redirect(url_for('main.index'))
    return render_template('user.html', form=login_form, heading='Login')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been successfully signed out. See you next time.", 'text-success')
    return redirect(url_for('main.index'))