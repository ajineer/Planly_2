from sqlalchemy_serializer import SerializerMixin
from .. import db


class Event(db.Model, SerializerMixin):

    __tablename__ = "events"

    serialize_rules = ("-calendar",)

    id = db.Column(db.Integer, primary_key=True)
    calendar_id = db.Column(
        db.Integer, db.ForeignKey("calendars.id", ondelete="CASCADE")
    )
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    start = db.Column(db.String, nullable=False)
    end = db.Column(db.String, nullable=False)

    calendar = db.relationship("Calendar", back_populates="events")
