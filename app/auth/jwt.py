import jwt
import datetime
from datetime import timezone, timedelta, datetime

import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"

# create access token, and return token
def create_access_token(data: dict ,expires_delta: timedelta | None = None):
    """
    method responsible to create a jwt(token) 

    args:
    data: a empty dictonary
    expires_detla: minutes required for the token expiration 

    return: 
    returns a encoded jwt(token)
    """
    to_encode = data.copy()

    if expires_delta:
        expires = datetime.now(timezone.utc) + expires_delta
    else: 
        expires = datetime.now(timezone.utc) + timedelta(minutes=20)

    to_encode.update({"exp":expires})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt

# decode access token, return username
def decode_access_token(token: str):
    """
    decoddes a jwt(token)

    args: 
    token: recevies a encoded token

    return:
    a decoded token
    """
    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    return payload