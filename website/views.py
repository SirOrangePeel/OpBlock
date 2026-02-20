from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Walk, Active
from sqlalchemy.orm import joinedload
from . import db
import json
import re
from dotenv import load_dotenv 
import os 
load_dotenv() # Load variables from .env to environment

views = Blueprint('views', __name__)

# Home Page
@views.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if request.form.get('form_type') == 'form1':
            return redirect(url_for("views.request_page"))
        else:
            return redirect(url_for("views.contact"))

    return render_template("home.html")

@views.route("/contact")
def contact():
    return render_template("contact.html")


@views.route("/request", methods=["GET", "POST"])
def request_page():
    if request.method == "POST":

        # Form Data
        ccid = request.form.get("student_id")
        email = request.form.get("email")
        f_name = request.form.get("first_name")
        l_name = request.form.get("last_name")

        lat_start = request.form.get("lat_start")
        lon_start = request.form.get("lon_start")
        lat_end = request.form.get("lat_end")
        lon_end = request.form.get("lon_end")

        # Create Walk
        new_walk = Walk(
            ccid=ccid,
            email=email,
            f_name=f_name,
            l_name=l_name,
            lat_start=lat_start,
            lon_start=lon_start,
            lat_end=lat_end,
            lon_end=lon_end
        )

        db.session.add(new_walk)
        db.session.commit()


        new_active = Active(
            walk_id=new_walk.id,
            status="Pending"
        )

        db.session.add(new_active)
        db.session.commit()

        flash("Walk request submitted and activated!", "success")
        return redirect(url_for("views.request_page"))

    return render_template("request.html")

@views.route("/pending")
def pending():

    pending_walks = Active.query.filter_by(status="Pending").all()

    return render_template("pending.html", pending_walks=pending_walks)

@views.route("/pending-data")
def pending_data():
    pending_walks = (
        Active.query
        .options(joinedload(Active.walk))
        .filter_by(status="Pending")
        .all()
    )
    return render_template("partials/pending_list.html", pending_walks=pending_walks)

    return render_template("home.html")

@views.route("/map")
def map():
    return render_template(
        "maps.html",
        maps_key=os.getenv("MAPS_API_KEY")
    )
