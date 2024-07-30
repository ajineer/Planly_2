import jwt
from dotenv import load_dotenv
import os
from uuid import UUID
from flask import request
from datetime import datetime
from models import Collaboration, Calendar


def generate_token(email, id, timeUnits):

    load_dotenv()
    secret_key = os.getenv("SECRET_KEY")
    payload = {
        "email": email,
        "user_id": id,
        "exp": datetime.utcnow() + timeUnits,
    }
    token = jwt.encode(payload, secret_key)
    return token


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
        token = None
        if "Authorization" in request.headers:
            token = request.headers.get("Authorization").split(" ")[1]
        if not token:
            return {"error": error_messages[401]}, 401

        email, user_id = decode_token(token)
        if not email or not user_id:
            return {"error": f"{user_id}, {email}"}, 401
        return func(*args, email, user_id, **kwargs)

    return wrapper


def verify_data(func):
    def wrapper(*args, **kwargs):
        data = request.get_json()
        if not data:
            return {"error": error_messages[400]}, 400
        data_items = {}
        keys = data.keys()
        for key in keys:
            if not data.get(key):
                return {"error": error_messages[400]}, 400
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


error_messages = {
    400: "Invalid request parameters",
    401: "Unauthorized",
    404: "Not found",
    409: "Conflict",
    422: "Unprocessable entity",
    500: "Internal server error",
}

success_messages = {200: "OK", 202: "updated", 201: "Created", 204: "No Content"}
