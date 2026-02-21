from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from dotenv import load_dotenv 
import os 
load_dotenv() # Load variables from .env to environment

db = SQLAlchemy() #Start database object
mail = Mail() # instantiate the mail class
DB_NAME = "database.db" #Name of database


def env_bool(name: str, default: bool = False) -> bool:
    v = os.getenv(name)
    if v is None:
        return default
    return v.strip().lower() in ("1", "true", "yes", "y", "on")

def create_app():
    app = Flask(__name__) #Create app

    app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY")  #Secret key.
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' #Location of the database. IE the same folder as parent 
    app.config["MAPS_KEY"] = os.getenv("MAPS_KEY") #Maps API key

    # configuration of mail
    app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER") #Server to use
    app.config['MAIL_PORT'] = os.getenv("MAIL_PORT") #Port to email
    app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME") #Username. email
    app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD") #Password
    app.config["MAIL_USE_TLS"] = env_bool("MAIL_USE_TLS", True)
    app.config["MAIL_USE_SSL"] = env_bool("MAIL_USE_SSL", False)
    app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER", app.config["MAIL_USERNAME"])
    

    if not app.config['SECRET_KEY']:
        raise ValueError("SECRET_KEY not set")
    if not app.config['MAPS_KEY']:
        raise ValueError("MAPS_KEY not set")

    mail.init_app(app)
    db.init_app(app) #Connect the database to the app

    #Import the blueprints for views and auth
    from .views import views
    from .auth import auth
    from .mail import mailer
    from .admin import admin
    from .decisions import decisions

    #Register the correct prefixes
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(mailer, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(decisions, url_prefix='/')

    #Import the database model schemas
    from .models import Admin, Walk, Walker, Recurring, Active, History, Location
    
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


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')

    from .models import Location

    with app.app_context():
        if not Location.query.first() is None:
            return

        data_folder = "website/data"

        FILE_FLAGS = {
            "pickup_locations.txt": {"pickup": True,  "dropoff_20_min_dist": False},
            "stations_20m.txt":      {"pickup": False, "dropoff_20_min_dist": True},
            "stations_non20m.txt":   {"pickup": False, "dropoff_20_min_dist": False},
        }

        for file in os.scandir(data_folder):

            if not file.is_file():
                continue

            print("Seeding:", file.name)

            flags = FILE_FLAGS.get(file.name)
            if not flags:
                continue

            with open(file.path, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split(",")
                    if len(parts) != 3:
                        print("Skipping bad line:", line)
                        continue
                    name, lat, lng = parts
                    location = Location(
                        name=name.strip(),
                        lat=float(lat.strip()),
                        lng=float(lng.strip()),
                        pickup=flags["pickup"],
                        dropoff_20_min_dist=flags["dropoff_20_min_dist"]
                    )
                    db.session.add(location)

        db.session.commit()
        print("Seeded location data.")