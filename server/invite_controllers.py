from flask_restful import Resource
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from config import db
from models import Calendar, Invite
from datetime import datetime
from uuid import UUID
from utils import (
    verify_data,
    token_required,
    error_messages,
    success_messages,
)


class SentInviteQueryController(Resource):

    @token_required
    @verify_data
    def post(self, email, user_id, data_items):
        invites = Invite.query.filter(
            Invite.sent_at.between(
                datetime.fromisoformat(data_items["start"]),
                datetime.fromisoformat(data_items["end"]),
            ),
            Invite.sender_email == email,
            Invite.sender.id == user_id,
        ).all()
        if not invites:
            return {"error": f"invites {error_messages[404]}"}, 404
        return [i.to_dict() for i in invites], 200


class ReceivedInviteQueryController(Resource):

    @token_required
    @verify_data
    def post(self, email, user_id, data_items):
        invites = Invite.query.filter(
            Invite.sent_at.between(
                datetime.fromisoformat(data_items["start"]),
                datetime.fromisoformat(data_items["end"]),
            ),
            Invite.receiver.id == user_id,
        ).all()
        if not invites:
            return {"error": f"invites {error_messages[404]}"}, 404
        return [i.to_dict() for i in invites], 200


class InviteCreateController(Resource):

    @token_required
    @verify_data
    def post(self, email, user_id, data_items):
        if data_items["receiver_email"] == email:
            return {"error": error_messages[409]}, 409
        invite = Invite.query.filter(
            Invite.sender_email == email,
            Invite.receiver_email == data_items["receiver_email"],
            Invite.calendar_id == UUID(data_items["calendar_string_id"]),
        ).first()
        if invite:
            return {"error": error_messages[409]}, 409
        calendar = Calendar.query.filter(
            Calendar.id == UUID(data_items["calendar_string_id"])
        )
        if not calendar:
            return {"error": error_messages[404]}, 404
        try:
            new_invite = Invite(
                status="pending",
                sent_at=datetime.utcnow(),
                set_permissions=data_items["set_permissions"],
                recipient_name=data_items["recipient_name"],
                calendar_name=data_items["calendar_name"],
                active=1,
                calendar_id=calendar.id,
                sender_email=email,
                receiver_email=data_items["receiver_email"],
            )
            db.session.add(new_invite)
            db.session.commit()
            return new_invite.to_dict(), 201
        except (IntegrityError, SQLAlchemyError) as e:
            return {"error": f"{e}"}, 500


class InvitePatchController(Resource):

    @token_required
    @verify_data
    def patch(self, email, user_id, data_items):
        invite = Invite.query.filter(
            Invite.id == data_items["invite_id"],
            Invite.sender_email == email,
            Invite.sender.id == user_id,
        ).first()
        if not invite:
            return {"error": error_messages[404]}, 404
        if not invite.active:
            return {"error": error_messages[400]}, 400
        try:
            setattr(invite, "status", data_items["status"])
            setattr(invite, "active", 0)
            db.session.add(invite)
            db.session.commit()
            return {"message": success_messages[202]}, 202
        except (IntegrityError, SQLAlchemyError) as e:
            return {"error": f"error: {e}"}, 500


class InviteDeleteController(Resource):

    @token_required
    def delete(self, email, user_id, invite_string_id):
        invite_id = UUID(invite_string_id)
        if not invite_id:
            return {"error": error_messages[400]}, 400
        invite = Invite.query.filter(
            Invite.id == invite_id,
            Invite.sender_email == email,
            Invite.sender.id == user_id,
        ).first()
        if not invite:
            return {"error": error_messages[404]}, 404
        try:
            db.session.delete(invite)
            db.session.commit()
            return {"message": success_messages[204]}, 204
        except (IntegrityError, SQLAlchemyError) as e:
            return {"error": f"error: {e}"}, 500
