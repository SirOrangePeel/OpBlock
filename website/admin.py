from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user
from .models import Walker, Active
from sqlalchemy.orm import joinedload
from . import db

admin = Blueprint("admin", __name__)

@admin.route("/dashboard")
@login_required
def dashboard():
    return render_template("admin/dashboard.html")

@admin.route("/view-volunteers", methods=["GET", "POST"])
@login_required
def view_Volunteers():
    
    return render_template("admin/view_volunteers.html")

@admin.route("/create-walker", methods=["GET", "POST"])
@login_required
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
@login_required
def pending():

    pending_walks = (
        Active.query
        .options(joinedload(Active.walk))
        .filter_by(status="Pending")
        .all()
    )

    available_walkers = Walker.query.filter_by(status="Available").all()

    return render_template(
        "pending.html",
        pending_walks=pending_walks,
        available_walkers=available_walkers
    )


@admin.route("/pending-data")
@login_required
def pending_data():

    pending_walks = (
        Active.query
        .options(joinedload(Active.walk))
        .filter_by(status="Pending")
        .all()
    )

    assigned_walker_ids = db.session.query(Active.walker_id)\
        .filter(Active.walker_id.isnot(None))\
        .subquery()

    available_walkers = Walker.query\
        .filter(~Walker.id.in_(assigned_walker_ids))\
        .all()
        
    print("Assigned IDs:", db.session.query(Active.walker_id).all())
    
    return render_template(
        "partials/pending_list.html",
        pending_walks=pending_walks,
        available_walkers=available_walkers
    )