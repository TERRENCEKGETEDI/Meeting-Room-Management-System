import jwt
from fastapi import HTTPException
import datetime
from datetime import timezone, timedelta, datetime

import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# create access token, and return token
def create_access_token(username: str):
    """
    method responsible to create a jwt(token) 

    args:
    a username

    return: 
    returns a encoded jwt(token)
    """
    
    expires = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": username,
        "exp": expires
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

# decode access token, return username
def decode_access_token(token: str):
    """
    decoddes a jwt(token)

    args: 
    token: recevies a encoded token

    return:
    the payload
    """
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        )
    
    return payload