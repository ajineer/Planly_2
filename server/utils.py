import jwt
from dotenv import load_dotenv
import os
from uuid import UUID
from flask import request, make_response, jsonify
from datetime import datetime, timedelta
from models import Collaboration, Calendar


def generate_token(email, id, timeUnits):

    load_dotenv()
    secret_key = os.getenv("SECRET_KEY")
    access_token_payload = {
        "email": email,
        "user_id": id,
        "exp": datetime.utcnow() + timeUnits,
    }
    refresh_token_payload = {
        "email": email,
        "user_id": id,
        "exp": datetime.utcnow() + timedelta(days=30),
    }
    access_token = jwt.encode(access_token_payload, secret_key)
    refresh_token = jwt.encode(refresh_token_payload, secret_key)

    return access_token, refresh_token


def decode_token(token):
    load_dotenv()
    secret_key = os.getenv("SECRET_KEY")

    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        email = payload["email"]
        user_id = UUID(payload["user_id"])
        return email, user_id
    except ValueError as e:
        return {"error": f"{e}"}, 400
    except jwt.ExpiredSignatureError as e:
        return {"error": f"Expired: {e}"}, 401
    except jwt.InvalidTokenError as e:
        return {"error": f"Invalid Token: {e}"}, 401


def token_required(func):
    def wrapper(*args, **kwargs):
        token = request.cookies.get("access_token")
        if not token:
            return {"error": error_messages[401]}, 401

        email, user_id = decode_token(token)
        if not email or not user_id:
            return {"error": "invalid token"}, 401
        return func(*args, email, user_id, **kwargs)

    return wrapper


def verify_data(func):
    def wrapper(*args, **kwargs):
        data = request.get_json()
        if not data:
            return {"error": f"data: {error_messages[400]}"}, 400
        data_items = {}
        keys = data.keys()
        for key in keys:
            if data.get(key) == None:
                return {"error": f"{key, data[key], error_messages[400]}"}, 400
            else:
                data_items[key] = data[key]
        return func(*args, data_items=data_items, **kwargs)

    return wrapper


def verify_collaboration(func):

    @token_required
    @verify_data
    def wrapper(*args, email, user_id, data_items, **kwargs):
        collaboration = Collaboration.query.filter(
            Collaboration.id == UUID(data_items["collaboration_string_id"]),
            Collaboration.guest.id == user_id,
            Collaboration.guest_email == email,
        ).first()
        if not collaboration:
            return {"error" f"collaboration {error_messages[404]}"}, 404
        if collaboration.permissions != "write":
            return {"error": error_messages[401]}, 401
        calendar = Calendar.query.filter(
            Calendar.id == UUID(collaboration.calendar_id)
        ).first()
        if not calendar:
            return {"error": f"calendar {error_messages[404]}"}, 404
        return func(*args, calendar=calendar, data_items=data_items, **kwargs)

    return wrapper


def refresh_token(func):

    def wrapper(*args, **kwargs):
        try:
            token = request.cookies.get("access_token")
            if not token:
                return {"error": error_messages[401]}, 401
            email, user_id = decode_token(token)
            if not email or not user_id:
                return {"error": error_messages[401]}, 401
            access_token, refresh_token = generate_token(
                email, str(user_id), timedelta(days=30)
            )
            response = make_response(jsonify({"refresh_token": refresh_token}))
            response.set_cookie(
                "access_token",
                access_token,
                httponly=True,
                secure=True,
                samesite="Strict",
            )
            return func(*args, response=response, **kwargs)
        except jwt.ExpiredSignatureError:
            return {"error": "Refresh token expired"}, 401
        except jwt.InvalidTokenError:
            return {"error": "Invalid refresh token"}, 401

    return wrapper


error_messages = {
    400: "Invalid request parameters",
    401: "Unauthorized",
    404: "Not found",
    409: "Conflict",
    422: "Unprocessable entity",
    500: "Internal server error",
}

success_messages = {200: "OK", 202: "updated", 201: "Created", 204: "No Content"}
