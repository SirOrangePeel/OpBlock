from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Walk
from . import db
import json
import re

views = Blueprint('views', __name__)

# Home Page
@views.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        return redirect(url_for("views.request_page"))

    return render_template("index.html")



@views.route("/request", methods=["GET", "POST"])
def request_page():
    if request.method == "POST":

        ccid = request.form.get("student_id")
        f_name = request.form.get("first_name")
        l_name = request.form.get("last_name")
        email = request.form.get("email")
        
        
        if not ccid or len(ccid) < 25:
            flash("Student ID must be at least 3 characters.", "error")
            return redirect(url_for("views.request_page"))

        if not f_name or not l_name:
            flash("First and Last name are required.", "error")
            return redirect(url_for("views.request_page"))

        # Basic email regex
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Please enter a valid email address.", "error")
            return redirect(url_for("views.request_page"))
        

        # Create Walk object
        new_walk = Walk(
            ccid=ccid,
            f_name=f_name,
            l_name=l_name,
            email=email
        )

        db.session.add(new_walk)
        db.session.commit()

        flash("Request submitted successfully!", "success")
        return redirect(url_for("views.request_page"))

    return render_template("request.html")