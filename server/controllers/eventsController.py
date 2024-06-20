from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

# Local imports
from config import app, db, api

# Add your model imports
from models import Event


class Events(Resource):
    def post(self):
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
            return {"erro": "Unauthorized"}, 401


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
