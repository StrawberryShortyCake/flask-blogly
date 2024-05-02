"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import NotFound

from models import db, dbx, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
db.init_app(app)

# TODO: need to listen for when a user page is going to be generated


@app.get('/')
def show_homepage():

    q = db.select(User)
    users = dbx(q).scalars().all()

    return render_template(
        "user_listing.jinja",
        users=users
    )


@app.get('/users')
def show_all_users():

    q = db.select(User).order_by(User.last_name, User.first_name)
    sorted_users = dbx(q).scalars().all()

    return render_template(
        "user_listing.jinja",
        users=sorted_users
    )


@app.get('/users/new')
def add_new_user():

    return render_template(
        "new_user.jinja"
    )


@app.post('/users/new')
def handle_add_user():

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    img_url = request.form['img_url'] or None

    user = User(first_name=first_name,
                last_name=last_name,
                image_url=img_url
                )

    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.get('/users/<int:user_id>')
def show_user_details(user_id):

    q = db.select(User).where(User.id == user_id)
    user = dbx(q).scalars().all()[0]

    return render_template(
        "user_details.jinja",
        user=user
    )


@app.get('/users/<int:user_id>/edit')
def edit_user_details(user_id):

    q = db.select(User).where(User.id == user_id)
    user = dbx(q).scalars().all()[0]

    return render_template(
        "user_edit.jinja",
        user=user
    )


@app.post('/users/<int:user_id>/edit')
def confirm_user_edit(user_id):

    q = db.select(User).where(User.id == user_id)
    user = dbx(q).scalars().one()

    # TODO: ADD VALIDATIONS
    # TODO: TEST

    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['img_url']

    db.session.commit()

    return redirect('/users')


@app.post('/users/<int:user_id>/delete')
def confirm_user_delete(user_id):

    q = db.select(User).where(User.id == user_id)
    user = dbx(q).scalars().one()

    db.session.delete(user)
    db.session.commit()

    return redirect('/users')
