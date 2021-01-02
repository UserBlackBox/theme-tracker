from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import Entry
import datetime

main = Blueprint('main', __name__)


@main.route('/')
def index():
    if not current_user.is_authenticated:
        return render_template('index.html')

    new = Entry.query.filter(Entry.user!=current_user.name).order_by(Entry.id).all()[::-1]
    new = new[:5]
    recent = Entry.query.filter_by(user=current_user.name).order_by(Entry.id).all()[::-1]
    recent = recent[:5]
    tags = set()
    tags.add(current_user.theme.lower())
    entries = Entry.query.filter_by(user=current_user.name).order_by(Entry.id).all()[::-1]
    for i in entries:
        for j in i.tags.split():
            tags.add(j)
    entries = Entry.query.filter(Entry.user!=current_user.name).order_by(Entry.id).all()[::-1]
    suggested = []
    for i in entries:
        for j in i.tags.split():
            if j in tags:
                suggested.append(i)
                break
    suggested = suggested[:5]

    return render_template('home.html', new=new, recent=recent, suggested=suggested)


@main.route('/new-activity/')
@login_required
def new():
    new = Entry.query.filter(Entry.user!=current_user.name).order_by(Entry.id).all()[::-1]
    return render_template('new.html', new=new)


@main.route('/your-entries/')
@login_required
def your():
    recent = Entry.query.filter_by(user=current_user.name).order_by(Entry.id).all()[::-1]
    return render_template('entries.html', recent=recent)


@main.route('/suggested/')
@login_required
def suggested():
    tags = set()
    tags.add(current_user.theme.lower())
    entries = Entry.query.filter_by(user=current_user.name).order_by(Entry.id).all()[::-1]
    for i in entries:
        for j in i.tags.split():
            tags.add(j)
    entries = Entry.query.filter(Entry.user!=current_user.name).order_by(Entry.id).all()[::-1]
    suggested = []
    for i in entries:
        for j in i.tags.split():
            if j in tags:
                suggested.append(i)
                break
    return render_template('activities.html', suggested = suggested)
