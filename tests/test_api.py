from flask_testing import TestCase
from application import create_app, db
import unittest


class BaseTestCase(TestCase):
    def create_app(self):
        return create_app('test')


class TestApi(BaseTestCase):
    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_available(self):
        response = self.client.get("http://localhost:5000/api")
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
