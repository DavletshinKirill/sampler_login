from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(70), unique=True)
    password = db.Column(db.Text)

    def __init__(self, name, password):
        self.user_name = name
        self.hash_password(password)

    def __repr__(self):
        return '<User %r>' % self.id

    def hash_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


