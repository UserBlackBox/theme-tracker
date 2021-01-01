from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, login_required, current_user
from . import db
from .models import User, Entry

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET'])
def login():
    return 'Login'

@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(name=username).first()
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))
    return #TODO add a redirect page here

@auth.route('/signup', methods=['GET'])
def signup():
    return 'Signup'

@auth.route('/signup', methods=['POST'])
def signup_post():
    username = request.form.get('username')
    password = request.form.get('password')
    theme = request.form.get('theme')

    if User.query.filter_by(name=username).first():
        flash('User with that username already exists')
        return redirect(url_for('auth.signup'))

    new_user = User(name=username, password=generate_password_hash(password, method='sha256'), theme=theme)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
def logout():
    return 'Logout'