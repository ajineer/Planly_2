import jwt
from dotenv import load_dotenv
import os
from uuid import UUID
from flask import session, request
import json


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


# def token_required(func):
#     def wrapper(*args, **kwargs):
#         if not session.get("user_token"):
#             return {"error": error_messages[401]}, 401
#         email, user_id = decode_token(session["user_token"])
#         if not email or not user_id:
#             return {"error": error_messages[401]}, 401
#         return func(*args, email, user_id, **kwargs)

#    return wrapper


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


error_messages = {
    400: "Invalid request parameters",
    401: "Unauthorized",
    404: "Not found",
    409: "Conflict",
    422: "Unprocessable entity",
    500: "Internal server error",
}

success_messages = {200: "OK", 202: "updated", 201: "Created", 204: "No Content"}
