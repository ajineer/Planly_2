from sqlalchemy_serializer import SerializerMixin
from config import db

class Invite(db.Model, SerializerMixin):

    __tablename__ = "invites"

    serialize_rules = (
        "-user",
        "-calendars",
    )

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    receiver_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    calendar_id = db.Column(
        db.Integer, db.ForeignKey("calendars.id", ondelete="CASCADE")
    )
    status = db.Column(db.String, nullable=False)
    sent_at = db.Column(db.String, nullable=False)

    users = db.relationship("User", back_populates="invites")
    calendars = db.relationship("Calendar", back_populates="invites")
