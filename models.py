from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Userpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # valid ID of an existing user to this field when a new object is created. This is a one to many relationship


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    gender = db.Column(db.String(15))
    password = db.Column(db.String(150))
    userpost = db.relationship('Userpost')

    #if I want to start the collaborative platform, it might be worth using one to many relationship