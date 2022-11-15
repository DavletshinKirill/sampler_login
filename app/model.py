import enum

from flask import abort
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from sqlalchemy import Enum, event


class Permissions(enum.Enum):
    FOLLOW = "FOLLOW"
    COMMENT = "COMMENT"
    WRITE = "WRITE"
    MODERATE = "MODERATE"
    ADMIN = "ADMIN"


# permissions_dictionary = {
#     "ADMIN": [Permissions.ADMIN],
#     "MODERATE": [Permissions.MODERATE, Permissions.ADMIN],
#     "WRITE": [Permissions.MODERATE, Permissions.ADMIN, Permissions.WRITE],
#     "COMMENT": [Permissions.MODERATE, Permissions.ADMIN, Permissions.WRITE, Permissions.COMMENT],
#     "FOLLOW": [Permissions.MODERATE, Permissions.ADMIN, Permissions.WRITE, Permissions.COMMENT, Permissions.FOLLOW]
# }

class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(70), unique=True)
    password = db.Column(db.Text)
    permission = db.Column(Enum(Permissions))

    def __init__(self, name, password, permission=Permissions.WRITE):
        self.user_name = name
        self.hash_password(password)
        self.permission = permission

    def __repr__(self):
        return '<User %r>' % self.id

    def hash_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def can(self, perm):
        return self.permission is not None and self.permission == perm


class Model(db.Model):
    __tablename__ = 'models'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(70), unique=True)
    price = db.Column(db.Integer())


@event.listens_for(Model, "load")
def load_event(user, instance):
    if not current_user.can(Permissions.WRITE):
        abort(403)
