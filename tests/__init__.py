from flask_testing import TestCase
from application import create_app, db


class BaseTestCase(TestCase):
    def create_app(self):
        return create_app('test')

    def setUp(self):
        db.create_all()
        self.base_url = "http://localhost:5000/api/"

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_available(self):
        """
        Test general availability of the API
        GET /api/
        """
        response = self.client.get("http://localhost:5000/")
        self.assertEqual(response.status_code, 200)


__all__ = ["BaseTestCase"]
