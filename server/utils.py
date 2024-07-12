import jwt
from dotenv import load_dotenv
import os
from uuid import UUID


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
    except jwt.InvalidTokenError:
        return None, None


error_messages = {
    400: "Invalid request parameters",
    401: "Unauthorized",
    404: "Not found",
    409: "Conflict",
    422: "Unprocessable entity",
    500: "Internal server error",
}

success_messages = {200: "OK", 201: "Created", 204: "No Content"}
