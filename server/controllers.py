from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from config import db
from models import User, Calendar, Event, Task, Invite, Collaboration
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import jwt
from utils import decode_token, error_messages, success_messages
from uuid import UUID


class Signup(Resource):

    def post(self):
        data = request.get_json()
        if not data:
            return {"error": error_messages[401]}, 401
        email = data["email"]
        first_name = data["first_name"]
        last_name = data["last_name"]
        password = data["password"]

        if not email or not password or not first_name or not last_name:
            return {"error": error_messages[401]}, 401
        user = User.query.filter(User.email == email).first()
        if user:
            return {"error": error_messages[409]}, 409
        try:
            new_user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
            )
            new_user.password_hash = password
            db.session.add(new_user)
            db.session.commit()
            return {"message": success_messages[201]}, 201
        except IntegrityError:
            return {"error": error_messages[422]}, 422


class Login(Resource):

    def post(self):

        data = request.get_json()
        if not data:
            return {"error": error_messages[400]}, 400

        email = data["email"]
        password = data["password"]
        if not password or not email:
            return {"error": error_messages[400]}, 400
        user = User.query.filter(User.email == email).first()
        if not user or not user.authenticate(password) or not user.email or not user.id:
            return {"error": error_messages[401]}, 401

        token = self.generate_token(user.email, str(user.id))
        session["user_token"] = token
        return {"message": success_messages[200]}, 200

    def generate_token(self, email, id):

        load_dotenv()
        secret_key = os.getenv("SECRET_KEY")
        payload = {
            "email": email,
            "user_id": id,
            "exp": datetime.utcnow() + timedelta(days=7),
        }
        token = jwt.encode(payload, secret_key)
        return token


class CheckSession(Resource):

    def get(self):
        if not session.get("user_token"):
            return {"error": error_messages[401]}, 401
        email, user_id = decode_token(session["user_token"])
        if not email or not user_id:
            return {"error": error_messages[401]}, 401
        user = User.query.filter(User.id == user_id).first()
        if not user:
            return {"error": error_messages[404]}, 404
        return (user.to_dict(), 200)


class Logout(Resource):

    def delete(self):
        if not session.get("user_token"):
            return {"error": error_messages[401]}, 401
        session["user_token"] = None
        return {"message": success_messages[204]}, 204


class CalendarController(Resource):

    def get(self):
        if not session.get("user_token"):
            return {"error": error_messages[401]}, 401
        email, user_id = decode_token(session["user_token"])
        if not user_id:
            return {"error": error_messages[401]}, 401
        calendars = Calendar.query.filter(Calendar.user_id == user_id).all()
        if not calendars:
            return {"error": error_messages[404]}, 404
        return [
            c.to_dict(
                rules=(
                    "tasks",
                    "events",
                    "collaborations",
                )
            )
            for c in calendars
        ], 200

    def post(self):
        if not session.get("user_token"):
            return {"error": error_messages[401]}, 401
        email, user_id = decode_token(session["user_token"])
        if not user_id:
            return {"error": error_messages[401]}, 401
        data = request.get_json()
        if not data:
            return {"error": error_messages[400]}, 400
        name = data["name"]
        description = data["description"]
        if not name or not description:
            return {"error": error_messages[400]}, 400
        try:
            new_calendar = Calendar(
                user_id=user_id,
                name=data["name"],
                description=data["description"],
            )
            db.session.add(new_calendar)
            db.session.commit()
            return new_calendar.to_dict(), 201
        except IntegrityError:
            return {"error": error_messages[422]}, 422


class CalendarControllerById(Resource):

    def get(self, calendar_string_id):

        if not session.get("user_token"):
            return {"error": error_messages[401]}, 401
        email, user_id = decode_token(session["user_token"])
        if not user_id:
            return {"error": error_messages[401]}, 401
        calendar_id = UUID(calendar_string_id)
        if not calendar_id:
            return {"error": error_messages[400]}, 400
        calendar = Calendar.query.filter(
            Calendar.id == calendar_id and Calendar.user_id == user_id
        ).first()
        if not calendar:
            return {"error": error_messages[404]}, 404
        return calendar.to_dict(), 200

    def patch(self, calendar_string_id):

        if not session.get("user_token"):
            return {"error": error_messages[401]}, 401
        email, user_id = decode_token(session["user_token"])
        if not user_id:
            return {"error": error_messages[401]}, 401
        calendar_id = UUID(calendar_string_id)
        if not calendar_id:
            return {"error": error_messages[400]}, 400
        data = request.get_json()
        if not data:
            return {"error": error_messages[400]}, 400
        name = data["name"]
        description = data["description"]
        if not name or not description:
            return {"error": error_messages[400]}, 400
        calendar = Calendar.query.filter(
            Calendar.id == calendar_id and Calendar.user_id == user_id
        ).first()
        if not calendar:
            return {"error": error_messages[404]}, 404
        try:
            setattr(calendar, "name", data["name"])
            setattr(calendar, "description", data["description"])
            db.session.add(calendar)
            db.session.commit()
            return calendar.to_dict(rules=("participant.profiles")), 202
        except IntegrityError:
            return {"error": error_messages[409]}, 409
        except SQLAlchemyError:
            db.session.rollback()
            return {"error": error_messages[500]}, 500

    def delete(self, calendar_string_id):

        if not session.get("user_token"):
            return {"error": error_messages[401]}, 401
        email, user_id = decode_token(session["user_token"])
        if not user_id:
            return {"error": error_messages[401]}, 401
        calendar_id = UUID(calendar_string_id)
        if not calendar_id:
            return {"error": error_messages[400]}, 400
        calendar = Calendar.query.filter(
            Calendar.id == calendar_id and Calendar.user_id == user_id
        ).first()
        if not calendar:
            return {"error": error_messages[404]}, 404
        try:
            db.session.delete(calendar)
            db.session.commit()
            return {"message": success_messages[204]}, 204
        except IntegrityError:
            return {"error": error_messages[409]}, 409
        except SQLAlchemyError:
            db.session.rollback()
            return {"error": error_messages[500]}, 500


class GuestCalendarControllerById(CalendarControllerById):

    def patch(self, calendar_string_id):
        if not session.get("user_token"):
            return {"error": error_messages[401]}, 401
        calendar_id = UUID(calendar_string_id)
        if not calendar_id:
            return {"error": error_messages[400]}, 400
        calendar = Calendar.query.filter(Calendar.id == calendar_id).first()
        if not calendar:
            return {"error": error_messages[404]}, 404
        collaboration = Collaboration.filter(
            Collaboration.calendar_id == calendar_id
        ).first()
        if not collaboration:
            return {"error": error_messages[404]}, 404
        if collaboration.permissions != "write":
            return {"error": error_messages[401]}, 401
        return super.patch()

    def delete(self, calendar_string_id):
        if not session.get("user_token"):
            return {"error": error_messages[401]}, 401
        calendar_id = UUID(calendar_string_id)
        if not calendar_id:
            return {"error": error_messages[400]}, 400
        calendar = Calendar.query.filter(Calendar.id == calendar_id).first()
        if not calendar:
            return {"error": error_messages[404]}, 404
        collaboration = Collaboration.filter(
            Collaboration.calendar_id == calendar_id
        ).first()
        if not collaboration:
            return {"error": error_messages[404]}, 404
        if collaboration.permissions != "write":
            return {"error": error_messages[401]}, 401
        return super.delete()


class EventController(Resource):

    def post(self):
        if not session.get("user_token"):
            return {"error": error_messages[401]}, 401
        data = request.get_json()
        if not data:
            return {"error": error_messages[400]}, 400
        calendar_id = (data["calendar_id"],)
        name = (data["name"],)
        description = (data["description"],)
        start = (data["start"],)
        end = (data["end"],)
        if not calendar_id or not name or not description or not start or not end:
            return {"error": error_messages[400]}, 400
        try:
            new_event = Event(
                calendar_id=calendar_id,
                name=name,
                description=description,
                start=start,
                end=end,
            )
            db.session.add(new_event)
            db.session.commit()
        except IntegrityError:
            return {"error": error_messages[422]}, 422
        except SQLAlchemyError:
            db.session.rollback()
            return {"error": error_messages[500]}, 500


class GuestEventController(EventController):

    def post(self, event_string_id):
        if not session.get("user_token"):
            return {"error": error_messages[401]}, 401
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
        return super.post()


class EventControllerById(Resource):

    def patch(self, event_string_id):
        if not session.get("user_token"):
            return {"error": error_messages[401]}, 401
        event_id = UUID(event_string_id)
        if not event_id:
            return {"error": error_messages[400]}, 400
        data = request.get_json()
        if not data:
            return {"error": error_messages[400]}, 400
        name = data["name"]
        description = data["description"]
        start = data["start"]
        end = data["end"]
        if not name or not description or not start or not end:
            return {"error": error_messages[400]}, 400

        event = Event.query.filter(Event.id == event_id).first()
        if not event:
            return {"error": error_messages[404]}, 404
        try:
            data = request.get_json()
            setattr(event, "name", name)
            setattr(event, "description", description)
            setattr(event, "start", start)
            setattr(event, "end", end)
            db.session.add(event)
            db.session.commit()
            return event.to_dict(), 202
        except IntegrityError:
            return {"error": error_messages[422]}, 422
        except SQLAlchemyError:
            db.session.rollback()
            return {"error": error_messages[500]}, 500

    def delete(self, event_string_id):
        if not session.get("user_token"):
            return {"error": error_messages[401]}, 401
        event_id = UUID(event_string_id)
        if not event_id:
            return {"error": error_messages[400]}, 400
        data = request.get_json()
        if not data:
            return {"error": error_messages[400]}, 400
        event = Event.query.filter(Event.id == event_id).first()
        if not event:
            return {"error": error_messages[404]}, 404
        try:
            db.session.delete(event)
            db.session.commit()
            return {"message": success_messages[204]}, 204
        except IntegrityError:
            return {"error": error_messages[409]}, 409
        except SQLAlchemyError:
            db.session.rollback()
            return {"error": error_messages[500]}, 500


class GuestEventControllerById(EventControllerById):

    def patch(self, event_string_id):
        if not session.get("user_token"):
            return {"error": error_messages[401]}, 401
        event_id = UUID(event_string_id)
        if not event_id:
            return {"error": error_messages[400]}, 400
        event = Event.query.filter(Event.id == event_id)
        if not event:
            return {"error": error_messages[404]}, 404
        collaboration = Collaboration.filter(
            Collaboration.calendar_id == event.calendar_id
        ).first()
        if not collaboration:
            return {"error": error_messages[404]}, 404
        if collaboration.permissions != "write":
            return {"error": error_messages[401]}, 401
        return super.patch()

    def delete(self, event_string_id):
        if not session.get("user_token"):
            return {"error": error_messages[401]}, 401
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
        return super.delete()


class TaskController(Resource):

    def post(self):
        if not session.get("user_token"):
            return {"error": error_messages[401]}, 401
        data = request.get_json()
        if not data:
            return {"error": error_messages[400]}, 400
        calendar_id = UUID(data["calendar_id"])
        title = data["title"]
        description = data["description"]
        date = data["date"]
        status = data["status"]
        if not calendar_id or not title or not description or not date or not status:
            return {"error": error_messages[400]}, 400
        try:
            new_task = Task(
                calendar_id=calendar_id,
                title=title,
                description=description,
                date=date,
                status=status,
            )
            db.session.add(new_task)
            db.session.commit()
            return new_task.to_dict(), 201
        except IntegrityError:
            return {"error": error_messages[422]}, 422
        except SQLAlchemyError:
            db.session.rollback()
            return {"error": error_messages[500]}, 500


class GuestTaskController(TaskController):

    def post(self, task_string_id):
        if not session.get("user_token"):
            return {"error": error_messages[401]}, 401
        task_id = UUID(task_string_id)
        if not task_id:
            return {"error": error_messages[400]}, 400
        task = Task.query.filter(Task.id == task_id).first()
        if not task:
            return {"error": error_messages[404]}, 404
        collaboration = Collaboration.filter(
            Collaboration.calendar_id == task.calendar_id
        )
        if not collaboration:
            return {"error": error_messages[404]}, 404
        if collaboration.permissions != "write":
            return {"error": error_messages[401]}, 401
        return super.post()


class TaskControllerById(Resource):

    def patch(self, task_string_id):
        if not session.get("user_token"):
            return {"error": error_messages[401]}, 401
        task_id = UUID(task_string_id)
        if not task_id:
            return {"error": error_messages[400]}, 400
        data = request.get_json()
        if not data:
            return {"error": error_messages[400]}, 400
        title = data["title"]
        description = data["description"]
        date = data["date"]
        status = data["status"]
        if not title or not description or not date or not status:
            return {"error": error_messages[400]}, 400
        task = Task.query.filter(Task.id == task_id).first()
        if not task:
            return {"error": error_messages[404]}, 404
        try:
            setattr(task, "title", title)
            setattr(task, "description", description)
            setattr(task, "date", date)
            setattr(task, "status", status)
            db.session.add(task)
            db.session.commit()
            return task.to_dict(), 204
        except IntegrityError:
            return {"error": error_messages[422]}, 422
        except SQLAlchemyError:
            db.session.rollback()
            return {"error": error_messages[500]}, 500

    def delete(self, task_string_id):
        if not session.get("user_token"):
            return {"error": error_messages[401]}, 401
        task_id = UUID(task_string_id)
        if not task_id:
            return {"error": error_messages[400]}, 400
        task = Task.query.filter(Task.id == task_id).first()
        if not task:
            return {"error": error_messages[404]}, 404
        try:
            db.session.delete(task)
            db.session.commit()
            return {"message": success_messages[204]}, 204
        except IntegrityError:
            return {"error": error_messages[409]}, 409
        except SQLAlchemyError:
            db.session.rollback()
            return {"error": error_messages[500]}, 500


class GuestTaskControllerById(TaskControllerById):

    def patch(self, task_string_id):
        if not session.get("user_token"):
            return {"error": error_messages[401]}, 401
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
        return super.patch()

    def delete(self, task_string_id):
        if not session.get("user_token"):
            return {"error": error_messages[401]}, 401
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

    def get(self):
        if not session.get("user_token"):
            return {"error": error_messages[401]}, 401
        email, user_id = decode_token(session["user_token"])
        if not user_id or not email:
            return {"error": error_messages[401]}, 401
        user = User.query.filter(User.id == user_id).first()
        if not user:
            return {"error": error_messages[404]}, 404
        invites = Invite.query.filter(Invite.receiver_email == user.email).all()
        if not invites:
            return {"error": error_messages[404]}, 404
        return [i.to_dict() for i in invites], 200

    def post(self):
        if not session.get("user_token"):
            return {"error": error_messages[401]}, 401
        email, user_id = decode_token(session["user_token"])
        if not email or not user_id:
            return {"error": error_messages[401]}, 401
        user = User.query.filter(User.id == user_id).first()
        data = request.get_json()
        if not data:
            return {"error": error_messages[400]}, 400
        calendar = Calendar.query.filter(Calendar.id == UUID(data["calendar_id"]))
        invite = Invite.query.filter(
            Invite.sender_email == email
            and Invite.receiver_email == data["reciever_email"]
            and Invite.calendar_id == data["calendar_id"]
        ).first()
        if invite and invite.active:
            return {"error": error_messages[409]}, 409
        if not calendar:
            return {"error": error_messages[404]}, 404
        receiver_email = data["receiver_email"]
        recipient_name = data["recipient_name"]
        calendar_name = data["calendar_name"]
        calendar_id = UUID(data["calendar_id"])
        sent_at = data["sent_at"]
        set_permissions = data["set_permissions"]
        if (
            not receiver_email
            or not recipient_name
            or not calendar_name
            or not calendar_id
            or not sent_at
            or not set_permissions
        ):
            return {"error": error_messages[400]}, 400
        try:
            new_invite = Invite(
                status="pending",
                sent_at=sent_at,
                set_permissions=set_permissions,
                recipient_name=recipient_name,
                calendar_name=calendar_name,
                active=1,
                calendar_id=calendar_id,
                sender_email=user.email,
                receiver_email=receiver_email,
            )
            db.session.add(new_invite)
            db.session.commit()
            return new_invite.to_dict(), 201
        except IntegrityError:
            return {"error": error_messages[422]}, 422
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500


class InviteControllerById(Resource):

    def patch(self, invite_string_id):
        if not session.get("user_token"):
            return {"error": error_messages[401]}, 401
        data = request.get_json()
        if not data:
            return {"error": error_messages[400]}, 400
        invite_id = UUID(invite_string_id)
        if not invite_id:
            return {"error": error_messages[400]}, 400
        status = data["status"]
        if not invite_id or not status:
            return {"error": error_messages[400]}, 400
        invite = Invite.query.filter(Invite.id == invite_id).first()
        if not invite:
            return {"error": error_messages[404]}, 404
        if not invite.active:
            return {"error": error_messages[400]}, 400
        if status == "accepted":
            try:
                new_collaboration = Collaboration(
                    permissions=invite.set_permissions,
                    owner_email=invite.sender_email,
                    guest_email=invite.receiver_email,
                    calendar_id=invite.calendar_id,
                )
                setattr(invite, "status", status)
                setattr(invite, "active", 0)
                db.session.add(invite)
                db.session.add(new_collaboration)
                db.session.commit()
                return new_collaboration.to_dict(rules=("calendar",)), 201
            except IntegrityError:
                return {"error": error_messages[422]}, 422
            except SQLAlchemyError:
                db.session.rollback()
                return {"error": error_messages[500]}, 500
        elif status == "declined":
            try:
                setattr(invite, "active", 0)
                db.session.add(invite)
                db.session.commit()
                return {"Message": "Invite declined"}, 204
            except IntegrityError:
                return {"error": error_messages[422]}, 422
            except SQLAlchemyError:
                db.session.rollback()
                return {"error": error_messages[500]}, 500

    def delete(self, invite_string_id):
        if not session.get("user_token"):
            return {"error": error_messages[401]}, 401
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
        except IntegrityError:
            return {"error": error_messages[409]}, 409
        except SQLAlchemyError:
            db.session.rollback()
            return {"error": error_messages[500]}, 500


class CollaborationController(Resource):

    def get(self):
        if not session.get("user_token"):
            return {"error": error_messages[401]}, 401
        email, user_id = decode_token(session["user_token"])
        collaborations = Collaboration.query.filter(
            Collaboration.owner_email == email
        ).all()
        if not collaborations:
            return {"error": error_messages[404]}, 404
        return [c.to_dict() for c in collaborations], 200


class CollaborationControllerById(Resource):

    def patch(self, collaboration_string_id):
        if not session.get("user_token"):
            return {"error": error_messages[401]}, 401
        email, user_id = decode_token(session["user_token"])
        if not email or not user_id:
            return {"error": error_messages[401]}, 401
        collaboration_id = UUID(collaboration_string_id)
        if not collaboration_id:
            return {"error": error_messages[400]}, 400
        collaboration = Collaboration.query.filter(
            Collaboration.id == collaboration_id
        ).first()
        if not collaboration:
            return {"error": error_messages[404]}, 404
        if not collaboration.owner_email == email:
            return {"error": error_messages[401]}, 401
        data = request.get_json()
        if not data:
            return {"error": error_messages[400]}, 400
        permissions = data["permissions"]
        if not permissions:
            return {"error": error_messages[400]}, 400
        try:
            setattr(collaboration, "permissions", permissions)
            db.session.add(collaboration)
            db.session.commit()
            return collaboration.to_dict(), 204
        except IntegrityError:
            return {"error": error_messages[409]}, 409
        except SQLAlchemyError:
            db.session.rollback()
            return {"error": error_messages[500]}, 500

    def delete(self, collaboration_string_id):
        if not session.get("user_token"):
            return {"error": error_messages[401]}, 401
        collaboration_id = UUID(collaboration_string_id)
        if not collaboration_id:
            return {"error": error_messages[400]}, 400
        collaboration = Collaboration.query.filter(
            Collaboration.id == collaboration_id
        ).first()
        if not collaboration:
            return {"error": error_messages[404]}, 404
        try:
            db.session.delete(collaboration)
            db.session.commit()
            return {"message": success_messages[204]}, 204
        except IntegrityError:
            return {"error": error_messages[422]}, 422
        except SQLAlchemyError:
            db.session.rollback()
            return {"error": error_messages[500]}, 500
