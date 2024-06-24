from config import db

def create_participant_model():

    particpants = db.Table(
        "participants",
        db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
        db.Column("calendar_id", db.Integer, db.ForeignKey("calendars.id")),
    )

    return particpants

participants = create_participant_model()
