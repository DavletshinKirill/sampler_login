from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .model import Users


def add_data(user_amount=11):
    faker = Faker()
    counter = 0
    while counter < user_amount:
        user = Users(faker.name(), faker.word())
        db.session.add(user)
        try:
            db.session.commit()
            counter += 1
        except IntegrityError:
            db.session.rollback()
