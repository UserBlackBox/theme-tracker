from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/login/', methods=['GET'])
def login():
    return render_template('login.html')

@auth.route('/login/', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(name=username).first()
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=True)
    return redirect(url_for('main.index'))

@auth.route('/signup/', methods=['GET'])
def signup():
    return render_template('signup.html')

@auth.route('/signup/', methods=['POST'])
def signup_post():
    username = request.form.get('username')
    password = request.form.get('password')
    theme = request.form.get('theme')

    if request.form.get('password_verify') != password:
        flash('Passwords do not match')
        return redirect(url_for('auth.signup'))

    if len(password) < 8:
        flash('Password is too short')
        return redirect(url_for('auth.signup'))

    if User.query.filter_by(name=username).first():
        flash('User with that username already exists, try logging in <a href="{0}">here</a>'.format(url_for('auth.login')))
        return redirect(url_for('auth.signup'))

    new_user = User(name=username, password=generate_password_hash(password, method='sha256'), theme=theme)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
