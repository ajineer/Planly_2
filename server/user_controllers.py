import jwt

from flask import make_response, jsonify, request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from config import db
from models import User
from datetime import timedelta
from utils import (
    verify_data,
    error_messages,
    success_messages,
    generate_token,
    token_required,
    decode_token,
)


class Signup(Resource):

    @verify_data
    def post(self, data_items):
        user = User.query.filter(User.email == data_items["email"]).first()
        if user:
            return {"error": error_messages[409]}, 409
        try:
            new_user = User(
                first_name=data_items["first_name"],
                last_name=data_items["last_name"],
                email=data_items["email"],
            )
            new_user.password_hash = data_items["password"]
            db.session.add(new_user)
            db.session.commit()
            return {"message": success_messages[201]}, 201
        except (IntegrityError, SQLAlchemyError) as e:
            return {"error": f"{e}"}, 500


class Login(Resource):

    @verify_data
    def post(self, data_items):

        user = User.query.filter(User.email == data_items["email"]).first()
        if (
            not user
            or not user.authenticate(data_items["password"])
            or not user.email
            or not user.id
        ):
            return {"error": f"user {error_messages[404]}"}, 404

        days = timedelta(days=10)
        access_token = generate_token(user.email, str(user.id), timeUnits=days)
        response = make_response(jsonify({"message": success_messages[200]}))
        response.set_cookie(
            "access_token",
            access_token,
            httponly=True,
            secure=True,
            samesite="Strict",
        )
        return response


class Logout(Resource):

    @token_required
    def post(self, email, user_id):
        user = User.query.filter(User.email == email, User.id == user_id).first()
        if not user:
            return {"error": f"user {error_messages[401]}"}, 401
        response = make_response({"message": "user logged out"})
        response.set_cookie("access_token", expires=0, httponly=True, secure=True)
        return response


class CheckAuth(Resource):

    @token_required
    def get(self, email, user_id):
        user = User.query.filter(User.email == email, User.id == user_id).first()
        if not user:
            return {"error": f"user {error_messages[401]}"}, 401
        return {"message": f"user authenticated {success_messages[200]}"}, 200
