from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Walk(db.Model): # Database schema for Notes
    id = db.Column(db.Integer, primary_key=True)
    ccid = db.Column(db.String(25))
    email = db.Column(db.String(150), unique=False)
    f_name = db.Column(db.String(25))
    l_name = db.Column(db.String(25))
    s_loc = db.Column(db.Integer, db.ForeignKey('locations.location_id'))

    e_loc_lat = db.Column(db.Integer, nullable=False)
    e_loc_lng = db.Column(db.Integer, nullable=False)

    @property
    def coordinates(self):
        return (self.e_loc_lat, self.e_loc_lng)

    @coordinates.setter
    def coordinates(self, value):
        self.e_loc_lat, self.e_loc_lng = value



class Walker(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    ccid = db.Column(db.String(25))
    email = db.Column(db.String(150), unique=True)
    f_name = db.Column(db.String(25))
    l_name = db.Column(db.String(25))
    status = db.Column(db.String(25))
    schedule = db.Column(db.String(1000))

    past_walks = db.relationship("History", backref=db.backref("history", remote_side=[id]), lazy=True)

class Admin(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

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
    completes = active = db.Column(db.Boolean)
    walker = db.Column(db.Integer, db.ForeignKey('walker.id'))

class Locations(db.Model):
    location_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False)

    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    @property
    def coordinates(self):
        return (self.latitude, self.longitude)

    @coordinates.setter
    def coordinates(self, value):
        self.latitude, self.longitude = value