from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__) #Create a blueprint for this files. IE the "views"

@views.route("/map")
def map():
    return render_template(
        "map.html",
        maps_key=current_app.config["MAPS_KEY"]
    )
