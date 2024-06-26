from sqlalchemy_serializer import SerializerMixin
from config import db


participants = db.Table(
    "participants",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("calendar_id", db.Integer, db.ForeignKey("calendars.id")),
)


# class Participant(db.Model, SerializerMixin):
#     __tablename__ = "participants"

#     serialize_rules = ""

#     id = db.Column(db.Integer, primary_key=True)
#     role = db.Column(db.String, nullable=False)

#     users = db.relationship(
#         "User", back_populates="participants", cascade="all, delete, delete-orphan"
#     )
#     calendars = db.relationship(
#         "Calendar", back_populates="participants", cascade="all, delete, delete-orphan"
#     )
