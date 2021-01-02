from flask import Blueprint, render_template, redirect, url_for, request, abort
from flask_login import login_required, current_user
from . import db
from .models import Entry, User
import datetime

main = Blueprint('main', __name__)


@main.route('/')
def index():
    if not current_user.is_authenticated:
        return render_template('index.html')

    new = Entry.query.filter(Entry.user!=current_user.name).filter_by(public=True).order_by(Entry.id).all()[::-1]
    new = new[:5]
    recent = Entry.query.filter_by(user=current_user.name).order_by(Entry.id).all()[::-1]
    recent = recent[:5]
    tags = set()
    tags.add(current_user.theme.lower())
    entries = Entry.query.filter_by(user=current_user.name).order_by(Entry.id).all()[::-1]
    for i in entries:
        for j in i.tags.split():
            tags.add(j)
    entries = Entry.query.filter(Entry.user!=current_user.name).filter_by(public=True).order_by(Entry.id).all()[::-1]
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
    new = Entry.query.filter(Entry.user != current_user.name).filter_by(public=True).order_by(Entry.id).all()[::-1]
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
    entries = Entry.query.filter_by(user=current_user.name).filter_by(public=True).order_by(Entry.id).all()[::-1]
    for i in entries:
        for j in i.tags.split():
            tags.add(j)
    entries = Entry.query.filter(Entry.user != current_user.name).order_by(Entry.id).all()[::-1]
    suggested = []
    for i in entries:
        for j in i.tags.split():
            if j in tags:
                suggested.append(i)
                break
    return render_template('activities.html', suggested=suggested)

@main.route('/new/', methods=['GET'])
@login_required
def new_entry():
    return render_template('new-entry.html')

@main.route('/new/', methods=['POST'])
@login_required
def new_entry_post():
    entry = request.form.get('entry')
    tags = request.form.get('tags').lower()
    date = datetime.datetime.strptime(request.form.get('date'), '%Y-%m-%d')
    public = True if request.form.get('public') else False
    entries = Entry.query.order_by(Entry.id).all()
    if len(entries) == 0:
        id = 1
    else:
        id = entries[-1].id+1
    new_entry = Entry(id=id, user=current_user.name, date=date, entry=entry, tags=tags, public=public)
    db.session.add(new_entry)
    db.session.commit()
    return redirect(url_for('main.your'))

@main.route('/settings/', methods=['GET'])
@login_required
def settings():
    return render_template('settings.html')

@main.route('/settings/', methods=['POST'])
@login_required
def settings_post():
    current_user.theme = request.form.get('theme')
    db.session.commit()
    return redirect(url_for('main.index'))

@main.route('/profile/<user>/')
@login_required
def profile(user):
    user = User.query.filter_by(name=user).first()
    if not user:
        abort(404)
    entries = Entry.query.filter_by(user=user.name).filter_by(public=True).order_by(Entry.id).all()[::-1]
    return render_template('profile.html', user=user.name, entries=entries)
