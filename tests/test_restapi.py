import pytest
from application import create_app


@pytest.fixture
def app():
    app = create_app()
    return app


def test_my_json_response(client):
    res = client.get("http://localhost:5000/api/tags/")
    assert res.statua_code == 200
