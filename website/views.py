from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Walk, Active, Walker, Location
from sqlalchemy.orm import joinedload
from . import db
import json
import re
from dotenv import load_dotenv 
import os 

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
    # Query pickup locations for start, all locations for end
    pickup_locations = Location.query.filter_by(pickup=True).order_by(Location.name).all()
    all_locations = Location.query.order_by(Location.name).all()

    previous_s_loc = request.form.get("s_loc")
    previous_e_loc = request.form.get("e_loc")

    while True:
        s_loc = request.form.get("s_loc")
        e_loc = request.form.get("e_loc")

        if previous_s_loc != s_loc:
            # Get the new value
            # Put that into the places API
            # Place a marker on the location
            pass

        if previous_e_loc != e_loc:
            # Get the new value
            # Put that into the places API
            # Place a marker on the location
            pass

        if request.method == "POST":
            ccid = request.form.get("student_id")
            email = request.form.get("email")
            f_name = request.form.get("first_name")
            l_name = request.form.get("last_name")
            s_loc = request.form.get("s_loc")
            e_loc = request.form.get("e_loc")

            # Basic validation
            if not all([ccid, email, f_name, l_name, s_loc, e_loc]):
                flash("All fields are required.", "error")
                return render_template(
                    "request.html",
                    pickup_locations=pickup_locations,
                    all_locations=all_locations
                )

            new_walk = Walk(
                ccid=ccid,
                email=email,
                f_name=f_name,
                l_name=l_name,
                s_loc=int(s_loc),
                e_loc=int(e_loc)
            )
            db.session.add(new_walk)
            db.session.flush()  # Get new_walk.id before committing

            new_active = Active(
                walk_id=new_walk.id,
                status="Pending"
            )
            db.session.add(new_active)
            db.session.commit()

            flash("Walk request submitted and activated!", "success")

            return redirect(url_for("mailer.sendPending", recipient=new_walk.email, active_id=new_active.id))

    return render_template(
        "request.html",
        pickup_locations=pickup_locations,
        all_locations=all_locations,
        maps_key=os.getenv("MAPS_KEY")
    )



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

@views.route("/<int:active_id>", methods=["GET", "POST"])
def view_walk(active_id):
    active = Active.query.filter_by(id=active_id).first_or_404()
    return render_template("walk.html", walk=active.walk)

