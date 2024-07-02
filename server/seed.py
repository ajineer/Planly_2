from models import User, Calendar, Invite, Event, Task, participants
from config import db, app

if __name__ == "__main__":

    with app.app_context():
        User.query.delete()
        Calendar.query.delete()
        Invite.query.delete()
        Event.query.delete()
        Task.query.delete()
        db.session.execute(participants.delete())
        db.session.commit()
        # db.drop_all()
        # db.create_all()
