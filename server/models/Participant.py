from server.config import db

particpants = db.Table(
    "participants",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("calendar_id", db.Integer, db.ForeignKey("calendars.id")),
)
