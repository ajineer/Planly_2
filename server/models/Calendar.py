from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from config import db, bcrypt


class Calendar(db.Model, SerializerMixin):

    __tablename__ = "calendars"

    serialize_rules = (
        "-user",
        "-participant",
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    participant_id = db.Column(
        db.Integer, db.ForeignKey("participants.id", ondelete="CASCADE")
    )

    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)

    user = db.relationship("User", back_populates="calendars")
    participant = db.relationship("Participant", back_populates="calendars")
    events = db.relationship(
        "Event", back_populates="calendar", cascade="all, delete, delete-orphan"
    )
    tasks = db.relationship(
        "Task", back_populates="calendar", cascade="all, delete, delete-orphan"
    )
