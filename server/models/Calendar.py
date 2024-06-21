from sqlalchemy_serializer import SerializerMixin
from ..config import db
from ..models.Participant import particpants


class Calendar(db.Model, SerializerMixin):

    __tablename__ = "calendars"

    serialize_rules = ("-user",)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    # participant_id = db.Column(
    #     db.Integer,
    #     db.ForeignKey("participants.id", ondelete="CASCADE"),
    #     nullable=True,
    # )

    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)

    user = db.relationship("User", back_populates="calendars")
    users = db.relationship("User", secondary=particpants, back_populates="calendars")
    # participant = db.relationship("Participant", back_populates="calendars")
    events = db.relationship(
        "Event", back_populates="calendar", cascade="all, delete, delete-orphan"
    )
    tasks = db.relationship(
        "Task", back_populates="calendar", cascade="all, delete, delete-orphan"
    )
