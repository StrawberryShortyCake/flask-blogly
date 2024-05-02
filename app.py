"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import NotFound

from models import db, dbx, User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'  # WHY DOES THIS WORK WITH FLASH???
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
db.init_app(app)


@app.get('/')
def show_homepage():
    """Show the user_listing page with all the users."""

    q = db.select(User)
    users = dbx(q).scalars().all()

    return render_template(
        "user_listing.jinja",
        users=users
    )


@app.get('/users')
def show_all_users():
    """Show the user_listing page with all the users, ordered by last name,
        first name."""

    q = db.select(User).order_by(User.last_name, User.first_name)
    sorted_users = dbx(q).scalars().all()

    return render_template(
        "user_listing.jinja",
        users=sorted_users
    )


@app.get('/users/new')
def add_new_user():
    """ Show the add new user form. """

    return render_template(
        "new_user.jinja"
    )


@app.post('/users/new')
def handle_add_user():
    """ Given first name, last name, and an optional image URL,
        add a user to the database. """

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    img_url = request.form['img_url'] or None

    user = User(first_name=first_name,
                last_name=last_name,
                image_url=img_url
                )

    db.session.add(user)
    db.session.commit()

    flash(f'User {first_name} was added!')

    return redirect('/users')


@app.get('/users/<int:user_id>')
def show_user_details(user_id):
    """ Given a user id, show the page for the user details. """

    q = db.select(User).where(User.id == user_id)
    user = dbx(q).scalars().one()

    return render_template(
        "user_details.jinja",
        user=user
    )


@app.get('/users/<int:user_id>/edit')
def edit_user_details(user_id):
    """ Given the user id, show the page for the user to edit details. """

    q = db.select(User).where(User.id == user_id)
    user = dbx(q).scalars().one()

    return render_template(
        "user_edit.jinja",
        user=user
    )


@app.post('/users/<int:user_id>/edit')
def confirm_user_edit(user_id):
    """ Given a user id and changes to the user details, update the database.
        """

    q = db.select(User).where(User.id == user_id)
    user = dbx(q).scalars().one()

    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['img_url']

    db.session.commit()

    # TODO: ask why this wouldn't work without a secret key
    flash(f'User {user.first_name} was edited!')

    return redirect('/users')


@app.post('/users/<int:user_id>/delete')
def confirm_user_delete(user_id):
    """ Given a user id, delete the user instance from the database.
        """

    q = db.select(User).where(User.id == user_id)
    user = dbx(q).scalars().one()

    db.session.delete(user)
    db.session.commit()

    flash(f'User {user.first_name} was deleted!')

    return redirect('/users')
