from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from apps.carts.models import CartItems, Cart


def get_cart_by_user_id(db:Session, user_id:int) -> Cart | None:
    result = db.execute(select(Cart).where(Cart.user_id==user_id))
    return result.scalar_one_or_none()


def create_cart(db:Session, user_id:int) -> Cart:
    cart = Cart(
        user_id=user_id
    )

    db.add(cart)
    db.commit()
    db.refresh(cart)

    return cart

def get_item_by_product_id(db:Session, cart_id:int, product_id:int) -> CartItems | None:
    result = db.execute(select(CartItems).where(CartItems.cart_id==cart_id, CartItems.product_id==product_id))
    return result.scalar_one_or_none()


def get_item_by_id(db:Session, item_id:int, cart_id:int) -> CartItems | None:
    result = db.execute(select(CartItems).where(CartItems.id==item_id, CartItems.cart_id==cart_id))
    return result.scalar_one_or_none()


def add_item(db:Session, cart_id:int, product_id:int, quantity:int) -> CartItems:
    cart_item = CartItems(
        cart_id=cart_id,
        product_id=product_id,
        quantity=quantity
    )

    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)

    return cart_item


def update_item_quantity(db:Session, item:CartItems, quantity:int) -> CartItems:
    item.quantity = quantity

    db.commit()
    db.refresh(item)

    return item


def delete_item(db:Session, item:CartItems):
    db.delete(item)
    db.commit()


def clear_cart(db:Session, cart_id:int) -> None:
    result = db.execute(delete(CartItems).where(CartItems.cart_id==cart_id))
    db.commit()