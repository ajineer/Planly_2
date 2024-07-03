from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
import uuid
from config import db, bcrypt


participants = db.Table(
    "participants",
    db.Column("user_email", db.String, db.ForeignKey("users.email")),
    db.Column("calendar_id", db.Integer, db.ForeignKey("calendars.id")),
)


class Calendar(db.Model, SerializerMixin):

    __tablename__ = "calendars"

    serialize_rules = (
        "-user",
        "-invites",
        "-user_id",
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)

    user = db.relationship("User", back_populates="calendars")
    user_group = db.relationship(
        "User", secondary="participants", back_populates="calendar_group"
    )

    invites = db.relationship("Invite", back_populates="calendars")
    events = db.relationship(
        "Event", back_populates="calendar", cascade="all, delete, delete-orphan"
    )
    tasks = db.relationship(
        "Task", back_populates="calendar", cascade="all, delete, delete-orphan"
    )


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


class Invite(db.Model, SerializerMixin):

    __tablename__ = "invites"

    serialize_rules = (
        "-sender",
        "-receiver",
        "-calendars",
    )

    id = db.Column(db.Integer, primary_key=True)
    sender_email = db.Column(
        db.String, db.ForeignKey("users.email", ondelete="CASCADE")
    )
    receiver_email = db.Column(
        db.String, db.ForeignKey("users.email", ondelete="CASCADE")
    )
    calendar_id = db.Column(
        db.Integer, db.ForeignKey("calendars.id", ondelete="CASCADE")
    )
    status = db.Column(db.String, nullable=False)
    sent_at = db.Column(db.String, nullable=False)

    sender = db.relationship(
        "User", foreign_keys=[sender_email], back_populates="sent_invites"
    )
    receiver = db.relationship(
        "User", foreign_keys=[receiver_email], back_populates="received_invites"
    )
    calendars = db.relationship("Calendar", back_populates="invites")


class User(db.Model, SerializerMixin):

    __tablename__ = "users"

    serialize_rules = (
        "-_password_hash",
        "-calendars",
        "-calendar_group",
        "-id",
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
        foreign_keys=[Invite.sender_email],
        back_populates="sender",
        cascade="all, delete, delete-orphan",
    )
    received_invites = db.relationship(
        "Invite",
        foreign_keys=[Invite.receiver_email],
        back_populates="receiver",
        cascade="all, delete, delete-orphan",
    )

    calendar_group = db.relationship(
        "Calendar", secondary="participants", back_populates="user_group"
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
