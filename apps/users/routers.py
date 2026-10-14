from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from apps.core.database import get_db
from apps.users import service
from apps.users.schemas import UserCreate, UserOut, Token
from apps.users.models import User
from apps.core.dependencies import get_current_user
from apps.core.security import create_access_token


router = APIRouter(prefix='/auth', tags=['authentication'])

@router.post('/register', response_model=UserOut, status_code=201)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    return service.register_user(db, user_data=user_data)

@router.post('/login', response_model=Token, status_code=200)
def login(
    form_data:OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = service.authenticate_user(db, form_data.username, form_data.password)
    access_token = create_access_token({'sub':user.username})
    return {'access_token':access_token, 'token_type':'bearer'}

@router.get('/me', response_model=UserOut, status_code=200)
def me(current_user: User = Depends(get_current_user)):
    return current_user