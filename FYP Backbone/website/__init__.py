# The role of this file is to make the website folder a python package
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "adviceportal.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Karissa is so cool'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' #SQL databse is stored/located at this database
    db.init_app(app)


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    
    #from . import models
    from .models import User

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    #this is telling flask how we load the user. using get I wont have to specify the user ID

    return app

#created a flask app, as well as a secret key for storing cookies and session data, etc. and have also returned the app
