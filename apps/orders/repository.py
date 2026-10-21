from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from apps.orders.models import Order, OrderItem, Status
from decimal import Decimal

def create_order(db:Session, user_id:int, total_price:Decimal, items: list[dict]) -> Order:
    order = Order(
        user_id=user_id,
        total_price=total_price,
        items=[OrderItem(**item) for item in items]
    )

    db.add(order)
    db.flush()

    return order

def get_order_by_order_id(db:Session, order_id:int) -> Order | None:
    result = db.execute(select(Order).where(Order.id==order_id).options(selectinload(Order.items).selectinload(OrderItem.product)))
    return result.scalar_one_or_none()

def get_order_by_user_id(db:Session, user_id:int, skip: int=0, limit: int=20) -> Order | None:
    result = db.execute(select(Order).where(Order.user_id==user_id).order_by(Order.id).offset(skip).limit(limit))

    return list(result.scalars().all())

def update_status(db: Session, order:Order, new_status: Status) -> Order:
    order.status=new_status

    db.commit()

    return get_order_by_order_id(db, order_id=order.id)