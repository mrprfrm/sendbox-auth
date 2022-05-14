import pytest
from flask_jwt_extended import create_refresh_token


@pytest.fixture
@pytest.mark.usefixtures("user")
def refresh_token(user):
    return create_refresh_token(identity=user.username)


@pytest.mark.usefixtures("app", "client", "refresh_token", "user")
def test_refresh(app, client, refresh_token):
    with app.app_context():
        response = client.post(
            "/refresh",
            headers={"Authorization": f"Bearer {refresh_token}"},
        )
        assert response.status_code == 200
