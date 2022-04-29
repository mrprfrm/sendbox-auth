import json

import pytest


@pytest.mark.usefixtures("app", "client", "user")
def test_login(app, client):
    with app.app_context():
        response = client.post(
            "/login",
            data=json.dumps({"username": "usr", "password": "1"}),
            content_type="application/json",
        )
        assert response.status_code == 200


@pytest.mark.usefixtures("app", "client", "user")
@pytest.mark.parametrize("data", ({"username": "usr"}, {"password": "1"}, {}))
def test_login_with_wrong_data(app, client, data):
    with app.app_context():
        response = client.post(
            "/login", data=json.dumps(data), content_type="application/json"
        )
        assert response.status_code == 400


@pytest.mark.usefixtures("app", "client", "user")
def test_login_with_wrong_password(app, client):
    with app.app_context():
        response = client.post(
            "/login",
            data=json.dumps({"username": "usr", "password": "2"}),
            content_type="application/json",
        )
        assert response.status_code == 401
