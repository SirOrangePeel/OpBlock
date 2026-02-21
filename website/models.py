from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Walk(db.Model): # Database schema for Notes
    id = db.Column(db.Integer, primary_key=True)
    ccid = db.Column(db.String(25))
    email = db.Column(db.String(150))
    f_name = db.Column(db.String(25))
    l_name = db.Column(db.String(25))
    lat_start = db.Column(db.Numeric(9, 6), nullable=False)
    lon_start = db.Column(db.Numeric(9, 6), nullable=False)
    lat_end = db.Column(db.Numeric(9, 6), nullable=False)
    lon_end = db.Column(db.Numeric(9, 6), nullable=False)


class Walker(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    ccid = db.Column(db.String(25))
    email = db.Column(db.String(150), unique=True)
    f_name = db.Column(db.String(25))
    l_name = db.Column(db.String(25))
    status = db.Column(db.String(25))
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

class Active(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now()) #func just returns the current datetime
    walk_id = db.Column(db.Integer, db.ForeignKey('walk.id'))
    status = db.Column(db.String(25))
    walk = db.relationship("Walk", backref="active_entries")

class History(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now()) #func just returns the current datetime
    walk_id = db.Column(db.Integer, db.ForeignKey('walk.id'))
    completes = db.Column(db.Boolean)
    walker = db.Column(db.Integer, db.ForeignKey('walker.id'))