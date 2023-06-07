#from package import Class
from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db=SQLAlchemy()
app=Flask(__name__)  # this is the name of the module/package that is calling this app


#create a function that creates a web application
# a web server will run this web application
def create_app():
    
    app.debug=True
    app.secret_key='somesecretgoeshere'
    #app.secret_key = os.urandom(32)
    #set the app configuration data 
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///brisbane_live_events.sqlite'
    #initialise db with flask app
    db.init_app(app)

    bootstrap = Bootstrap5(app)
    
    #initialize the login manager
    login_manager = LoginManager()
    
    #set the name of the login function that lets user login
    # in our case it is auth.login (blueprintname.viewfunction name)
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    #create a user loader function takes userid and returns User
    from .models import User  # importing here to avoid circular references
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    #importing views module here to avoid circular references
    # a common practice.
    from . import views
    app.register_blueprint(views.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import createEvent
    app.register_blueprint(createEvent.bp)

    from . import myAccount
    app.register_blueprint(myAccount.bp)

    #config upload folder
    UPLOAD_FOLDER = '/static/image'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  

    return app

@app.errorhandler(404) 
def not_found(e): 
  return render_template("error.html",error=404)

@app.errorhandler(500)
def server_error(e): 
  return render_template("error.html",error=500)

@app.errorhandler(404) 
def not_found(e): 
  return render_template("error.html",error=404)

@app.errorhandler(Exception)
def handle_generic_exception(e):
    return render_template("error.html", error=e)

