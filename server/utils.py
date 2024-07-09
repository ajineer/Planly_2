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
