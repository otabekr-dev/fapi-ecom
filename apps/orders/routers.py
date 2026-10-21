from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from apps.core.database import get_db
from apps.core.dependencies import require_admin, get_current_user
from apps.users.models import User
from apps.orders import service
from apps.orders.schemas import OrderItemOut, OrderOut, OrderStatusUpdate

router = APIRouter(prefix='/orders', tags=['orders'])

@router.post(path='/create', response_model=OrderOut, status_code=201)
def create_order(user:User = Depends(get_current_user), db: Session = Depends(get_db)):
    return service.checkout(db, user_id=user.id)

@router.get(path='/list', response_model=list[OrderOut], status_code=200)
def list_my_orders(
    user:User = Depends(get_current_user),
    skip:int = Query(ge=0, default=0),
    limit:int = Query(gt=0, le=100, default=20),
    db: Session = Depends(get_db)
):
    return service.list_my_orders(db, user_id=user.id, skip=skip, limit=limit)

@router.get(path='/get/{order_id}', response_model=OrderOut, status_code=200)
def get_my_order(order_id:int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return service.get_my_order(db, user_id=user.id, order_id=order_id)

@router.patch(path='/update/{order_id}', response_model=OrderOut, status_code=200, dependencies=[Depends(require_admin)])
def update_status(data:OrderStatusUpdate, order_id:int, db:Session = Depends(get_db)):
    return service.change_status(db, order_id=order_id, new_status=data.status)
