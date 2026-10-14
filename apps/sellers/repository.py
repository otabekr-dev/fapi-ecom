from sqlalchemy.orm import Session
from apps.sellers.models import SellerProfile


def get_seller_by_id(db:Session, seller_id:int) -> SellerProfile | None:
    return db.query(SellerProfile).filter(SellerProfile.id==seller_id).first()

def get_seller_by_user_id(db: Session, user_id:int) -> SellerProfile | None:
    return db.query(SellerProfile).filter(SellerProfile.user_id==user_id).first()

def get_seller_by_shop_name(db:Session, shop_name:str)-> SellerProfile | None:
    return db.query(SellerProfile).filter(SellerProfile.shop_name==shop_name).first()

def create_seller(db:Session, shop_name:str, user_id:int, description:str | None = None)-> SellerProfile:
    seller = SellerProfile(shop_name=shop_name, description=description, user_id=user_id)

    db.add(seller)
    db.flush()

    return seller

def update_seller(
    db: Session,
    seller: SellerProfile,
    shop_name: str | None = None,
    description: str | None = None
)-> SellerProfile:

    seller_shop_name = seller.shop_name
    seller_description = seller.description

    if shop_name is not None:
        seller.shop_name = shop_name


    if description is not None:
        seller.description = description

    db.commit()
    db.refresh(seller)

    return seller

def list_sellers(
    db: Session,
    skip:int = 0,
    limit:int = 20,
    is_active: bool | None = None 
)-> list[SellerProfile]:
    query = db.query(SellerProfile)

    if is_active is not None:
        query = query.filter(SellerProfile.is_active==is_active)

    return query.order_by(SellerProfile.id).offset(skip).limit(limit).all()
