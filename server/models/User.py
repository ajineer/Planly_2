from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from .Participant import participants
from .Invite import Invite

from config import db, bcrypt


class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    serialize_rules = (
        "-_password_hash",
        "-calendars",
        "-calendars_group",
        "-sent_invites",
        "-received_invites",
    )

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    _password_hash = db.Column(db.String)

    calendars = db.relationship(
        "Calendar", back_populates="user", cascade="all, delete, delete-orphan"
    )
    sent_invites = db.relationship(
        "Invite",
        foreign_keys=[Invite.sender_id],
        back_populates="sender",
        cascade="all, delete, delete-orphan",
    )
    received_invites = db.relationship(
        "Invite",
        foreign_keys=[Invite.receiver_id],
        back_populates="receiver",
        cascade="all, delete, delete-orphan",
    )

    calendars_group = db.relationship(
        "Calendar", secondary=participants, back_populates="users"
    )

    @hybrid_property
    def password_hash(self):
        raise Exception("Password hashes may not be viewed")

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode("utf-8"))
        self._password_hash = password_hash.decode("utf-8")

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode("utf-8"))

    @validates("email")
    def validate_email(self, key, email):
        if "@" not in email or not email:
            raise ValueError("Email must be a non-empty string.")
        return email
