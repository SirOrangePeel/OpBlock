from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from dotenv import load_dotenv 
import os 
load_dotenv() # Load variables from .env to environment

db = SQLAlchemy() #Start database object
DB_NAME = "database.db" #Name of database


def create_app():
    app = Flask(__name__) #Create app
    app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY")  #Secret key.
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' #Location of the database. IE the same folder as parent 
    app.config["MAPS_KEY"] = os.getenv("DIRECTIONS_API_KEY") #Maps API key

    if not app.config['SECRET_KEY']:
        raise ValueError("SECRET_KEY not set")
    if not app.config['API_KEY']:
        raise ValueError("API_KEY not set")

    db.init_app(app) #Connect the database to the app

    #Import the blueprints for views and auth
    from .views import views
    from .auth import auth

    #Register the correct prefixes
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    #Import the database model schemas
    from .models import Admin, Walk, Walker, Recurring, Active, History
    
    #Using the app context (The connected database and models) create the schemas
    create_database(app) #Creating the database

    #Start login manager
    login_manager = LoginManager() #Create object
    login_manager.login_view = 'auth.login' #View where users will login
    login_manager.init_app(app) #Connect login manager to app

    #User loader for login manager. Not quite sure what this is but I think it is the way that login manager should be able to access a user. IE the query to be able to get a User object
    @login_manager.user_loader
    def load_user(id):
        return Admin.query.get(int(id))

    return app #Return the configured app


def create_database(app): #Function to create database if it doesn't exist
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')