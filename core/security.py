from fastapi import Depends
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
import os


secret_key = os.getenv('SECRET_KEY')
algorithm_local = os.getenv('ALGORITHM')
EXPIRATION_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRATION_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm_local)
    return encoded_jwt 

def decode_access_token(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, secret_key, algorithms=algorithm_local)
        return payload
    except JWTError:
        return {}