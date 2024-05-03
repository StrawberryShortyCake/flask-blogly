"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
dbx = db.session.execute


class User(db.Model):
    """site user"""

    __tablename__ = "users"

    user_id = db.mapped_column(
        db.Integer,
        db.Identity(),
        primary_key=True,
    )

    first_name = db.mapped_column(
        db.String(50),
        nullable=False
    )

    last_name = db.mapped_column(
        db.String(50),
        nullable=False
    )

    image_url = db.mapped_column(
        db.String(1000),
        nullable=False,
        default="https://demofree.sirv.com/nope-not-here.jpg"
    )

    posts = db.relationship(
        "Post",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    """user posts"""

    __tablename__ = "posts"

    id = db.mapped_column(
        db.Integer,
        db.Identity(),
        primary_key=True,
    )

    title = db.mapped_column(
        db.Text,
        nullable=False
    )

    content = db.mapped_column(
        db.Text,
        nullable=False
    )

    created_at = db.mapped_column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    user_id = db.mapped_column(
        db.Integer,
        db.ForeignKey(
            "users.user_id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        )
    )

    user = db.relationship("User", back_populates="posts")
