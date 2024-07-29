from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError, SQLAlchemyError, NoResultFound
from config import db
from models import User, Calendar, Event, Task, Invite, Collaboration
from datetime import datetime, timedelta
from uuid import UUID
from utils import (
    verify_data,
    token_required,
    error_messages,
    success_messages,
    generate_token,
    verify_collaboration,
)


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
            return {"error": f"{e}"}, 500


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
            return {"error": f"user {error_messages[404]}"}, 404

        days = timedelta(days=10)
        token = generate_token(user.email, str(user.id), timeUnits=days)
        return {"message": success_messages[200], "token": str(token)}, 200


class CalendarQueryCreateController(Resource):

    @token_required
    def get(self, email, user_id):
        calendars = Calendar.query.filter(Calendar.user_id == user_id).all()
        if not calendars:
            return {"error": f"calendars {error_messages[404]}"}, 404
        return [c.to_dict() for c in calendars], 200

    @token_required
    @verify_data
    def post(self, email, user_id, data_items):
        try:
            new_calendar = Calendar(
                user_id=user_id,
                name=data_items["name"],
                description=data_items["description"],
            )
            db.session.add(new_calendar)
            db.session.commit()
            return new_calendar.to_dict(), 201
        except (IntegrityError, SQLAlchemyError) as e:
            return {"error": f"{e}"}, 500


class CalendarPatchController(Resource):

    @token_required
    @verify_data
    def patch(self, email, user_id, data_items):

        calendar_id = UUID(data_items["calendar_string_id"])
        if not calendar_id:
            return {"error": error_messages[400]}, 400
        calendar = Calendar.query.filter(
            Calendar.user_id == user_id, Calendar.id == calendar_id
        ).first()
        if not calendar:
            return {"error": f"calendar {error_messages[404]}"}, 404
        try:
            setattr(calendar, "name", data_items["name"])
            setattr(calendar, "description", data_items["description"])
            db.session.add(calendar)
            db.session.commit()
            return calendar.to_dict(), 202
        except (IntegrityError, SQLAlchemyError) as e:
            return {"error": f"{e}"}, 500


class CalendarDeleteController(Resource):

    @token_required
    def delete(self, email, user_id, calendar_string_id):

        if not calendar_string_id:
            return {"error": error_messages[400]}, 400
        calendar_id = UUID(calendar_string_id)
        calendar = Calendar.query.filter(
            Calendar.user_id == user_id,
            Calendar.id == calendar_id,
            Calendar.user_id == user_id,
        ).first()
        if not calendar:
            return {"error": f"calendar {error_messages[404]}"}, 404
        try:
            db.session.delete(calendar)
            db.session.commit()
            return {"message": success_messages[204]}, 204
        except (IntegrityError, SQLAlchemyError) as e:
            return {"error": f"{e}"}, 500


class EventQueryController(Resource):
    @token_required
    @verify_data
    def post(self, email, user_id, data_items):
        calendars = Calendar.query.filter(Calendar.user_id == user_id).all()
        if not calendars:
            return {"error": error_messages[401]}, 401

        events = Event.query.filter(
            Event.start.between(
                datetime.fromisoformat(data_items["start"]),
                datetime.fromisoformat(data_items["end"]),
            ),
            Event.calendar_id.in_([c.id for c in calendars]),
        ).all()
        if not events:
            return {"error": f"events {error_messages[404]}"}, 404
        return [e.to_dict() for e in events], 200


class EventCreateController(Resource):

    @token_required
    @verify_data
    def post(self, email, user_id, data_items):
        try:
            calendar = Calendar.query.filter(
                Calendar.id == UUID(data_items["calendar_string_id"]),
                Calendar.user_id == user_id,
            ).first()
            new_event = Event(
                calendar_id=calendar.id,
                name=data_items["name"],
                description=data_items["description"],
                start=datetime.fromisoformat(data_items["start"]),
                end=datetime.fromisoformat(data_items["end"]),
            )
            db.session.add(new_event)
            db.session.commit()
            return new_event.to_dict(), 200
        except ValueError as e:
            return {"error": str(e)}
        except (IntegrityError, SQLAlchemyError) as e:
            return {"error": f"{e}"}, 500


class GuestEventQueryController(Resource):

    @token_required
    @verify_collaboration
    def post(self, email, user_id, data_items, calendar):
        events = Event.query.filter(
            Event.start.between(
                datetime.fromisoformat(data_items["start"]),
                datetime.fromisoformat(data_items["end"]),
            ),
            Event.calendar_id == calendar.calendar_id,
        ).all()
        if not events:
            return {"error": f"events {error_messages[404]}"}, 404
        return [e.to_dict() for e in events], 200


class GuestEventCreateController(Resource):

    @token_required
    @verify_collaboration
    def post(self, email, user_id, data_items, calendar):
        try:
            new_event = Event(
                calendar_id=calendar.id,
                name=data_items["name"],
                description=data_items["description"],
                start=datetime.fromisoformat(data_items["start"]),
                end=datetime.fromisoformat(data_items["end"]),
            )
            db.session.add(new_event)
            db.session.commti()
            return new_event.to_dict(), 201
        except ValueError as e:
            return {"error": str(e)}
        except (IntegrityError, SQLAlchemyError) as e:
            return {"error": f"error: {e}"}, 500


class EventPatchController(Resource):

    @token_required
    @verify_data
    def patch(self, email, user_id, data_items):

        calendar = Calendar.query.filter(
            Calendar.user_id == user_id,
            Calendar.id == UUID(data_items["calendar_string_id"]),
        ).first()
        if not calendar:
            return {"error": f"calendar {error_messages[404]}"}, 404
        event = Event.query.filter(
            Event.id == UUID(data_items["event_string_id"])
        ).first()
        if not event:
            return {"error": error_messages[404]}, 404

        try:
            setattr(event, "name", data_items["name"])
            setattr(event, "description", data_items["description"])
            setattr(event, "start", datetime.fromisoformat(data_items["start"]))
            setattr(event, "end", datetime.fromisoformat(data_items["end"]))
            db.session.add(event)
            db.session.commit()
            return event.to_dict(), 202
        except (IntegrityError, SQLAlchemyError) as e:
            return {"error": f"error: {e}"}, 500


class EventDeleteController(Resource):

    @token_required
    def delete(self, email, user_id, event_string_id):
        if not event_string_id:
            return {"error": error_messages[400]}, 400
        event_id = UUID(event_string_id)
        event = Event.query.filter(Event.id == event_id).first()
        if not event:
            return {"error": error_messages[404]}, 404
        calendar = Calendar.query.filter(
            Calendar.id == event.calendar_id, Calendar.user_id == user_id
        ).first()
        if not calendar:
            return {"error": f"calendar {error_messages[404]}"}, 404
        try:
            db.session.delete(event)
            db.session.commit()
            return {"message": success_messages[204]}, 204
        except (IntegrityError, SQLAlchemyError) as e:
            return {"error": f"error: {e}"}, 500


class GuestEventPatchDeleteController(Resource):

    @token_required
    @verify_collaboration
    def patch(self, email, user_id, data_items, calendar):

        event = Event.query.filter(
            Event.id == UUID(data_items["event_string_id"]),
            Event.calendar_id == calendar.id,
        ).first()
        if not event:
            return {"error": error_messages[404]}, 404
        try:
            setattr(event, "name", data_items["name"])
            setattr(event, "description", data_items["description"])
            setattr(event, "start", datetime.fromisoformat(data_items["start"]))
            setattr(event, "end", datetime.fromisoformat(data_items["end"]))
            db.session.add(event)
            db.session.commit()
            return event.to_dict(), 202
        except (IntegrityError, SQLAlchemyError) as e:
            return {"error": f"error: {e}"}, 500

    @token_required
    @verify_collaboration
    def delete(self, email, user_id, data_items, calendar):

        event = Event.query.filter(
            Event.id == UUID(data_items["event_string_id"]),
            Event.calendar_id == calendar.id,
        ).first()
        if not event:
            return {"error": error_messages[404]}, 404
        try:
            db.session.delete(event)
            db.session.commit()
            return {"message": success_messages[204]}, 204
        except (IntegrityError, SQLAlchemyError) as e:
            return {"error": f"error: {e}"}, 500


class TaskQueryController(Resource):

    @token_required
    @verify_data
    def post(self, email, user_id, data_items):
        calendars = Calendar.query.filter(Calendar.user_id == user_id).all()
        if not calendars:
            return {"error": f"calendars {error_messages[404]}"}, 404
        tasks = Task.query.filter(
            Task.date.between(
                datetime.fromisoformat(data_items["start"]),
                datetime.fromisoformat(data_items["end"]),
            ),
            Task.calendar_id.in_([UUID(c.id) for c in calendars]),
        ).all()
        if not tasks:
            return {"error": f"tasks {error_messages[404]}"}, 404
        return [t.to_dict() for t in tasks], 200


class TaskCreateController(Resource):

    @token_required
    @verify_data
    def post(self, email, user_id, data_items):
        calendar = Calendar.query.filter(
            Calendar.id == UUID(data_items["calendar_string_id"]),
            Calendar.user_id == user_id,
        ).first()
        if not calendar:
            return {"error": f"calendar {error_messages[404]}"}, 404
        try:
            new_task = Task(
                calendar_id=UUID(data_items["calendar_string_id"]),
                title=data_items["title"],
                description=data_items["description"],
                date=datetime.fromisoformat(data_items["date"]),
                status=data_items["status"],
            )
            db.session.add(new_task)
            db.session.commit()
            return new_task.to_dict(), 201
        except ValueError as e:
            return {"error": f"error: {e}"}, 400
        except (IntegrityError, SQLAlchemyError) as e:
            return {"error": f"error: {e}"}, 500


class GuestTaskCreateController(Resource):

    @token_required
    @verify_collaboration
    def post(self, email, user_id, data_items, calendar):
        try:
            new_task = Task(
                calendar_id=calendar.id,
                title=data_items["title"],
                description=data_items["description"],
                date=datetime.fromisoformat(data_items["date"]),
                status=data_items["status"],
            )
            db.session.add(new_task)
            db.session.commit()
            return new_task.to_dict(), 201
        except ValueError as e:
            return {"error": f"error: {e}"}, 400
        except (IntegrityError, SQLAlchemyError) as e:
            return {"error": f"error: {e}"}, 500


class TaskPatchController(Resource):

    @token_required
    @verify_data
    def patch(self, email, user_id, data_items):
        task = Task.query.filter(Task.id == UUID(data_items["task_string_id"])).first()
        if not task:
            return {"error": f"task {error_messages[404]}"}, 404
        calendar = Calendar.query.filter(
            Calendar.user_id == user_id, Calendar.id == task.calendar_id
        ).first()
        if not calendar:
            return {"error": f"calendar {error_messages[404]}"}, 404
        try:
            setattr(task, "title", data_items["title"])
            setattr(task, "description", data_items["description"])
            setattr(task, "date", datetime.fromisoformat(data_items["date"]))
            setattr(task, "status", data_items["status"])
            db.session.add(task)
            db.session.commit()
            return task.to_dict(), 202
        except (IntegrityError, SQLAlchemyError) as e:
            return {"error": f"error: {e}"}, 500


class TaskDeleteController(Resource):

    @token_required
    @verify_data
    def delete(self, email, user_id, task_string_id):

        task = Task.query.filter(Task.id == UUID(task_string_id)).first()
        if not task:
            return {"error": error_messages[404]}, 404
        calendar = Calendar.query.filter(
            Calendar.id == task.calendar_id, Calendar.user_id == user_id
        ).first()
        if not calendar:
            return {"error": f"calendar {error_messages[404]}"}, 404
        try:
            db.session.delete(task)
            db.session.commit()
            return {"message": success_messages[204]}, 204
        except (IntegrityError, SQLAlchemyError) as e:
            return {"error": f"error: {e}"}, 500


class GuestTaskPatchDeleteController(Resource):

    @token_required
    @verify_collaboration
    def patch(self, email, user_id, data_items, calendar):

        task = Task.query.filter(
            Task.calendar_id == calendar.id,
            Task.id == UUID(data_items["task_string_id"]),
        ).first()
        try:
            setattr(task, "title", data_items["title"])
            setattr(task, "description", data_items["description"])
            setattr(task, "date", datetime.fromisoformat(data_items["date"]))
            setattr(task, "status", data_items["status"])
            db.session.add(task)
            db.session.commit()
            return task.to_dict(), 202
        except (IntegrityError, SQLAlchemyError) as e:
            return {"error": f"error: {e}"}, 500

    @token_required
    @verify_collaboration
    def delete(self, email, user_id, data_items, calendar):

        task = Task.query.filter(
            Task.id == UUID(data_items["task_string_id"]),
            Task.calendar_id == calendar.id,
        ).first()

        try:
            db.session.delete(task)
            db.session.commit()
            return {"message": success_messages[204]}, 204
        except (IntegrityError, SQLAlchemyError) as e:
            return {"error": f"error: {e}"}, 500


class InviteQueryController(Resource):

    @token_required
    @verify_data
    def post(self, email, user_id, data_items):
        invites = Invite.query.filter(
            Invite.sent_at.between(
                datetime.fromisoformat(data_items["start"]),
                datetime.fromisoformat(data_items["end"]),
            ),
            Invite.sender.id == user_id,
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
            Invite.id == data_items["invite_id"], Invite.sender_email == email
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
            Invite.id == invite_id, Invite.sender_email == email
        ).first()
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
        invite = Invite.query.filter(
            Invite.calendar_id == calendar.id,
            Invite.receiver_email == email,
            Invite.id == UUID(data_items["invite_string_id"]),
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
