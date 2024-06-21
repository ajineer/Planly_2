from sqlalchemy_serializer import SerializerMixin
from ..models.Participant import particpants
from ..config import db


class Calendar(db.Model, SerializerMixin):

    __tablename__ = "calendars"

    serialize_rules = ("-user",)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))

    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)

    user = db.relationship("User", back_populates="calendars")
    users = db.relationship("User", secondary=particpants, back_populates="calendars")
    events = db.relationship(
        "Event", back_populates="calendar", cascade="all, delete, delete-orphan"
    )
    tasks = db.relationship(
        "Task", back_populates="calendar", cascade="all, delete, delete-orphan"
    )
