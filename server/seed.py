from models import User
from config import db, app

if __name__ == "__main__":

    with app.app_context():
        session = db.session
        User.query.delete()
        db.session.commit()
        db.create_all()
