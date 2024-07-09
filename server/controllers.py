from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.hybrid import hybrid_property
from config import db
from models import User, Calendar, Event, Task, Invite, UserCalendar
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import jwt
from utils import decode_token
from uuid import UUID


class Signup(Resource):

    def post(self):
        data = request.get_json()
        email = data["email"]
        first_name = data["first_name"]
        last_name = data["last_name"]
        password = data["password"]

        # user = User.query.filter(User.email == email).first()
        try:
            if email and password:
                new_user = User(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    shared_id=None,
                )
                new_user.password_hash = password
                db.session.add(new_user)
                db.session.commit()
                return {"message": "User created, please login"}, 201
            return {"error": "cannot signup twice with same email"}, 409
        except IntegrityError:
            return {"error": "422 Unprocessable Entity"}, 422


class Login(Resource):

    def post(self):

        data = request.get_json()
        email = data["email"]
        password = data["password"]

        user = User.query.filter(User.email == email).first()

        if user and user.authenticate(password) and user.email and user.id:
            token = self.generate_token(user.email, str(user.id))
            session["user_token"] = token
            return {"token": token}, 200
        return {"error": "Invalid email or password"}, 401

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
        token = session.get("user_token")
        if token:
            email, user_id = decode_token(token)
            user = User.query.filter(User.id == user_id).first()
            if user:
                return (user.to_dict(), 200)
            return {"error": "user not found"}, 404
        return {"error": "Invalid token"}, 401


class Logout(Resource):

    def delete(self):

        if session.get("user_token"):
            session["user_token"] = None
            return {"Message": "User logged out"}, 204
        return {"error": "Unauthorized"}, 401


class CalendarController(Resource):

    def get(self):
        token = session.get("user_token")
        if token:
            email, user_id = decode_token(token)
            if user_id:
                calendars = Calendar.query.filter(Calendar.user_id == user_id).all()
                if calendars:
                    return [
                        c.to_dict(
                            rules=(
                                "tasks",
                                "events",
                                "participant.invites",
                            )
                        )
                        for c in calendars
                    ], 200
                return {"error": "No calendars found"}, 404
            return {"error", "Invalid token"}, 401
        return {"error": "Unauthorized"}, 401

    def post(self):

        token = session.get("user_token")
        if token:
            email, user_id = decode_token(token)
            if user_id:
                data = request.get_json()
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
                    return {"error": "could not create calendar"}, 422
            return {"error", "Invalid token"}, 401
        return {"error": "Unauthorized"}, 401


class CalendarControllerById(Resource):

    def get(self, calendar_id):
        if session.get("user_id"):
            email, user_id = decode_token(session["user_id"])
            calendar = Calendar.query.filter(
                Calendar.id == calendar_id and Calendar.user_id == user_id
            ).first()
            if calendar:
                return (
                    calendar.to_dict(),
                    200,
                )
            return {"error": "calendar not found"}, 404
        return {"error": "Unauthorized"}, 401

    def patch(self, calendar_id):

        if session.get("user_id"):
            email, user_id = decode_token(session["useer_token"])
            calendar = Calendar.query.filter(
                Calendar.id == calendar_id and Calendar.user_id == user_id
            ).first()
            if calendar:
                data = request.get_json()
                setattr(calendar, "name", data["name"])
                setattr(calendar, "description", data["description"])
                db.session.add(calendar)
                db.session.commit()
                return calendar.to_dict(rules=("participant.profiles")), 202
            return {"error": "Calendar not found"}, 404
        return {"error": "Unauthorized"}, 401

    def delete(self, calendar_id):

        if session.get("user_id"):
            email, user_id = decode_token(session["user_token"])
            calendar = Calendar.query.filter(
                Calendar.id == calendar_id and Calendar.user_id == user_id
            ).first()
            if calendar:
                db.session.delete(calendar)
                db.session.commit()
                return {"Message": "Calendar deleted"}, 204
            return {"error": "Calendar not found"}, 404
        return {"error": "Unauthorized"}, 401


class EventController(Resource):
    def post(self):

        if session.get("user_token"):
            try:
                data = request.get_json()
                new_event = Event(
                    calendar_id=data["calendar_id"],
                    name=data["name"],
                    description=data["description"],
                    start=data["start"],
                    end=data["end"],
                )
                db.session.add(new_event)
                db.session.commit()
            except IntegrityError:
                return {"error": "could not create event"}
        return {"error": "Unauthorized"}, 401


class EventControllerById(Resource):

    def patch(self, event_id):
        if session.get("user_token"):
            event = Event.query.filter(Event.id == event_id).first()
            if event:
                data = request.get_json()
                setattr(event, "name", data["name"])
                setattr(event, "description", data["description"])
                setattr(event, "start", data["start"])
                setattr(event, "end", data["end"])
                db.session.add(event)
                db.session.commit()
                return event.to_dict(), 202
            return {"error": "Event not found"}, 404
        return {"error": "Unauthorized"}, 401

    def delete(self, event_id):
        if session.get("user_token"):
            event = Event.query.filter(Event.id == event_id).first()
            if event:
                db.session.delete(event)
                db.session.commit()
                return {"Message": "Event deleted"}, 204
            return {"error": "Event not found"}, 404
        return {"error": "Unauthorized"}, 401


class TaskController(Resource):

    def post(self):

        if session.get("user_token"):
            try:
                data = request.get_json()
                new_task = Task(
                    calendar_id=data["calendar_id"],
                    title=data["title"],
                    description=data["description"],
                    date=data["date"],
                    status=data["status"],
                )
                db.session.add(new_task)
                db.session.commit()
            except IntegrityError:
                return {"error": "could not create task"}, 422
        return {"error": "Unauthorized"}, 401


class TaskControllerById(Resource):

    def patch(self, task_id):

        if session.get("user_token"):
            task = Task.query.filter(Task.id == task_id).first()
            if task:
                data = request.get_json()
                setattr(task, "title", data["title"])
                setattr(task, "description", data["description"])
                setattr(task, "date", data["date"])
                setattr(task, "status", data["status"])

                db.session.add(task)
                db.session.commit()

                return task.to_dict(), 202
            return {"error": "Task not found"}, 404
        return {"error": "Unauthorized"}, 401

    def delete(self, task_id):

        if session.get("user_token"):
            task = Task.query.filter(Task.id == task_id).first()
            if task:
                db.session.delete(task)
                db.session.commit()
                return {"Message": "Task deleted"}, 204
            return {"error": "Task not found"}, 404
        return {"error": "Unauthorized"}, 401


class InviteController(Resource):

    def get(self):

        if session.get("user_token"):
            email, user_id = decode_token(session["user_token"])
            user = User.query.filter(User.id == user_id).first()
            invites = Invite.query.filter(Invite.receiver_email == user.email).all()
            if invites:
                return [i.to_dict() for i in invites], 200
            return {"error": "No invites found"}, 404
        return {"error": "Unauthorized"}, 401

    def post(self):

        if session.get("user_token"):
            email, user_id = decode_token(session["user_token"])
            user = User.query.filter(User.id == user_id).first()
            data = request.get_json()
            calendar = Calendar.query.filter(Calendar.id == data["calendar_id"])
            if calendar and data and user:
                try:
                    new_invite = Invite(
                        sender_email=user.email,
                        receiver_email=data["receiver_email"],
                        recipient_name=data["recipient_name"],
                        calendar_name=data["calendar_name"],
                        calendar_id=data["calendar_id"],
                        sent_at=data["sent_at"],
                        set_permissions=data["set_permissions"],
                        status="pending",
                    )
                    db.session.add(new_invite)
                    db.session.commit()
                    return new_invite.to_dict(), 201
                except IntegrityError:
                    return {"error": "could not create invite"}, 422
            return {"error": "Calendar does not exist or can't be shared"}, 404
        return {"error": "Unauthorized"}

    def patch(self):

        if session.get("user_token"):
            data = request.get_json()
            invite_id = UUID(data["invite_id"])
            status = data["status"]
            invite = Invite.query.filter(Invite.id == invite_id).first()
            if not invite or not status:
                return {"error": "Invite or status not found in request data"}, 400
            calendar = Calendar.query.filter(
                Calendar.id == UUID(invite.calendar_id)
            ).first()
            if not calendar:
                return {"error": "Calendar not found for the invite"}, 404
            email, user_id = decode_token(session["user_token"])
            user = User.query.filter(User.id == user_id).first()
            if not user:
                return {"error": "User not found"}, 404
            if status == "accepted":
                user_calendar = UserCalendar.query.filter(
                    UserCalendar.id == user.shared_id
                ).first()
                try:
                    if not user_calendar:
                        new_user_calendar = UserCalendar(
                            permissions=invite.set_permissions
                        )
                        db.session.add(new_user_calendar)
                        db.session.commit()

                        setattr(calendar, "shared_id", new_user_calendar.id)
                        setattr(user, "shared_id", new_user_calendar.id)
                        setattr(invite, "status", status)
                        db.session.add(user)
                        db.session.add(calendar)
                        db.session.add(invite)
                        db.session.commit()
                        return new_user_calendar.to_dict()
                    else:
                        return {
                            "error": "cannot share calendar more than once with same user"
                        }, 409
                except IntegrityError:
                    db.session.rollback()
                    return {"error": "Could not join recipient and calendar"}, 422
            elif status == "declined":
                db.session.delete(invite)
                db.session.commit()
                return {"Message": "Invite declined and deleted"}, 204
            return {"error": "Invalid status or operation"}, 400
        return {"error": "Unauthorized"}, 401


# class InviteControllerById(Resource):
