from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError


def use_db():
    from app import db
    return db

class Invite(Resource):
    def post(self):
        from db_models import Invite
        db = use_db()
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
