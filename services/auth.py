from fastapi import HTTPException, status, Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jwt.exceptions import InvalidTokenError
from schema.user import UserOut, UserLogin
from models.user import Users
from core.security import decode_access_token
from .utils import verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def get_user(email: UserLogin, db: Session) -> UserOut:
    user = db.query(Users).filter(Users.email == email).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='User not found')
    return user

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session):
    credential_exception = HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        detail='User not authenticated',
        headers={"WWW-Authenticate": 'Bearer'}
    )
    try:
        payload = decode_access_token(token)
        email = payload.get('sub')
        if not email:
            raise credential_exception
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise credential_exception
    user = get_user(user, db)
    if user is None:
        raise credential_exception
    return user

def authenticate_user(user: UserLogin, db: Session):
    user_exists = get_user(user, db)
    return user_exists