from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   #means from __init__.py import db
from .models import Admin
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__) # Create the blueprint


@auth.route('/login', methods=['GET', 'POST']) 
def login():
    if request.method == 'POST': #Check if the access is a POST
        email = request.form.get('email') #Collect email from the form
        password = request.form.get('password') #Collect the password from the form

        user = Admin.query.filter_by(email=email).first() #Collect all Users from the database with this email. At most there should only be 1 user as email should be unique based on the schema
        if user: #If a user exists
            if check_password_hash(user.password, password): #Check the password against the hashed password
                flash('Logged in successfully!', category='success') #Message
                login_user(user, remember=True) #Use the flask_login functions to set the current user
                return redirect(url_for('admin.dashboard')) #Redirect back to home
            else:
                flash('Incorrect password, try again.', category='error') #If password is wrong error message
        else:
            flash('Email does not exist.', category='error') #If email is wrong error message

    return render_template("admin/login.html", user=current_user) #Render the login page


@auth.route('/logout')
@login_required #Need to be loged in to log out
def logout():
    logout_user() #Use flask to logout user
    return redirect(url_for('admin.dashboard')) #Redirect to the login page


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST': #Same as login page but with more data validations
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = Admin.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = Admin(email=email, first_name=first_name, password=generate_password_hash(password1)) #Hash users password
            db.session.add(new_user) #Add the new user to the database
            db.session.commit() #Save
            login_user(new_user, remember=True) #User flask to login new user
            flash('Account created!', category='success') #Message
            return redirect(url_for('admin.dashboard')) #Redirect to home

    return render_template("admin/sign_up.html", user=current_user) #Render sign up page

