from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from apps.carts import repository
from apps.products import repository as product_repository
from apps.carts.schemas import CartItemAdd, CartItemUpdate


def get_or_create_cart(db:Session, user_id:int):
    existing_cart = repository.get_cart_by_user_id(db, user_id=user_id)

    if existing_cart:
        return existing_cart

    new_cart = repository.create_cart(db, user_id=user_id)

    return new_cart

def get_cart(db:Session, user_id:int):
    cart = repository.get_cart_by_user_id(db, user_id=user_id)

    if cart is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'msg':'Cart not found'}
        )

    return cart

def add_item(db:Session, item_data:CartItemAdd, user_id:int):
    if item_data.quantity <= 0:
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={'msg':'Quantity can not be negative'}
        )

    cart = get_or_create_cart(db, user_id=user_id)

    product = product_repository.get_product_by_id(db, product_id=item_data.product_id)

    if product is None or not product.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'msg':'Product not found'}
        )

    if product.stock < item_data.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={'msg':'Stock not enough'}
        )

    item = repository.get_item_by_product_id(db, cart_id=cart.id, product_id=product.id)

    if item:
        new_quantity = item.quantity + item_data.quantity

        if new_quantity > product.stock:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={'msg':'Stock not enough'}
            )

        return repository.update_item_quantity(db, item=item, quantity=new_quantity)

    return repository.add_item(db, cart_id=cart.id, product_id=product.id, quantity=item_data.quantity)

def update_item_quantity(db:Session, update_data:CartItemUpdate, user_id:int, item_id:int):
    if update_data.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={'msg':'Quantity cannot be negative'}
        )

    cart = get_cart(db, user_id=user_id)

    item = repository.get_item_by_id(db, item_id=item_id, cart_id=cart.id)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'msg':'Item not found'}
        )

    if update_data.quantity > item.product.stock:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={'msg':'Stock not enough'}
        )

    return repository.update_item_quantity(db, item=item, quantity=update_data.quantity)

def delete_item(db:Session, item_id:int, user_id:int):
    cart = get_cart(db, user_id=user_id)

    item = repository.get_item_by_id(db, item_id=item_id, cart_id=cart.id)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'msg':'Item Not Found'}
        )

    repository.delete_item(db, item=item)

def clear_cart(db:Session, user_id:int):
    cart = get_cart(db, user_id=user_id)
    repository.clear_cart(db, cart_id=cart.id)
