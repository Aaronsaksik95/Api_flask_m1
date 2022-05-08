import unittest
from config.database import db
from app import app


class TestBase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.db = db.get_db()
    
    def drop_db(self):
        for collection in self.db.list_collection_names():
            self.db.drop_collection(collection)
