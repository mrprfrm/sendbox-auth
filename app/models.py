from sqlalchemy.dialects.postgresql import UUID

from .database import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(UUID, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String, nullable=False)
