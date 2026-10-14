from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from apps.sellers import repository
from apps.sellers.schemas import SellerCreate, SellerUpdate
from apps.sellers.models import SellerProfile
from apps.users.models import Roles
from apps.users import repository as users_repository


def create_seller(db:Session, seller_data: SellerCreate, user_id:int) -> SellerProfile:
    user = users_repository.get_user_by_id(db, user_id=user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'msg':'user not found'}
        )

    if repository.get_seller_by_user_id(db, user_id=user_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={'msg':'This user already have a shop'}
        )

    shop_name = seller_data.shop_name.strip()

    if repository.get_seller_by_shop_name(db, shop_name=shop_name):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={'msg':'Shop name is already taken'}
        )

    try:
        seller = repository.create_seller(db, shop_name=shop_name, description=seller_data.description, user_id=user_id)

        if user.role == Roles.CUSTOMER:
            user.role = Roles.SELLER

        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={'Shop name is already taken'}
        )


    db.refresh(seller)

    return seller

def update_seller(db: Session, seller: SellerProfile, upd_data:SellerUpdate)-> SellerProfile:
    fields = upd_data.model_dump()

    shop_name = fields.get('shop_name')
    description = fields.get('description')

    if shop_name is not None:
        shop_name = shop_name.strip()

        if shop_name != seller.shop_name:
            existing = repository.get_seller_by_shop_name(db, shop_name=shop_name)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail={'msg':'Shop name is already taken'}
                )

    try:
        return repository.update_seller(db, seller=seller, shop_name=shop_name, description=description)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={'msg':'Shop name is already taken'}
        )            

    