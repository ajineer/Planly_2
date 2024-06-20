from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

# Local imports
from config import app, db, api

# Add your model imports
from models import Calendar


class Calendars(Resource):

    def get(self):
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
                            "invites",
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
        if session.get("user_id"):
            calendar = Calendar.query.filter(Calendar.id == calendar_id).first()
            if calendar:
                db.session.delete(calendar)
                db.session.commit()
                return {"Message": "Calendar deleted"}, 204
            return {"error": "Calendar not found"}, 404
        return {"error": "Unauthorized"}, 401
