from sqlalchemy.orm import Session
from sqlalchemy import select
from models.user import Users
from schema.user import UserCreate, UserOut
from fastapi import HTTPException, status
from .utils import hash_password

def create_user(user: UserCreate, db: Session) -> UserOut:
    user_exists = db.query(Users).filter(Users.email == user.email).first()

    if user_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Usuário já existe')

        try:
            username_exists = db.query(Users).filter(Users.name == user.name)
            if username_exist:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Nome já cadastrado')
        except Exception as e:
            print(e)   
    hashed_password = hash_password(user.password)
    user_create = Users(
        name=user.name,
        hashed_password=hashed_password,
        email=user.email,
    )
    db.add(user_create)
    db.commit()
    db.refresh(user_create)
    return user_create

def update_user(user_id: int, user_data: UserCreate, db: Session) -> UserOut:
    user_to_update = db.query(Users).filter(Users.id == user_id).first()
    hashed_password = hash_password(user_data.password) 
    if user_to_update:
        if user_data.name is not None:
            user_to_update.name = user_data.name
        if user_data.email is not None:
            user_to_update.email = user_data.email
        if user_data.password is not None:
            user_to_update.hashed_password = hashed_password

        db.add(user_to_update)
        db.commit()
        db.refresh(user_to_update)
        return user_to_update

def delete_user(user_id: int, db: Session) -> UserOut:
    user_delete = db.query(Users).filter(Users.id == user_id).first()

    if user_delete:
        db.delete(user_delete) 
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Usuário não encontrado')   