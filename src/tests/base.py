from flask_testing import TestCase
import sys, os
print(os.getcwd())
sys.path.append(os.getcwd())
from app import create_app
from database.db import db


class BaseTestCase(TestCase):
    def create_app(self):
        return create_app('TEST')

    def setUp(self):
        self.app = self.app.test_client()
        db.drop_all()
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.session.commit()

