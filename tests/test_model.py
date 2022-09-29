from unittest import TestCase
from app import create_app, db
from app.fake import add_data
from app.model import Users


class TestApp(TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exist(self):
        self.assertFalse(self.app_context is None)

    def test_db_data(self):
        add_data()
        amount_books = len(Users.query.filter_by().all())
        self.assertTrue(amount_books > 10)

    def test_add_data(self):
        user = Users("Kirill", "123")
        db.session.add(user)
        db.session.commit()
        self.assertTrue(Users.query.filter_by(user_name="Kirill").first())
