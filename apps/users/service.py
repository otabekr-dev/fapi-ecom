from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from apps.users import repository
from .schemas import UserCreate
from .models import User
from apps.core.security import hash_password, verify_password

def authenticate_user(db: Session, username:str, password:str) -> User:
    user = repository.get_user_by_username(db=db, username=username)

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            detail={'msg':'Incorrect password or username'},
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    return user

def register_user(db: Session, user_data:UserCreate)-> User:
    existing_user = repository.get_user_by_username(db, username=user_data.username)

    if existing_user:
        raise HTTPException(detail={'msg':'Username already taken'}, status_code=status.HTTP_400_BAD_REQUEST)

    hashed_password = hash_password(user_data.password)

    email = user_data.email

    if email is not None:
        email = email.strip().lower()
        if email == '':
            email = None

    user = repository.create_user(db, username=user_data.username, hashed_password=hashed_password, email=email)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user