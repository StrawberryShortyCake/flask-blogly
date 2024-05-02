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
    # sorted_users_full_name = sorted_users.map((user_instance)=>{

    # })

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

    # behind the scene: dict = {'/users': show_all_users}
    # Server listens to request
    # Flask dispatches the request
