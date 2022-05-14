import uuid

from flask_cors import cross_origin
from flask import Flask, g, jsonify, request
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)
from werkzeug.security import check_password_hash, generate_password_hash

from .utils import to_camelcase
from .database import init_app
from .models import User


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.settings.Settings")
    JWTManager(app)
    init_app(app)

    @app.route("/signup", methods=["POST", "OPTIONS"])
    @cross_origin(headers=['Content-Type'])
    def signup():
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
        user = User(id=str(uuid.uuid4()), username=username, password=password_hash)
        g.db.session.add(user)
        g.db.session.commit()

        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(identity=user.id)
        return jsonify(
            **dict(to_camelcase({
                "user": {"id": user.id, "username": username},
                "access_token": access_token,
                "refresh_token": refresh_token,
            }))
        )

    @app.route("/signin", methods=["POST", "OPTIONS"])
    @cross_origin(headers=['Content-Type'])
    def signin():
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

        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(identity=user.id)
        return jsonify(
            **dict(to_camelcase({
                "user": {"id": user.id, "username": user.username},
                "access_token": access_token,
                "refresh_token": refresh_token,
            }))
        )

    @app.route("/refresh", methods=["POST", "OPTIONS"])
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @jwt_required(refresh=True)
    def refresh():
        identity = get_jwt_identity()
        user = User.query.filter(User.id == identity).first()
        access_token = create_access_token(identity=identity, fresh=False)
        return jsonify(
            **dict(to_camelcase({
                "access_token": access_token,
                "user": {"id": user.id, "username": user.username}
            }))
        )

    return app
