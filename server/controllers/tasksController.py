from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError


def use_db():
    from app import db
    return db


class Tasks(Resource):
    def post(self):
        from db_models import Task
        db = use_db()
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
                return {"error": "could not create task"}
        return {"error": "Unauthorized"}, 401


class TasksById(Resource):
    def patch(self, task_id):
        from db_models import Task
        db = use_db()
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
        from db_models import Task
        db = use_db()
        if session.get("user_id"):
            task = Task.query.filter(Task.id == task_id).first()
            if task:
                db.session.delete(task)
                db.session.commit()
                return {"Message": "Task deleted"}, 204
            return {"error": "Task not found"}, 404
        return {"error": "Unauthorized"}, 401
