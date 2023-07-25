#store the standard root for the website. Also anythign not related to authentication that the user can use
from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
@login_required #cannot get to the homepage unless logged in
def home():
    return render_template("home.html", user=current_user)
