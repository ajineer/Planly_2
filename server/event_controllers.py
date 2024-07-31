from flask_restful import Resource
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from config import db
from models import Calendar, Event
from datetime import datetime
from uuid import UUID
from utils import (
    verify_data,
    token_required,
    error_messages,
    success_messages,
    verify_collaboration,
)


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

    @verify_collaboration
    def post(self, data_items, calendar):
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
            Calendar.id == UUID(data_items["calendar_id"]),
        ).first()
        if not calendar:
            return {"error": f"calendar {error_messages[404]}"}, 404
        event = Event.query.filter(Event.id == UUID(data_items["id"])).first()
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
            Calendar.id == event.calendar_id,
            Calendar.user_id == user_id,
        ).first()
        if not calendar:
            return {"error": f"calendar {error_messages[404]}"}, 404
        try:
            db.session.delete(event)
            db.session.commit()
            return {"message": success_messages[200]}, 200
        except (IntegrityError, SQLAlchemyError) as e:
            return {"error": f"error: {e}"}, 500


class GuestEventPatchDeleteController(Resource):

    @verify_collaboration
    def patch(self, data_items, calendar):

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

    @verify_collaboration
    def delete(self, data_items, calendar):

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
