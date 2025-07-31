from fastapi import APIRouter, Depends, status, HTTPException, Form
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from schema.user import UserCreate, UserLogin, UserOut
from schema.token import Token
from core.security import create_access_token, decode_access_token
from typing import Annotated
from services.user import create_user, update_user, delete_user
from services.utils import verify_password
from services.auth import authenticate_user, get_user, get_current_user
from sqlalchemy.orm import Session
from db.session import SessionLocal
from datetime import timedelta, timezone

user_router = APIRouter(prefix='/user', tags=['user'])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@user_router.post('/register', status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)) -> UserOut:
    return create_user(user, db)

@user_router.put('/update_profile/{user_id}', status_code=status.HTTP_201_CREATED)
def update_profile(user_id: int, user: UserCreate, db: Session = Depends(get_db)) -> UserOut:
    return update_user(user_id, user, db)

@user_router.delete('/delete_profile/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def remove_user(user_id: int, db: Session = Depends(get_db)):
    return delete_user(user_id, db)

@user_router.post('/token', status_code=status.HTTP_202_ACCEPTED, response_model=Token)
def login_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)) -> Token:
    user = authenticate_user(form_data.username, db)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail='Invalid password or email',
            headers={'WWW-Authenticate': "Bearer"}
        )
    access_token = create_access_token(data={"sub": user.email})
    return Token(access_token=access_token, token_type="bearer")

@user_router.get('/data', status_code=status.HTTP_202_ACCEPTED)
def data_login(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)) -> UserCreate:
    return get_current_user(token, db)