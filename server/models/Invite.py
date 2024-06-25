from sqlalchemy_serializer import SerializerMixin
from config import db


class Invite(db.Model, SerializerMixin):

    __tablename__ = "invites"

    serialize_rules = (
        "-sender",
        "-receiver",
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

    sender = db.relationship(
        "User", foreign_keys=[sender_id], back_populates="sent_invites"
    )
    receiver = db.relationship(
        "User", foreign_keys=[receiver_id], back_populates="received_invites"
    )
    calendars = db.relationship("Calendar", back_populates="invites")
