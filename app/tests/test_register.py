import json

import pytest

from app.models import User


@pytest.mark.usefixtures("app", "client")
def test_register(app, client):
    with app.app_context():
        response = client.post(
            "/register",
            data=json.dumps({"username": "usr", "password": "1"}),
            content_type="application/json",
        )
        assert response.status_code == 200
        assert User.query.filter(User.username == "usr").first() is not None


@pytest.mark.usefixtures("app", "client")
@pytest.mark.parametrize("data", ({"username": "usr"}, {"password": "1"}, {}))
def test_register_with_wrong_data(app, client, data):
    with app.app_context():
        response = client.post(
            "/register", data=json.dumps(data), content_type="application/json"
        )
        assert response.status_code == 400


@pytest.mark.usefixtures("app", "client", "user")
def test_register_with_existing_username(app, client):
    response = client.post(
        "/register",
        data=json.dumps({"username": "usr", "password": "1"}),
        content_type="application/json",
    )
    assert response.status_code == 400
