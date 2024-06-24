from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

# Local imports
from .. import db

# Add your model imports
from ..models import Participant


class Particpants(Resource):
    def post(self):
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
        if session.get("user_id"):
            participant = Participant.query.filter(
                Participant.id == particpant_id
            ).first()
            db.session.delete(participant)
            db.session.commit()
            return {"Message": "Participant successfully removed."}, 204
        return {"error", "Unauthorized"}, 401
