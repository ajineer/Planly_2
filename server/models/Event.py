from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from config import db, bcrypt


class Event(db.Model, SerializerMixin):

    __tablename__ = "events"

    serialize_rules = "-calendar"

    id = db.Column(db.Integer, primary_key=True)
    calendar_id = db.Column(
        db.Integer, db.ForeignKey("calendars.id", ondelete="CASCADE")
    )
    name = db.Column(db.string, nullable=False)
    description = db.Column(db.string)
    start = db.Column(db.string, nullable=False)
    end = db.Column(db.string, nullable=False)

    calendar = db.relationship("Calendar", back_populates="events")
