import uuid

import pytest
from werkzeug.security import generate_password_hash

from app import create_app
from app.database import db
from app.models import User


@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
@pytest.mark.usefixtures("app")
def client(app):
    return app.test_client()


@pytest.fixture
@pytest.mark.usefixtures("app")
def user(app):
    with app.app_context():
        usr = User(
            id=str(uuid.uuid4()), username="usr", password=generate_password_hash("1")
        )
        db.session.add(usr)
        db.session.commit()
        yield usr
        db.session.delete(usr)
        db.session.commit()
