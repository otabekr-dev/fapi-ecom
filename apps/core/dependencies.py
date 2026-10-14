from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from apps.core.database import get_db
from apps.users import repository
from apps.users.models import User, Roles
from .security import decode_access_token

from apps.sellers import repository as seller_repo

oauth2 = OAuth2PasswordBearer(tokenUrl='auth/login')

def get_current_user(
    token:str=Depends(oauth2),
    db: Session = Depends(get_db)
) -> User:
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            detail={'msg':'Could not validate credentials'},
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    username = payload.get('sub')

    if username is None:
        raise HTTPException(
            detail={'msg':'Could not validate credentials'},
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    user = repository.get_user_by_username(db=db,username=username)

    if user is None:
        raise HTTPException(
            detail={'msg':'Could not validate credentials'},
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    return user

def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != Roles.ADMIN:
        raise HTTPException(
            detail={'msg':'User is not admin'},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    return current_user

def require_seller_or_admin(current_user: User = Depends(get_current_user)):
    if current_user.role not in (Roles.ADMIN, Roles.SELLER):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={'msg':'User is not seller or admin'}
        )

    return current_user


def get_current_seller(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    seller = seller_repo.get_seller_by_user_id(db, user_id=current_user.id)

    if seller is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'msg':'Seller not found'}
        )


    return seller