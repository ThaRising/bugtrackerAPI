from tests import BaseTestCase as FlaskTest
import unittest
from pathlib import Path
import json


class TestTag(FlaskTest):
    def test_create(self):
        """
        Test whether creation of Tags works as intended
        POST /api/tags/
        """
        base_url = f"{self.base_url}tags/"
        # Tests with no headers and empty payload
        response = self.client.post(base_url)
        self.assertEqual(response.status_code, 422)
        # Tests with correct headers and empty payload
        response = self.client.post(base_url, content_type="application/json")
        self.assertEqual(response.status_code, 422)
        # Tests with wrong header value and empty payload
        response = self.client.post(base_url, content_type="text/plain")
        self.assertEqual(response.status_code, 422)
        # Tests with correct header and payload of length 0
        response = self.client.post(base_url, content_type="application/json", json="")
        self.assertEqual(response.status_code, 422)
        # Tests with correct header and payload with bad json format
        response = self.client.post(base_url, content_type="application/json", json="name=Test")
        self.assertEqual(response.status_code, 422)
        # Should succeed
        with open(Path(__file__).parent / "test_data" / "tags.json") as json_file:
            self.test_data = json.load(json_file)
        self.test_success = self.test_data["validation_success"]
        self.test_failure = self.test_data["validation_fail"]
        for set_ in self.test_success:
            response = self.client.post(base_url, content_type="application/json", json=set_)
            self.assertEqual(response.status_code, 200)
        # Should fail
        for set_ in self.test_failure:
            response = self.client.post(base_url, content_type="application/json", json=set_)
            self.assertGreaterEqual(response.status_code, 422)


if __name__ == '__main__':
    unittest.main()
