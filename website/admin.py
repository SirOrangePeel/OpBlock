from flask import Blueprint, render_template, request, redirect, flash
from .models import Walker, Active
from sqlalchemy.orm import joinedload
from . import db

admin = Blueprint("admin", __name__)

@admin.route("/dashboard")
def dashboard():
    return render_template("admin/dashboard.html")

@admin.route("/view-volunteers", methods=["GET", "POST"])
def view_Volunteers():
    
    return render_template("admin/view_volunteers.html")

@admin.route("/create-walker", methods=["GET", "POST"])
def create_walker():

    if request.method == "POST":
        ccid = request.form.get("ccid")
        email = request.form.get("email")
        f_name = request.form.get("f_name")
        l_name = request.form.get("l_name")
        schedule = request.form.get("schedule")

        # Check if email already exists
        existing = Walker.query.filter_by(email=email).first()
        if existing:
            flash("Email already exists.", "error")
            return redirect("admin/create-walker")

        new_walker = Walker(
            ccid=ccid,
            email=email,
            f_name=f_name,
            l_name=l_name,
            status="Available",
            schedule=schedule
        )

        db.session.add(new_walker)
        db.session.commit()

        flash("Walker created successfully!", "success")
        return render_template("admin/walker_confirm.html", walker=new_walker)

    return render_template("admin/create_walker.html")

@admin.route("/pending")
def pending():

    pending_walks = Active.query.filter_by(status="Pending").all()

    return render_template("pending.html", pending_walks=pending_walks)

@admin.route("/pending-data")
def pending_data():
    pending_walks = (
        Active.query
        .options(joinedload(Active.walk))
        .filter_by(status="Pending")
        .all()
    )
    return render_template("partials/pending_list.html", pending_walks=pending_walks)