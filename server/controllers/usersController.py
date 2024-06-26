from flask import request, session
from flask_restful import Resource
from config import db


class Signup(Resource):

    def post(self):

        from models import User

        email = request.get_json()["email"]
        first_name = request.get_json()["first_name"]
        last_name = request.get_json()["last_name"]
        password = request.get_json()["password"]

        user = User.query.filter(User.email == email).first()

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

        return {"error": "422 Unprocessable Entity"}, 422


class Login(Resource):

    def post(self):
        from models import User

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

        from models import User

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
