import uuid

from flask import Flask, g, jsonify, request
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)
from werkzeug.security import check_password_hash, generate_password_hash

from .database import init_app
from .models import User


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.settings.Settings")
    JWTManager(app)
    init_app(app)

    @app.route("/register", methods=["POST"])
    def register():
        username = request.json.get("username", None)
        password = request.json.get("password", None)

        if not (username and password):
            return (
                jsonify({"message": "Fields username and password can not be emply"}),
                400,
            )

        user = User.query.filter(User.username == username).first()
        if user is not None:
            return (
                jsonify({"message": "User with current username is already exists"}),
                400,
            )

        password_hash = generate_password_hash(password)
        usr = User(id=str(uuid.uuid4()), username=username, password=password_hash)
        g.db.session.add(usr)
        g.db.session.commit()

        access_token = create_access_token(identity=username, fresh=True)
        refresh_token = create_refresh_token(identity=username)
        return jsonify(access_token=access_token, refresh_token=refresh_token)

    @app.route("/login", methods=["POST"])
    def login():
        username = request.json.get("username", None)
        password = request.json.get("password", None)

        if not (username and password):
            return (
                jsonify({"message": "Fields username and password can not be emply"}),
                400,
            )

        user = User.query.filter(User.username == username).first()
        if user is None or not check_password_hash(user.password, password):
            return (
                jsonify(
                    {"message": "No user with current username or password exists"}
                ),
                401,
            )

        access_token = create_access_token(identity=username, fresh=True)
        refresh_token = create_refresh_token(identity=username)
        return jsonify(access_token=access_token, refresh_token=refresh_token)

    @app.route("/refresh", methods=["POST"])
    @jwt_required(refresh=True)
    def refresh():
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity, fresh=False)
        return jsonify(access_token=access_token)

    return app
