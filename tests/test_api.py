from flask_testing import TestCase
import requests
from application import create_app, db


class TestApi(TestCase):
    def create_app(self):
        return create_app("test")

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_available(self):
        response = requests.get("http://localhost:5000/api")
        self.assertEquals(response.status_code, 200)
