from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from uuid import uuid4
from config import db, bcrypt


class Event(db.Model, SerializerMixin):

    __tablename__ = "events"

    serialize_rules = ("-calendar",)

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid4)
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

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid4)
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
    )

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid4)
    sender_email = db.Column(
        db.String, db.ForeignKey("users.email", ondelete="CASCADE")
    )
    receiver_email = db.Column(
        db.String, db.ForeignKey("users.email", ondelete="CASCADE")
    )
    status = db.Column(db.String, nullable=False)
    sent_at = db.Column(db.String, nullable=False)
    set_permissions = db.Column(db.String, nullable=False)
    recipient_name = db.Column(db.String, nullable=False)
    calendar_name = db.Column(db.String, nullable=False)
    calendar_id = db.Column(db.Integer, nullable=False)

    sender = db.relationship(
        "User", foreign_keys=[sender_email], back_populates="sent_invites"
    )
    receiver = db.relationship(
        "User", foreign_keys=[receiver_email], back_populates="received_invites"
    )


class UserCalendar(db.Model, SerializerMixin):

    __tablename__ = "user_calendars"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid4)
    permissions = db.Column(db.String, nullable=False)

    shared_calendars = db.relationship(
        "Calendar",
        back_populates="user_calendars",
        cascade="all, delete, delete-orphan",
    )

    guest_users = db.relationship(
        "User",
        back_populates="user_calendars",
        cascade="all, delete, delete-orphan",
    )

    # def to_dict(self, reciever_email=None):
    #     if reciever_email:
    #         invite = next(
    #             (
    #                 invite
    #                 for invite in self.invites
    #                 if invite.receiver_email == reciever_email
    #             ),
    #             None,
    #         )
    #         if invite and invite.check_status():
    #             return super().to_dict()
    #         else:
    #             data = super().to_dict()
    #             data.pop("shared_calendars", None)
    #             return data
    #     return super().to_dict()


class Calendar(db.Model, SerializerMixin):

    __tablename__ = "calendars"

    serialize_rules = (
        "-user",
        "-user_id",
        "-calendar_id",
        "-user_calendars",
    )

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = db.Column(
        db.UUID(as_uuid=True),
        db.ForeignKey("users.id", ondelete="CASCADE"),
    )
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    shared_id = db.Column(
        db.UUID(as_uuid=True),
        db.ForeignKey("user_calendars.id", ondelete="CASCADE"),
        nullable=True,
    )

    user = db.relationship("User", back_populates="calendars")
    user_calendars = db.relationship("UserCalendar", back_populates="shared_calendars")
    events = db.relationship(
        "Event", back_populates="calendar", cascade="all, delete, delete-orphan"
    )
    tasks = db.relationship(
        "Task", back_populates="calendar", cascade="all, delete, delete-orphan"
    )

    # def to_dict(self, receiver_email=None):
    #     if receiver_email:
    #         participant = self.participant
    #         if participant:
    #             invite = next(
    #                 (
    #                     invite
    #                     for invite in participant.invites
    #                     if invite.receiver_email == receiver_email
    #                 ),
    #                 None,
    #             )
    #             if invite and invite.check_status():
    #                 return super().to_dict()
    #             else:
    #                 data = super().to_dict()
    #                 data.pop("events", None)
    #                 data.pop("tasks", None)
    #                 return data
    #     return super().to_dict()


class User(db.Model, SerializerMixin):

    __tablename__ = "users"

    serialize_rules = (
        "-_password_hash",
        "-calendars",
        "-user_calendars",
    )

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid4)

    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    _password_hash = db.Column(db.String)
    shared_id = db.Column(
        db.UUID(as_uuid=True),
        db.ForeignKey("user_calendars.id", ondelete="CASCADE"),
        nullable=True,
    )

    calendars = db.relationship("Calendar", back_populates="user")
    user_calendars = db.relationship(
        "UserCalendar",
        back_populates="guest_users",
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
