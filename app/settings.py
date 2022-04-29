import os
from datetime import timedelta


class Settings:
    SQLALCHEMY_DATABASE_URI = "/".join(
        (
            os.getenv(
                "AUTH_DATABASE_URI",
                "postgresql+psycopg2://postgres:postgres@localhost:5432",
            ),
            os.getenv("AUTH_DATABASE_NAME", "auth"),
        )
    )
    JWT_SECRET_KEY = os.getenv("SECRET_KEY", "secret")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
