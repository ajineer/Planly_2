from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError


def use_db():
    from app import db
    return db


class Particpants(Resource):
    def post(self):
        from db_models import Participant
        db = use_db()
        if session.get("user_id"):
            try:
                new_particpant = Participant(
                    role=request.get_json()["role"],
                )
                db.session.add(new_particpant)
                db.session.commit()
            except IntegrityError:
                return {"error": "could not add participant"}, 422
        return {"error": "Unauthorized"}


class ParticpantsById(Resource):
    def delete(self, particpant_id):
        from db_models import Participant
        db = use_db()
        if session.get("user_id"):
            participant = Participant.query.filter(
                Participant.id == particpant_id
            ).first()
            db.session.delete(participant)
            db.session.commit()
            return {"Message": "Participant successfully removed."}, 204
        return {"error", "Unauthorized"}, 401
