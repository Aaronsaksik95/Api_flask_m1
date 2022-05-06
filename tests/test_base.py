import unittest
from config.database import db
from app import app


class TestBase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.db = db.get_db()
