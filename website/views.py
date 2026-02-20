from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
import json

views = Blueprint('views', __name__) #Create a blueprint for this files. IE the "views"

@views.route("/")
def home():
    return render_template("home.html")