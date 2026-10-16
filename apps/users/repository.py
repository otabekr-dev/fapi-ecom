from sqlalchemy.orm import Session
from .models import User
from sqlalchemy import select

def get_user_by_username(db: Session, username:str) -> User | None:
    result = db.execute(select(User).where(User.username==username))
    return result.scalar_one_or_none()

def get_user_by_id(db: Session, user_id:int) -> User | None:
    result = db.execute(select(User).where(User.id==user_id))

    return result.scalar_one_or_none()

def get_user_by_email(db: Session, email:str) -> User:
    result = db.execute(select(User).where(User.email==email))
    return result.scalar_one_or_none()


def create_user(db: Session, username:str, hashed_password:str, email: str | None = None) -> User:
    if email is not None:
        email = email.strip().lower()
        if email == '':
            email = None

    user = User(
        username=username.lower(),
        email=email,
        hashed_password=hashed_password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
