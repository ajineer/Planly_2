from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from config import db, bcrypt


class Task(db.Model, SerializerMixin):

    __tablename__ = "tasks"

    serialize_rules = "-calendar"

    id = db.Column(db.Integer, primary_key=True)
    calendar_id = db.Column(
        db.Integer, db.ForeignKey("calendars.id", ondelete="CASCADE")
    )
    title = db.Column(db.string, nullable=False)
    description = db.Column(db.string)
    date = db.Column(db.string, nullable=False)
    status = db.Column(db.Integer, nullable=False)

    calendar = db.relationship("Calendar", back_populates="tasks")
