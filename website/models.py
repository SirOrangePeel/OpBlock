from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Walk(db.Model): # Database schema for Notes
    id = db.Column(db.Integer, primary_key=True)
    ccid = db.Column(db.String(25))
    email = db.Column(db.String(150))
    f_name = db.Column(db.String(25))
    l_name = db.Column(db.String(25))
    s_loc = db.Column(db.Integer, db.ForeignKey('location.location_id'))
    e_loc = db.Column(db.Integer, db.ForeignKey('location.location_id'))

class Walker(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    ccid = db.Column(db.String(25))
    email = db.Column(db.String(150), unique=True)
    f_name = db.Column(db.String(25))
    l_name = db.Column(db.String(25))
    status = db.Column(db.String(25))
    avail = db.Column(db.Boolean)
    schedule = db.Column(db.String(1000))

    past_walks = db.relationship("History", backref=db.backref("history", remote_side=[id]), lazy=True)

class Admin(db.Model, UserMixin): 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(150))
    password = db.Column(db.String(150))

class Recurring(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    creationDate = db.Column(db.DateTime(timezone=True), default=func.now()) #func just returns the current datetime
    schedule = db.Column(db.String(1000))
    walk_id = db.Column(db.Integer, db.ForeignKey('walk.id'))
    active = db.Column(db.Boolean)
    one_time = db.Column(db.Boolean)

class Active(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now()) #func just returns the current datetime
    walk_id = db.Column(db.Integer, db.ForeignKey('walk.id'))
    status = db.Column(db.String(25))
    walker_id = db.Column(db.Integer, db.ForeignKey('walker.id'), nullable=True)
    walk = db.relationship("Walk", backref="active_entries")
    walker = db.relationship("Walker", backref="active_entries")

class History(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now()) #func just returns the current datetime
    walk_id = db.Column(db.Integer, db.ForeignKey('walk.id'))
    success = db.Column(db.Boolean)
    walker = db.Column(db.Integer, db.ForeignKey('walker.id'), nullable=True)

class Location(db.Model):
    location_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    pickup = db.Column(db.Boolean)
    dropoff_20_min_dist = db.Column(db.Boolean)
    lat = db.Column(db.Float, nullable=True)
    lng = db.Column(db.Float, nullable=True)
