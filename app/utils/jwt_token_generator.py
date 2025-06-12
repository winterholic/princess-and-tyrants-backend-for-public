import jwt
import datetime
import secrets
import base64
from fastapi import APIRouter
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

router = APIRouter()

@router.get("/generate_secret_key")
def generate_secret_key():
    length = 32
    key = secrets.token_bytes(length)
    encoded_key = base64.urlsafe_b64encode(key).decode('utf-8')
    return encoded_key

secret_key = "키"

def generate_jwt_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.now() + datetime.timedelta(hours=24 * 30),
    }
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token