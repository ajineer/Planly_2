from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from config import db, bcrypt


class Participant(db.Model, SerializerMixin):

    __tablename__ = "participants"

    serialize_rules = (
        "-users",
        "-calendars",
    )

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String, nullable=False)

    users = db.relationship(
        "User", back_populates="participant", cascade="all, delete, delete-orphan"
    )
    calendars = db.relationship(
        "Calendar", back_populates="participant", cascade="all, delete, delete-orphan"
    )
