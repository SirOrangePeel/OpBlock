from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
import json
from dotenv import load_dotenv 
import os 
load_dotenv() # Load variables from .env to environment

views = Blueprint('views', __name__) #Create a blueprint for this files. IE the "views"

@views.route("/")
def home():
    return render_template("home.html")

@views.route("/map")
def map():
    return render_template(
        "maps.html",
        maps_key=os.getenv("MAPS_API_KEY")
    )
