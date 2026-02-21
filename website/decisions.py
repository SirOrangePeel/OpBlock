from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Walk, Active, History, Walker
from . import db
from .mail import inform_invitation

decisions = Blueprint('decisions', __name__)

# Complete successful walk
@decisions.route("/complete/success/<active_id>/<walker_id>", methods=["GET"])
def complete_walk_success(active_id, walker_id):
    active = Active.query.filter_by(id=active_id).first_or_404()

    new_history = History(
        walk_id=active.walk_id,
        success=True,
        walker_id=walker_id
    )

    db.session.delete(active)
    db.session.add(new_history)
    db.session.commit()

    return redirect(url_for("mail.sendCompleted", recipient=active.email))

# Complete failure walk
@decisions.route("/complete/failure/<active_id>/<walker_id>", methods=["GET"])
def complete_walk_failure(active_id, walker_id=None):
    active = Active.query.filter_by(id=active_id).first_or_404()

    new_history = History(
        walk_id=active.walk_id,
        success=False,
        walker_id=walker_id
    )

    db.session.delete(active)
    db.session.add(new_history)
    db.session.commit()

    return redirect(url_for("mail.sendCompleted", recipient=active.email))


# Invite a walker
@decisions.route("/invite/<int:active_id>", methods=["POST"])
@login_required
def invite_walker(active_id):

    walker_id = request.form.get("walker_id")

    active = Active.query.filter_by(id=active_id).first_or_404()
    walker = Walker.query.filter_by(id=walker_id).first_or_404()

    if active.walker_id is not None:
        return redirect(url_for("admin.pending"))

    # Assign walker
    active.walker = walker
    active.status = "Invited"

    db.session.commit()

    # Send invitation email
    inform_invitation(walker, active_id)

    return redirect(url_for("admin.pending"))

# Walker accept
@decisions.route("/accept/<active_id>/<walker_id>", methods=["GET"])
def walker_accept(active_id, walker_id):
    active = Active.query.filter_by(id=active_id).first_or_404()
    active.status = "In Progress"
    active.walker = walker_id
    db.session.commit()

    return redirect(url_for("mail.sendAccepted", recipient=active.email, active_id=active_id))

# Walker reject
@decisions.route("/reject/<active_id>/<walker_id>", methods=["GET"])
def walker_reject(active_id, walker_id):
    active = Active.query.filter_by(id=active_id).first_or_404()
    active.status = "Pending"
    db.session.commit()

    return redirect(url_for("views.home"))