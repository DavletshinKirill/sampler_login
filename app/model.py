import enum
from flask import session, request
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from sqlalchemy import Enum, event


class Permissions(enum.Enum):
    FOLLOW = "FOLLOW"
    COMMENT = "COMMENT"
    WRITE = "WRITE"
    MODERATE = "MODERATE"
    ADMIN = "ADMIN"

class Users(db.Model, UserMixin):
    __tablename__ = 'user'
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


@event.listens_for(Users, "loaded_as_persistent")
def add_user( session ,  instance ):
    user = Users.query.get(request.args.get('user_id'))
    print(user)
    print('function is called')
    #if permissions_dictionary["ADMIN"]