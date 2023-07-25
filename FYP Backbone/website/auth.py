import re
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first() #filters through the database and produces the first email that the user has inputed (not even possible to have the same email)
        if user:
            if check_password_hash(user.password, password):
                flash('Successfully Logged In!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password, Please Try Again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    data = request.form
    print(data)
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required  #makes sure that the page cannot be accessed unless the user is actually logged in
def logout(): 
    logout_user()
    return redirect(url_for('auth.login'))

import re
from flask import request, flash

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    first_name = None
    last_name = None
    email = None
    gender = None
    password = None
    confirmPassword = None


    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        email = request.form.get('email')
        gender = request.form.get('gender')
        password = request.form.get('password')
        confirmPassword = request.form.get('confirmPassword')

        account_valid = True
    
        if not first_name or not last_name:
            flash("First name and last name are required", category='error')
            account_valid = False

        if not email:
            flash("Email is required", category='error')
            account_valid = False
        elif not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', email):
            flash("Please insert a valid email", category='error')
            account_valid = False

        if not gender:
            flash("Gender field is required", category='error')
            account_valid = False

        if not password:
            flash("Please enter your password", category='error')
            account_valid = False
        else:
            if len(password) <= 8:
                flash("Your Password Must Contain At Least 8 Digits! ", category='error')
                account_valid = False
            if not re.search(r'\d', password):
                flash("Your Password Must Contain At Least 1 Number! ", category='error')
                account_valid = False
            if not re.search(r'[A-Z]', password):
                flash("Your Password Must Contain At Least 1 Capital Letter! ", category='error')
                account_valid = False
            if not re.search(r'[a-z]', password):
                flash("Your Password Must Contain At Least 1 Lowercase Letter! ", category='error')
                account_valid = False
            if not re.search(r'[\'^£$%&*()}{@#~?><>,|=_+¬-]', password):
                flash("Your Password Must Contain At Least 1 Special Character! ", category='error')
                account_valid = False

        if confirmPassword != password:
            flash("Passwords do not match", category='error')
            account_valid = False

        if account_valid:
            user = User.query.filter_by(email=email).first()
            if user: 
                flash('The email you have entered already exists', category='error')
            else:
                new_user = User(first_name=first_name, last_name=last_name, email=email, gender=gender, password=generate_password_hash(password, method='sha256'))
                db.session.add(new_user)
                db.session.commit()
                login_user(user, remember=True)
                flash('Account Created', category='success')
                return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)