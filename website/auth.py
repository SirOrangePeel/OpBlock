from flask import Blueprint, render_template, request, flash, redirect, url_for
# from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__) #Create the blueprint


@auth.route('/login', methods=['GET', 'POST']) 
def login():
    return render_template("login.html", user=current_user) #Render the login page


@auth.route('/logout')
@login_required #Need to be loged in to log out
def logout():
    logout_user() #Use flask to logout user
    return redirect(url_for('auth.login')) #Redirect to the login page


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():

    return render_template("sign_up.html", user=current_user) #Render sign up page

