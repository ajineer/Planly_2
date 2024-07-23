from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from config import db
from models import User, Calendar, Event, Task, Invite, Collaboration
import os
from dotenv import load_dotenv
from datetime import timedelta
import jwt
from utils import (
    verify_data,
    token_required,
    error_messages,
    success_messages,
    generate_token,
)
from uuid import UUID
import jwt


class Signup(Resource):

    @verify_data
    def post(self, data_items):
        user = User.query.filter(User.email == data_items["email"]).first()
        if user:
            return {"error": error_messages[409]}, 409
        try:
            new_user = User(
                first_name=data_items["first_name"],
                last_name=data_items["last_name"],
                email=data_items["email"],
            )
            new_user.password_hash = data_items["password"]
            db.session.add(new_user)
            db.session.commit()
            return {"message": success_messages[201]}, 201
        except (IntegrityError, SQLAlchemyError) as e:
            return {"error": f"error: {e}"}, 500


class Login(Resource):

    @verify_data
    def post(self, data_items):

        user = User.query.filter(User.email == data_items["email"]).first()
        if (
            not user
            or not user.authenticate(data_items["password"])
            or not user.email
            or not user.id
        ):
            return {"error": error_messages[401]}, 401
        days = timedelta(days=10)
        token = generate_token(user.email, str(user.id), timeUnits=days)
        return {"message": success_messages[200], "token": str(token)}, 200


class Logout(Resource):

    @token_required
    def post(self, email, user_id):
        token = request.headers.get("Authorization").split(" ")[1]
        if not token:
            return {"error": error_messages[401]}, 401
        seconds = timedelta(seconds=30)
        token = generate_token(email, str(user_id), timeUnits=seconds)
        return {"message": success_messages[204], "token": str(token)}, 200


class CheckSession(Resource):

    @token_required
    def get(self, email, user_id):
        user = User.query.filter(User.id == user_id).first()
        if not user:
            return {"error": error_messages[404]}, 404
        return (
            user.to_dict(
                rules=(
                    "sent_invites",
                    "received_invites",
                )
            ),
            200,
        )


class CalendarController(Resource):

    @token_required
    def get(self, email, user_id):
        calendars = Calendar.query.filter(Calendar.user_id == user_id).all()
        if not calendars:
            return {"error": error_messages[404]}, 404
        return [c.to_dict() for c in calendars], 200

    @token_required
    @verify_data
    def post(self, email, user_id, data_items):
        name, description = data_items["name"], data_items["description"]
        try:
            new_calendar = Calendar(
                user_id=user_id,
                name=name,
                description=description,
            )
            db.session.add(new_calendar)
            db.session.commit()
            return new_calendar.to_dict(), 201
        except (IntegrityError, SQLAlchemyError) as e:
            return {"error": f"error: {e}"}, 500


class CalendarControllerById(Resource):

    @token_required
    def get(self, email, user_id, calendar_string_id):

        calendar_id = UUID(calendar_string_id)
        if not calendar_id:
            return {"error": error_messages[400]}, 400
        calendar = Calendar.query.filter(
            Calendar.id == calendar_id and Calendar.user_id == user_id
        ).first()
        if not calendar:
            return {"error": f" calendar {error_messages[404]} "}, 404
        return calendar.to_dict(), 200

    @token_required
    @verify_data
    def patch(self, email, user_id, calendar_string_id, data_items):
        if not calendar_string_id:
            return {"error": error_messages[400]}, 400
        calendar_id = UUID(calendar_string_id)
        name, description = data_items["name"], data_items["description"]
        calendar = Calendar.query.filter(Calendar.id == calendar_id).first()
        if not calendar:
            return {"error": f"Calendar {error_messages[404]}"}, 404
        try:
            setattr(calendar, "name", name)
            setattr(calendar, "description", description)
            db.session.add(calendar)
            db.session.commit()
            return calendar.to_dict(), 202
        except (IntegrityError, SQLAlchemyError) as e:
            return {"error": f"error: {e}"}, 500

    @token_required
    def delete(self, email, user_id, calendar_string_id):

        if not calendar_string_id:
            return {"error": error_messages[400]}, 400
        calendar_id = UUID(calendar_string_id)
        calendar = Calendar.query.filter(
            Calendar.id == calendar_id and Calendar.user_id == user_id
        ).first()
        if not calendar:
            return {"error": error_messages[404]}, 404
        try:
            db.session.delete(calendar)
            db.session.commit()
            return {"message": success_messages[204]}, 204
        except (IntegrityError, SQLAlchemyError) as e:
            return {"error": f"error: {e}"}, 500


class GuestCalendarControllerById(CalendarControllerById):

    @token_required
    def patch(self, email, user_id, calendar_string_id):
        if not calendar_string_id:
            return {"error": error_messages[400]}, 400
        calendar_id = UUID(calendar_string_id)
        calendar = Calendar.query.filter(Calendar.id == calendar_id).first()
        if not calendar:
            return {"error": error_messages[404]}, 404
        collaboration = Collaboration.query.filter(
            Collaboration.calendar_id == calendar_id
        ).first()
        if not collaboration:
            return {"error": error_messages[404]}, 404
        if collaboration.permissions != "write":
            return {"error": error_messages[401]}, 401
        return super().patch(calendar_string_id=calendar_string_id)


class EventController(Resource):

    @token_required
    @verify_data
    def post(self, email, user_id, data_items):

        calendar_id = UUID(data_items["calendar_string_id"])
        calendar = Calendar.query.filter(Calendar.id == calendar_id).first()
        if not calendar:
            return {"error": error_messages[400]}, 400
        try:
            new_event = Event(
                calendar_id=calendar_id,
                name=data_items["name"],
                description=data_items["description"],
                start=data_items["start"],
                end=data_items["end"],
            )
            db.session.add(new_event)
            db.session.commit()
            return new_event.to_dict(), 200
        except (IntegrityError, SQLAlchemyError) as e:
            return {"error": f"error: {e}"}, 500


class GuestEventController(EventController):

    @token_required
    def post(self, email, user_id, collaboration_string_id):
        collaboration_id = UUID(collaboration_string_id)
        if not collaboration_id:
            return {"error": error_messages[400]}, 400
        collaboration = Collaboration.query.filter(
            Collaboration.id == collaboration_id
        ).first()
        if not collaboration:
            return {"error": error_messages[404]}, 404
        if collaboration.permissions != "write":
            return {"error": error_messages[401]}, 401
        return super().post()


class EventControllerById(Resource):

    @token_required
    @verify_data
    def patch(self, email, user_id, event_string_id, data_items):
        if not event_string_id:
            return {"error": error_messages[400]}, 400
        event_id = UUID(event_string_id)
        event = Event.query.filter(Event.id == event_id).first()
        if not event:
            return {"error": error_messages[404]}, 404
        try:
            setattr(event, "name", data_items["name"])
            setattr(event, "description", data_items["description"])
            setattr(event, "start", data_items["start"])
            setattr(event, "end", data_items["end"])
            db.session.add(event)
            db.session.commit()
            return event.to_dict(), 202
        except (IntegrityError, SQLAlchemyError) as e:
            return {"error": f"error: {e}"}, 500

    @token_required
    def delete(self, email, user_id, event_string_id):
        if not event_string_id:
            return {"error": error_messages[400]}, 400
        event_id = UUID(event_string_id)
        event = Event.query.filter(Event.id == event_id).first()
        if not event:
            return {"error": error_messages[404]}, 404
        try:
            db.session.delete(event)
            db.session.commit()
            return {"message": success_messages[204]}, 204
        except (IntegrityError, SQLAlchemyError) as e:
            return {"error": f"error: {e}"}, 500


class GuestEventControllerById(EventControllerById):

    @token_required
    def patch(self, email, user_id, event_string_id):
        event_id = UUID(event_string_id)
        if not event_id:
            return {"error": error_messages[400]}, 400
        event = Event.query.filter(Event.id == event_id).first()
        if not event:
            return {"error": error_messages[404]}, 404
        collaboration = Collaboration.query.filter(
            Collaboration.calendar_id == event.calendar_id
        ).first()
        if not collaboration:
            return {"error": error_messages[404]}, 404
        if collaboration.permissions != "write":
            return {"error": error_messages[401]}, 401
        return super().patch(event_string_id=event_string_id)

    @token_required
    def delete(self, email, user_id, event_string_id):
        event_id = UUID(event_string_id)
        if not event_id:
            return {"error": error_messages[400]}, 400
        event = Event.query.filter(Event.id == event_id).first()
        if not event:
            return {"error": error_messages[404]}, 404
        collaboration = Collaboration.filter(
            Collaboration.calendar_id == event.calendar_id
        ).first()
        if not collaboration:
            return {"error": error_messages[404]}, 404
        if collaboration.permissions != "write":
            return {"error": error_messages[401]}, 401
        return super().delete()


class TaskController(Resource):

    @token_required
    @verify_data
    def post(self, email, user_id, data_items):
        try:
            # calendar_id = UUID(data_items["calendar_string_id"])
            new_task = Task(
                calendar_id=UUID(data_items["calendar_string_id"]),
                title=data_items["title"],
                description=data_items["description"],
                date=data_items["date"],
                status=data_items["status"],
            )
            db.session.add(new_task)
            db.session.commit()
            return new_task.to_dict(), 201
        except ValueError as e:
            return {"error": f"error: {e}"}, 400
        except (IntegrityError, SQLAlchemyError) as e:
            return {"error": f"error: {e}"}, 500


class GuestTaskController(TaskController):

    @token_required
    def post(self, email, user_id, collaboration_string_id):
        if not collaboration_string_id:
            return {"error": error_messages[400]}, 400
        collaboration_id = UUID(collaboration_string_id)
        collaboration = Collaboration.query.filter(
            Collaboration.id == collaboration_id
        ).first()
        if not collaboration:
            return {"error": error_messages[404]}, 404
        if collaboration.permissions != "write":
            return {"error": error_messages[401]}, 401
        return super().post()


class TaskControllerById(Resource):

    @token_required
    @verify_data
    def patch(self, email, user_id, task_string_id, data_items):
        if not task_string_id:
            return {"error": error_messages[400]}, 400
        task_id = UUID(task_string_id)
        task = Task.query.filter(Task.id == task_id).first()
        if not task:
            return {"error": error_messages[404]}, 404
        try:
            setattr(task, "title", data_items["title"])
            setattr(task, "description", data_items["description"])
            setattr(task, "date", data_items["date"])
            setattr(task, "status", data_items["status"])
            db.session.add(task)
            db.session.commit()
            return task.to_dict(), 202
        except (IntegrityError, SQLAlchemyError) as e:
            return {"error": f"error: {e}"}, 500

    @token_required
    def delete(self, email, user_id, task_string_id):

        if not task_string_id:
            return {"error": error_messages[400]}, 400
        task_id = UUID(task_string_id)
        task = Task.query.filter(Task.id == task_id).first()
        if not task:
            return {"error": error_messages[404]}, 404
        try:
            db.session.delete(task)
            db.session.commit()
            return {"message": success_messages[204]}, 204
        except (IntegrityError, SQLAlchemyError) as e:
            return {"error": f"error: {e}"}, 500


class GuestTaskControllerById(TaskControllerById):

    @token_required
    def patch(self, email, user_id, task_string_id):

        task_id = UUID(task_string_id)
        if not task_id:
            return {"error": error_messages[400]}, 400
        task = Task.query.filter(Task.id == task_id).first()
        if not task:
            return {"error": error_messages[404]}, 404
        collaboration = Collaboration.query.filter(
            Collaboration.calendar_id == task.calendar_id
        ).first()
        if not collaboration:
            return {"error": error_messages[404]}, 404
        if collaboration.permissions != "write":
            return {"error": error_messages[401]}, 401
        return super().patch(task_string_id=task_string_id)

    @token_required
    def delete(self, email, user_id, task_string_id):

        task_id = UUID(task_string_id)
        if not task_id:
            return {"error": error_messages[400]}, 400
        task = Task.query.filter(Task.id == task_id).first()
        if not task:
            return {"error": error_messages[404]}, 404
        collaboration = Collaboration.query.filter(
            Collaboration.calendar_id == task.calendar_id
        ).first()
        if not collaboration:
            return {"error": error_messages[404]}, 404
        if collaboration.permissions != "write":
            return {"error": error_messages[401]}, 401
        return super.delete()


class InviteController(Resource):

    @token_required
    def get(self, email, user_id):
        user = User.query.filter(User.id == user_id).first()
        if not user:
            return {"error": error_messages[404]}, 404
        invites = Invite.query.filter(Invite.sender_email == user.email).all()
        if not invites:
            return {"error": error_messages[404]}, 404
        return [i.to_dict() for i in invites], 200

    @token_required
    @verify_data
    def post(self, email, user_id, data_items):
        user = User.query.filter(User.id == user_id).first()
        invite = Invite.query.filter(
            Invite.sender_email == email
            and Invite.receiver_email == data_items["receiver_email"]
            and Invite.calendar_id == UUID(data_items["calendar_string_id"])
        ).first()
        if invite and invite.active:
            return {"error": error_messages[409]}, 409
        calendar = Calendar.query.filter(
            Calendar.id == UUID(data_items["calendar_string_id"])
        )
        if not calendar:
            return {"error": error_messages[404]}, 404
        try:
            new_invite = Invite(
                status="pending",
                sent_at=data_items["sent_at"],
                set_permissions=data_items["set_permissions"],
                recipient_name=data_items["recipient_name"],
                calendar_name=data_items["calendar_name"],
                active=1,
                calendar_id=UUID(data_items["calendar_string_id"]),
                sender_email=user.email,
                receiver_email=data_items["receiver_email"],
            )
            db.session.add(new_invite)
            db.session.commit()
            return new_invite.to_dict(), 201
        except (IntegrityError, SQLAlchemyError) as e:
            return {"error": f"{e}"}, 500


class InviteControllerById(Resource):

    @token_required
    @verify_data
    def patch(self, email, user_id, invite_string_id, data_items):
        if not invite_string_id:
            return {"error": error_messages[400]}, 400
        invite_id = UUID(invite_string_id)
        invite = Invite.query.filter(Invite.id == invite_id).first()
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

    @token_required
    def delete(self, email, user_id, invite_string_id):
        invite_id = UUID(invite_string_id)
        if not invite_id:
            return {"error": error_messages[400]}, 400
        invite = Invite.query.filter(Invite.id == invite_id).first()
        if not invite:
            return {"error": error_messages[404]}, 404
        try:
            db.session.delete(invite)
            db.session.commit()
            return {"message": success_messages[204]}, 204
        except (IntegrityError, SQLAlchemyError) as e:
            return {"error": f"error: {e}"}, 500


class CollaborationController(Resource):

    @token_required
    def get(self, email, user_id):
        collaborations = Collaboration.query.filter(
            Collaboration.owner_email == email
        ).all()
        if not collaborations:
            return {"error": error_messages[404]}, 404
        return [c.to_dict() for c in collaborations], 200

    @token_required
    @verify_data
    def post(self, email, user_id, data_items):
        calendar_id = UUID(data_items["calendar_string_id"])
        invite = Invite.query.filter(
            Invite.calendar_id == calendar_id and Invite.receiver_email == email
        ).first()
        if not invite:
            return {"error": error_messages[400]}, 400
        if invite.status != "accepted":
            return {"error": error_messages[401]}, 401
        set_permissions = invite.set_permissions
        sender_email = invite.sender_email
        receiver_email = email
        if not set_permissions or not sender_email or not receiver_email:
            return {"error": error_messages[400]}, 400
        try:
            new_collaboration = Collaboration(
                permissions=set_permissions,
                owner_email=sender_email,
                guest_email=receiver_email,
                calendar_id=UUID(data_items["calendar_string_id"]),
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


class GuestCollaborationController(Resource):

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


class CollaborationControllerById(Resource):

    @token_required
    @verify_data
    def patch(self, email, user_id, collaboration_string_id, data_items):

        if not collaboration_string_id:
            return {"error": error_messages[400]}, 400
        collaboration_id = UUID(collaboration_string_id)
        collaboration = Collaboration.query.filter(
            Collaboration.id == collaboration_id
        ).first()
        if not collaboration:
            return {"error": error_messages[404]}, 404
        if not collaboration.owner_email == email:
            return {"error": error_messages[401]}, 401
        try:
            setattr(collaboration, "permissions", data_items["permissions"])
            db.session.add(collaboration)
            db.session.commit()
            return collaboration.to_dict(), 204
        except (IntegrityError, SQLAlchemyError) as e:
            return {"error": f"error: {e}"}, 500

    @token_required
    def delete(self, email, user_id, collaboration_string_id):
        if not collaboration_string_id:
            return {"error": error_messages[400]}, 400
        collaboration_id = UUID(collaboration_string_id)
        collaboration = Collaboration.query.filter(
            Collaboration.id == collaboration_id
        ).first()
        if not collaboration:
            return {"error": error_messages[404]}, 404
        try:
            db.session.delete(collaboration)
            db.session.commit()
            return {"message": success_messages[204]}, 204
        except (IntegrityError, SQLAlchemyError) as e:
            return {"error": f"error: {e}"}, 500
