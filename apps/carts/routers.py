from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from apps.core.database import get_db
from apps.core.dependencies import get_current_user
from apps.carts import service
from apps.carts.schemas import CartItemAdd, CartItemUpdate
from apps.users.models import User


router = APIRouter(prefix='/carts', tags=['Cart API'])


@router.get(path='/list', status_code=status.HTTP_200_OK)
def get_cart(db:Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return service.get_or_create_cart(db, user_id=current_user.id)

@router.post(path='/items', status_code=status.HTTP_201_CREATED)
def add_item(item_data:CartItemAdd, current_user:User = Depends(get_current_user), db: Session = Depends(get_db)):
    return service.add_item(db, item_data=item_data, user_id=current_user.id)

@router.patch(path='/items/{item_id}/', status_code=status.HTTP_200_OK)
def update_item(data: CartItemUpdate, item_id:int, db:Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return service.update_item_quantity(db, update_data=data, user_id=current_user.id, item_id=item_id)

@router.delete(path='/items/{item_id}/', status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id:int, db:Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return service.delete_item(db, item_id=item_id, user_id=current_user.id)

@router.delete(path='/clear/{item_id}/', status_code=status.HTTP_204_NO_CONTENT)
def clear_cart(db: Session = Depends(get_db), current_user:User = Depends(get_current_user)):
    return service.clear_cart(db, user_id=current_user.id)