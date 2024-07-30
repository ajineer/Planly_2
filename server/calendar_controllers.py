from flask_restful import Resource
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from config import db
from models import Calendar
from uuid import UUID
from utils import (
    verify_data,
    token_required,
    error_messages,
    success_messages,
)


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

        calendar_id = UUID(data_items["id"])
        if not calendar_id:
            return {"error": f"calendar id {error_messages[400]}"}, 400
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
            return {"message": success_messages[200]}, 200
        except (IntegrityError, SQLAlchemyError) as e:
            return {"error": f"{e}"}, 500
