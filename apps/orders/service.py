from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from decimal import Decimal
from apps.orders.models import Order, OrderItem, Status
from apps.products import repository as prod_repo
from apps.carts import repository as cart_repo
from apps.orders import repository

ALLOWED_TRANSITIONS = {
    Status.PENDING: [Status.CANCELLED, Status.PAID],
    Status.PAID: [Status.SHIPPED, Status.CANCELLED],
    Status.SHIPPED: [Status.DELIVERED],
    Status.DELIVERED: [],
    Status.CANCELLED: []
}

def checkout(db: Session, user_id:int) -> Order:
    cart = cart_repo.get_cart_by_user_id(db, user_id=user_id)

    if cart is None or not cart.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={'msg':'Empty cart'}
        )

    product_ids = []

    for product in cart.items:
        product_ids.append(product.id)


    prod_repo.get_product_for_update(db, product_ids=product_ids)

    order_items = []
    total_price = Decimal(0)

    for item in cart.items:
        product = item.product

        if not product.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={'msg':f'Product {product.name} is not available'}
            )

        if item.quantity > product.stock:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={'msg':'Stock not enough'}
            )

        order_items.append({
            'product_id':product.id,
            'quantity': item.quantity,
            'price': product.price
        })

        total_price += item.quantity * product.price


    order = repository.create_order(db, user_id=user_id, total_price=total_price, items=order_items)

    for item in cart.items:
        item.product.stock -= item.quantity

    cart_repo.clear_cart(db, cart_id=cart.id)

    db.commit()
    db.refresh(order)

    return order

def list_my_orders(db:Session, user_id:int, skip:int = 0, limit:int = 20) -> list[Order]:
    result = repository.get_order_by_user_id(db, user_id=user_id, skip=skip, limit=limit)

    return result

def get_my_order(db:Session, user_id:int, order_id:int) -> Order:
    order = repository.get_order_by_order_id(db, order_id=order_id)

    if order is None or order.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={'msg':'Order not found'}
        )

    return order

def change_status(db:Session, order_id:int, new_status:Status) -> Order:
    order = repository.get_order_by_order_id(db, order_id=order_id)

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'msg':'Order not found'}
        )

    if new_status not in ALLOWED_TRANSITIONS[order.status]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={'msg':f'Cannot change status from {order.status.value} to {new_status.value}'}
        )

    if new_status == Status.CANCELLED and order.status != Status.CANCELLED:
        product_ids = []

        for item in order.items:
            product_ids.append(item.product_id)

        prod_repo.get_product_for_update(db, product_ids=product_ids)

        for item in order.items:
            item.product.stock += item.quantity

    return repository.update_status(db, order=order, new_status=new_status)