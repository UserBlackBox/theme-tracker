from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    theme = db.Column(db.String(1000))

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, unique=True)
    date = db.Column(db.DateTime)
    entry = db.column(db.String(10000))
