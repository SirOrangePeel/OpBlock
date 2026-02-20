from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Walk, Active, Walker
from sqlalchemy.orm import joinedload
from . import db
import json
import re

views = Blueprint('views', __name__)

# Home Page
@views.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if request.form.get('form_type') == 'form1':
            return redirect(url_for("views.request_page"))
        else:
            return redirect(url_for("views.contact"))

    return render_template("index.html")

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


@views.route("/create-walker", methods=["GET", "POST"])
def create_walker():

    if request.method == "POST":
        ccid = request.form.get("ccid")
        email = request.form.get("email")
        f_name = request.form.get("f_name")
        l_name = request.form.get("l_name")
        status = request.form.get("status")
        schedule = request.form.get("schedule")

        # Check if email already exists
        existing = Walker.query.filter_by(email=email).first()
        if existing:
            flash("Email already exists.", "error")
            return redirect("/create-walker")

        new_walker = Walker(
            ccid=ccid,
            email=email,
            f_name=f_name,
            l_name=l_name,
            status=status,
            schedule=schedule
        )

        db.session.add(new_walker)
        db.session.commit()

        flash("Walker created successfully!", "success")
        return render_template("walker_confirm.html", walker=new_walker)

    return render_template("create_walker.html")