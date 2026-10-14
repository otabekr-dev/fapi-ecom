from sqlalchemy.orm import Session
from .models import User

def get_user_by_username(db: Session, username:str) -> User | None:
    return db.query(User).filter(User.username==username.lower()).first()

def get_user_by_id(db: Session, user_id:int) -> User | None:
    return db.query(User).filter(User.id==user_id).first()


def get_user_by_email(db: Session, email:str) -> User:
    return db.query(User).filter(User.email==email).first()


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
