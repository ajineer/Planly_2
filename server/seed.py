from models import User, Calendar, Invite, Event, Task, Participant, Profile
from config import db, app

if __name__ == "__main__":

    with app.app_context():
        # User.query.delete()
        Participant.query.delete()
        Profile.query.delete()
        Calendar.query.delete()
        Invite.query.delete()
        # Event.query.delete()
        # Task.query.delete()
        db.session.commit()
        # db.drop_all()
        # db.create_all()
