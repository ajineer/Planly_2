from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from config import db
from models import User, Calendar, Event, Task, Invite


class Signup(Resource):

    def post(self):

        email = request.get_json()["email"]
        first_name = request.get_json()["first_name"]
        last_name = request.get_json()["last_name"]
        password = request.get_json()["password"]

        user = User.query.filter(User.email == email).first()
        try:
            if email and password and not user:
                new_user = User(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                )
                new_user.password_hash = password
                db.session.add(new_user)
                db.session.commit()
                session["user_id"] = new_user.id
                return (
                    new_user.to_dict(
                        rules=[
                            "-calendars",
                            "-calendar_group",
                            "-sent_invites",
                            "-received_invites",
                        ]
                    ),
                    201,
                )
            return {"error": "cannot signup twice with same email"}, 409
        except IntegrityError:
            return {"error": "422 Unprocessable Entity"}, 422


class Login(Resource):

    def post(self):

        data = request.get_json()
        email = data["email"]
        password = data["password"]

        user = User.query.filter(User.email == email).first()

        if user:
            if user.authenticate(password):
                session["user_id"] = user.id
                if session["user_id"]:
                    return (
                        user.to_dict(
                            rules=[
                                "calendar_group",
                                "sent_invites",
                                "received_invites",
                            ]
                        ),
                        200,
                    )
                return {"error": "session could not be established"}, 400

        return {"error": "Unauthorized"}, 401


class CheckSession(Resource):

    def get(self):

        user = User.query.filter(User.id == session.get("user_id")).first()
        if user:
            return (
                user.to_dict(
                    rules=[
                        "calendar_group",
                        "sent_invites",
                        "received_invites",
                    ]
                ),
                200,
            )
        return {"error": "Unauthorized"}, 401


class Logout(Resource):

    def delete(self):

        if session.get("user_id"):
            session["user_id"] = None
            return {"Message": "User logged out"}, 204
        return {"error": "Unauthorized"}, 401


class Calendars(Resource):

    def get(self):
        from models import Calendar

        if session.get("user_id"):
            calendars = Calendar.query.filter(
                Calendar.user_id == session["user_id"]
            ).all()
            if calendars:
                return [
                    c.to_dict(
                        rules=(
                            "tasks",
                            "events",
                            "user_group",
                        )
                    )
                    for c in calendars
                ], 200
            return {"error": "No calendars found"}, 404
        return {"error": "Unauthorized"}, 401

    def post(self):

        if session.get("user_id"):
            try:
                new_calendar = Calendar(
                    user_id=session["user_id"],
                    name=request.get_json()["name"],
                    description=request.get_json()["description"],
                )
                db.session.add(new_calendar)
                db.session.commit()
                return new_calendar.to_dict(), 201
            except IntegrityError:
                return {"error": "could not create calendar"}, 422
        return {"error": "Unauthorized"}, 401


class CalendarsById(Resource):

    def patch(self, calendar_id):
        from models import Calendar

        if session.get("user_id"):
            calendar = Calendar.query.filter(Calendar.id == calendar_id).first()
            if calendar:
                setattr(calendar, "name", request.get_json()["name"])
                setattr(calendar, "description", request.get_json()["description"])
                db.session.add(calendar)
                db.session.commit()
                return calendar.to_dict(), 202
            return {"error": "Calendar not found"}, 404
        return {"error": "Unauthorized"}, 401

    def delete(self, calendar_id):
        from models import Calendar

        if session.get("user_id"):
            calendar = Calendar.query.filter(Calendar.id == calendar_id).first()
            if calendar:
                db.session.delete(calendar)
                db.session.commit()
                return {"Message": "Calendar deleted"}, 204
            return {"error": "Calendar not found"}, 404
        return {"error": "Unauthorized"}, 401


class Events(Resource):
    def post(self):
        from models import Event

        if session.get("user_id"):
            try:
                new_event = Event(
                    user_id=session["user_id"],
                    name=request.get_json()["name"],
                    description=request.get_json()["description"],
                    start=request.get_json()["start"],
                    end=request.get_json()["end"],
                )
                db.session.add(new_event)
                db.session.commit()
            except IntegrityError:
                return {"error": "could not create event"}
        return {"error": "Unauthorized"}, 401


class EventsById(Resource):

    def patch(self, event_id):
        if session.get("user_id"):
            event = Event.query.filter(Event.id == event_id).first()
            if event:
                setattr(event, "name", request.get_json()["name"])
                setattr(event, "description", request.get_json()["description"])
                setattr(event, "start", request.get_json()["start"])
                setattr(event, "end", request.get_json()["end"])
                db.session.add(event)
                db.session.commit()
                return event.to_dict(), 202
            return {"error": "Event not found"}, 404
        return {"error": "Unauthorized"}, 401

    def delete(self, event_id):
        if session.get("user_id"):
            event = Event.query.filter(Event.id == event_id).first()
            if event:
                db.session.delete(event)
                db.session.commit()
                return {"Message": "Event deleted"}, 204
            return {"error": "Event not found"}, 404
        return {"error": "Unauthorized"}, 401


class Tasks(Resource):

    def post(self):

        if session.get("user_id"):
            try:
                new_task = Task(
                    user_id=session["user_id"],
                    title=request.get_json()["title"],
                    description=request.get_json()["description"],
                    date=request.get_json()["date"],
                    status=request.get_json()["status"],
                )
                db.session.add(new_task)
                db.session.commit()
            except IntegrityError:
                return {"error": "could not create task"}, 422
        return {"error": "Unauthorized"}, 401


class TasksById(Resource):

    def patch(self, task_id):

        if session.get("user_id"):

            task = Task.query.filter(Task.id == task_id).first()

            if task:

                setattr(task, "title", request.get_json()["title"])
                setattr(task, "description", request.get_json()["description"])
                setattr(task, "date", request.get_json()["date"])
                setattr(task, "status", request.get_json()["status"])

                db.session.add(task)
                db.session.commit()

                return task.to_dict(), 202
            return {"error": "Task not found"}, 404
        return {"error": "Unauthorized"}, 401

    def delete(self, task_id):

        if session.get("user_id"):
            task = Task.query.filter(Task.id == task_id).first()
            if task:
                db.session.delete(task)
                db.session.commit()
                return {"Message": "Task deleted"}, 204
            return {"error": "Task not found"}, 404
        return {"error": "Unauthorized"}, 401


class Invite(Resource):

    def get(self):

        if session.get("user_id"):
            invites = Invite.query.filter(
                Invite.receiver_email == session["email"]
            ).all()
            if invites:
                return [i.to_dict() for i in invites], 200
            return {"error": "No invites found"}, 404
        return {"error": "Unauthorized"}, 401

    def post(self):

        if session.get("user_id"):
            try:
                invite = Invite(
                    sender_id=session["user_id"],
                    sender_email=session["email"],
                    receiver_email=request.get_json()["email"],
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


class InvitesById(Resource):

    def patch(self, invite_id):

        if session.get("user_id"):
            invite = Invite.query.filter(Invite.id == invite_id).first()
            if invite:
                status = request.get_json()["status"]
                if status == "accepted":
                    setattr(invite, "status", status)
                    user = User.query.filter(User.id == invite.receiver_id).first()
                    calendar = Calendar.query.filter(
                        Calendar.id == invite.calendar_id
                    ).first()
                    user.calendar_group.append(calendar)
                    calendar.user_group.append(user)
                    db.session.add(user)
                    db.session.add(calendar)
                    db.session.delete(invite)
                    db.session.commit()
                    return {"Message": "Invite accepted"}, 202
                elif status == "declined":
                    db.session.delete(invite)
                    db.session.commit()
                    return {"Message": "Invite declined and deleted"}, 204
            return {"error": "Invite not found"}, 404
        return {"error": "Unauthorized"}, 401
