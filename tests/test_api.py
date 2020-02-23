from flask_testing import TestCase
from application import create_app, db
import unittest
import json
from pathlib import Path


class BaseTestCase(TestCase):
    def create_app(self):
        return create_app('test')


class TestTag(BaseTestCase):
    def setUp(self):
        db.create_all()
        #data_folder = Path("test_data/")
        #file_to_open = data_folder / "tags.json"
        #with open(file_to_open) as json_file:
        #    self.data = json.load(json_file)
        #self.test_success = self.data["validation_success"]
        #self.test_fails = self.data["validation_fail"]

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_available(self):
        """
        Test general availability of the API
        GET /api
        """
        base_url = "http://localhost:5000/api/"
        response = self.client.get(base_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "API operational.")

    def test_create(self):
        """
        Test whether creation of Tags works as intended
        POST /api/tags
        """
        base_url = "http://localhost:5000/api/tags"
        # Tests with no headers and empty payload
        response = self.client.post(base_url)
        self.assertEqual(response.status_code, 400)
        # Tests with correct headers and empty payload
        response = self.client.post(base_url, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        # Tests with wrong header value and empty payload
        response = self.client.post(base_url, content_type="text/plain")
        self.assertEqual(response.status_code, 406)
        # Tests with correct header and payload of length 0
        response = self.client.post(base_url, content_type="application/json", json="")
        self.assertEqual(response.status_code, 400)
        # Tests with correct header and payload with bad json format
        response = self.client.post(base_url, content_type="application/json", json="name=Test")
        self.assertEqual(response.status_code, 415)
        # Should succeed
        for set_ in self.test_success:
            response = self.client.post(base_url, content_type="application/json", json=set_)
            self.assertEqual(response.status_code, 201)
        # Should fail
        for set_ in self.test_fails:
            response = self.client.post(base_url, content_type="application/json", json=set_)
            self.assertGreaterEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
