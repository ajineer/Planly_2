from flask_restful import Resource
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from config import db
from models import Calendar, Invite, Collaboration
from uuid import UUID
from utils import (
    verify_data,
    token_required,
    error_messages,
    success_messages,
)


class CollaborationController(Resource):

    @token_required
    def get(self, email, user_id):
        collaborations = Collaboration.query.filter(
            Collaboration.owner_email == email, Collaboration.owner.id == user_id
        ).all()
        if not collaborations:
            return {"error": error_messages[404]}, 404
        return [c.to_dict() for c in collaborations], 200

    @token_required
    @verify_data
    def post(self, email, user_id, data_items):
        invite = Invite.query.filter(
            Invite.calendar_id == calendar.id,
            Invite.receiver_email == email,
            Invite.id == UUID(data_items["invite_string_id"]),
            Invite.receiver.id == user_id,
        ).first()
        if not invite:
            return {"error": error_messages[400]}, 400
        if invite.status != "accepted":
            return {"error": error_messages[401]}, 401
        calendar = Calendar.query.filter(Calendar.id == invite.calendar_id).first()
        if not calendar:
            return {"error": f"calendar {error_messages[404]}"}, 404
        try:
            new_collaboration = Collaboration(
                permissions=invite.set_permissions,
                owner_email=invite.sender_email,
                guest_email=invite.receiver_email,
                calendar_id=calendar.id,
            )
            db.session.add(new_collaboration)
            db.session.commit()
            return (
                new_collaboration.to_dict(
                    rules=(
                        "calendar",
                        "-owner_email",
                    )
                ),
                201,
            )
        except (IntegrityError, SQLAlchemyError) as e:
            return {"error": f"error: {e}"}, 500


class GuestCollaborationQueryController(Resource):
    @token_required
    def get(self, email, user_id):
        collaborations = Collaboration.query.filter(
            Collaboration.guest_email == email
        ).all()
        if not collaborations:
            return {"error": error_messages[404]}, 404
        return [
            c.to_dict(
                rules=(
                    "calendar",
                    "-guest_email",
                )
            )
            for c in collaborations
        ], 200


class GuestCollaborationDeleteController(Resource):

    @token_required
    def delete(self, email, user_id, collaboration_string_id):
        collaboration_id = UUID(collaboration_string_id)
        if not collaboration_id:
            return {"error": error_messages[400]}, 400
        collaboration = Collaboration.query.filter(
            Collaboration.id == collaboration_id, Collaboration.guest_email == email
        ).first()
        if not collaboration:
            return {"error": f"collaboration {error_messages[404]}"}, 404
        try:
            db.session.delete(collaboration)
            db.session.commit()
            return {"message": success_messages[204]}, 204
        except (IntegrityError, SQLAlchemyError) as e:
            return {"error": f"error: {e}"}, 500


class CollaborationPatchController(Resource):

    @token_required
    @verify_data
    def patch(self, email, user_id, data_items):

        collaboration = Collaboration.query.filter(
            Collaboration.id == data_items(data_items["collaboration_id"]),
            Collaboration.owner_email == email,
        ).first()
        if not collaboration:
            return {"error": error_messages[404]}, 404
        try:
            setattr(collaboration, "permissions", data_items["permissions"])
            db.session.add(collaboration)
            db.session.commit()
            return collaboration.to_dict(), 204
        except (IntegrityError, SQLAlchemyError) as e:
            return {"error": f"error: {e}"}, 500


class CollaborationDeleteController(Resource):

    @token_required
    def delete(self, email, user_id, collaboration_string_id):
        if not collaboration_string_id:
            return {"error": error_messages[400]}, 400
        collaboration_id = UUID(collaboration_string_id)
        collaboration = Collaboration.query.filter(
            Collaboration.id == collaboration_id, Collaboration.owner_email == email
        ).first()
        if not collaboration:
            return {"error": error_messages[404]}, 404
        try:
            db.session.delete(collaboration)
            db.session.commit()
            return {"message": success_messages[204]}, 204
        except (IntegrityError, SQLAlchemyError) as e:
            return {"error": f"error: {e}"}, 500
