from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Walk, Active, History
from . import db

decisions = Blueprint('decisions', __name__)

# Complete successful walk
@views.route("/complete/success/<active_id>/<walker_id>", methods=["GET", "POST"])
def complete_walk_success(active_id, walker_id):
    active = Active.query.filter_by(id=active_id).first_or_404()

    new_history = History(
        walk_id=active.walk_id,
        success=True,
        walker=walker_id
    )

    db.session.delete(active)
    db.session.add(new_history)
    db.session.commit()

    return redirect(url_for("views.home"))

# Complete failure walk
@views.route("/complete/failure/<active_id>/<walker_id>", methods=["GET", "POST"])
def complete_walk_success(active_id, walker_id=None):
    active = Active.query.filter_by(id=active_id).first_or_404()

    new_history = History(
        walk_id=active.walk_id,
        success=False,
        walker=walker_id
    )

    db.session.delete(active)
    db.session.add(new_history)
    db.session.commit()

    return redirect(url_for("views.home"))