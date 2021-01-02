from flask_login import UserMixin

from . import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    theme = db.Column(db.String(1000))
    following = db.Column(db.Text())


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user = db.Column(db.String(1000))
    date = db.Column(db.DateTime)
    entry = db.Column(db.String(1000))
    tags = db.Column(db.String(1000))
    public = db.Column(db.Boolean())
