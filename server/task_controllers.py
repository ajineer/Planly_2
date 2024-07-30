from flask_restful import Resource
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from config import db
from models import Calendar, Task
from datetime import datetime
from uuid import UUID
from utils import (
    verify_data,
    token_required,
    error_messages,
    success_messages,
    verify_collaboration,
)


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
