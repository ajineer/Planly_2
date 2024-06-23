from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from .. import db, bcrypt
from .Participant import particpants


class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    serialize_rules = ("-_password_hash",)

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    _password_hash = db.Column(db.String)

    calendars = db.relationship(
        "Calendar", back_populates="user", cascade="all, delete, delete-orphan"
    )
    invites = db.relationship(
        "Invite", back_populates="user", cascade="all, delete, delete-orphan"
    )

    calendars = db.relationship(
        "Calendar", secondary=particpants, back_populates="users"
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
        if not email or not isinstance(email, str):
            raise ValueError("Email must be a non-empty string.")
        return email
