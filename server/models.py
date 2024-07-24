from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from uuid import uuid4
from config import db, bcrypt


class Event(db.Model, SerializerMixin):

    __tablename__ = "events"

    serialize_rules = ("-calendar",)

    id = db.Column(
        db.UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    calendar_id = db.Column(
        db.UUID(as_uuid=True),
        db.ForeignKey(
            "calendars.id",
            ondelete="CASCADE",
        ),
    )
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)

    calendar = db.relationship("Calendar", back_populates="events")


class Task(db.Model, SerializerMixin):

    __tablename__ = "tasks"

    serialize_rules = ("-calendar",)

    id = db.Column(
        db.UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Integer, nullable=False)

    calendar_id = db.Column(
        db.UUID(as_uuid=True),
        db.ForeignKey(
            "calendars.id",
            ondelete="CASCADE",
        ),
    )

    calendar = db.relationship("Calendar", back_populates="tasks")


class Invite(db.Model, SerializerMixin):

    __tablename__ = "invites"

    serialize_rules = (
        "-sender",
        "-receiver",
    )

    id = db.Column(
        db.UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    status = db.Column(db.String, nullable=False)
    sent_at = db.Column(db.DateTime, nullable=False)
    set_permissions = db.Column(db.String, nullable=False)
    recipient_name = db.Column(db.String, nullable=False)
    calendar_name = db.Column(db.String, nullable=False)
    active = db.Column(db.Integer, nullable=False)
    calendar_id = db.Column(
        db.UUID(as_uuid=True),
        db.ForeignKey("calendars.id"),
        nullable=False,
    )
    sender_email = db.Column(
        db.String,
        db.ForeignKey(
            "users.email",
            ondelete="CASCADE",
        ),
    )
    receiver_email = db.Column(
        db.String,
        db.ForeignKey(
            "users.email",
            ondelete="CASCADE",
        ),
    )

    sender = db.relationship(
        "User",
        foreign_keys=[sender_email],
        back_populates="sent_invites",
    )
    receiver = db.relationship(
        "User",
        foreign_keys=[receiver_email],
        back_populates="received_invites",
    )


class Collaboration(db.Model, SerializerMixin):

    __tablename__ = "collaborations"

    serialize_rules = (
        "-owner",
        "-guest",
    )

    id = db.Column(
        db.UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    permissions = db.Column(db.String, nullable=False)
    owner_email = db.Column(
        db.String,
        db.ForeignKey(
            "users.email",
            ondelete="CASCADE",
        ),
    )
    guest_email = db.Column(
        db.String,
        db.ForeignKey(
            "users.email",
            ondelete="CASCADE",
        ),
    )
    calendar_id = db.Column(
        db.UUID(as_uuid=True),
        db.ForeignKey(
            "calendars.id",
            ondelete="CASCADE",
        ),
    )
    owner = db.relationship(
        "User",
        foreign_keys=[owner_email],
        back_populates="owned_collaborations",
    )
    guest = db.relationship(
        "User",
        foreign_keys=[guest_email],
        back_populates="guest_collaborations",
    )

    calendar = db.relationship(
        "Calendar",
        back_populates="collaborations",
    )


class Calendar(db.Model, SerializerMixin):

    __tablename__ = "calendars"

    serialize_rules = (
        "-user",
        "-user_id",
        "-collaborations",
        "-events",
        "-tasks",
    )

    id = db.Column(
        db.UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    user_id = db.Column(
        db.UUID(as_uuid=True),
        db.ForeignKey("users.id", ondelete="CASCADE"),
    )
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)

    user = db.relationship("User", back_populates="calendars")

    collaborations = db.relationship(
        "Collaboration",
        back_populates="calendar",
        cascade="all, delete, delete-orphan",
    )
    events = db.relationship(
        "Event",
        back_populates="calendar",
        cascade="all, delete, delete-orphan",
    )
    tasks = db.relationship(
        "Task",
        back_populates="calendar",
        cascade="all, delete, delete-orphan",
    )


class User(db.Model, SerializerMixin):

    __tablename__ = "users"

    serialize_rules = (
        "-_password_hash",
        "-calendars",
        "-owned_collaborations",
        "-guest_collaborations",
    )

    id = db.Column(
        db.UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    _password_hash = db.Column(db.String)

    calendars = db.relationship("Calendar", back_populates="user")

    owned_collaborations = db.relationship(
        "Collaboration",
        foreign_keys=[Collaboration.owner_email],
        back_populates="owner",
        cascade="all, delete, delete-orphan",
    )

    guest_collaborations = db.relationship(
        "Collaboration",
        foreign_keys=[Collaboration.guest_email],
        back_populates="guest",
        cascade="all, delete, delete-orphan",
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
