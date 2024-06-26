from sqlalchemy_serializer import SerializerMixin
from config import db


class Task(db.Model, SerializerMixin):

    __tablename__ = "tasks"

    serialize_rules = ("-calendar",)

    id = db.Column(db.Integer, primary_key=True)
    calendar_id = db.Column(
        db.Integer, db.ForeignKey("calendars.id", ondelete="CASCADE")
    )
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    date = db.Column(db.String, nullable=False)
    status = db.Column(db.Integer, nullable=False)

    calendar = db.relationship("Calendar", back_populates="tasks")
