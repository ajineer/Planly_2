import jwt
from dotenv import load_dotenv
import os
from uuid import UUID
from flask import request


def decode_token(token):
    load_dotenv()
    secret_key = os.getenv("SECRET_KEY")

    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        email = payload["email"]
        user_id = UUID(payload["user_id"])
        return email, user_id
    except jwt.ExpiredSignatureError:
        return None, None
    except jwt.InvalidTokenError as e:
        return None, {"error": f"{e}"}


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


error_messages = {
    400: "Invalid request parameters",
    401: "Unauthorized",
    404: "Not found",
    409: "Conflict",
    422: "Unprocessable entity",
    500: "Internal server error",
}

success_messages = {200: "OK", 202: "updated", 201: "Created", 204: "No Content"}
