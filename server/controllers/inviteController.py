from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

# Local imports
from config import app, db, api

# Add your model imports
from models import Invite


class Invite(Resource):
    def post(self):
        if session.get("user_id"):
            try:
                invite = Invite(
                    sender_id=session["user_id"],
                    reciever_id=request.get_json()["receiver_id"],
                    calendar_id=request.get_json()["calendar_id"],
                    sent_at=request.get_json()["sent_at"],
                    status=request.get_json()["status"],
                )
                db.session.add(invite)
                db.session.commit()
                return invite.to_dict(), 201
            except IntegrityError:
                return {"error": "could not create invite"}, 422
        return {"error": "Unauthorized"}
