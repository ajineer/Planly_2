from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

# Local imports
from config import app, db, api

# Add your model imports
from models import User


class Signup(Resource):

    def post(self):
        email = request.get_json().get("email")
        first_name = request.get_json().get("first_name")
        last_name = request.get_json().get("last_name")
        password = request.get_json().get("password")

        if email and password and not User.query.filter(User.email == email).first():
            new_user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
            )
            new_user.password_hash = password
            db.session.add(new_user)
            db.session.commit()
            session["user_id"] = new_user.id
            return new_user.to_dict(), 201

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
                    return user.to_dict(), 200
                return {"error": "session could not be established"}, 400

        return {"error": "Unauthorized"}, 401


class CheckSession(Resource):

    def get(self):
        user = User.query.filter(User.id == session.get("user_id")).first()
        if user:
            return user.to_dict(), 200
        return {"error": "Unauthorized"}, 401


class Logout(Resource):

    def delete(self):

        if session.get("user_id"):
            session["user_id"] = None
            return {"Message": "User logged out"}, 204
        return {"error": "Unauthorized"}, 401
