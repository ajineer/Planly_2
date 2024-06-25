from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from config import db


class Invite(Resource):
    def get(self):
        from models import Invite

        if session.get("user_id"):
            invites = Invite.query.filter(
                Invite.receiver_id == session["user_id"]
            ).all()
            if invites:
                return [i.to_dict() for i in invites], 200
            return {"error": "No invites found"}, 404
        return {"error": "Unauthorized"}, 401

    def post(self):
        from models import Invite

        if session.get("user_id"):
            try:
                invite = Invite(
                    sender_id=session["user_id"],
                    receiver_id=request.get_json()["receiver_id"],
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
