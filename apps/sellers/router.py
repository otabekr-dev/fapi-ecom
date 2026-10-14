from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from apps.core.database import get_db
from apps.sellers import service
from apps.sellers.schemas import SellerUpdate, SellerCreate, SellerOut
from apps.sellers.models import SellerProfile
from apps.core.dependencies import require_seller_or_admin, get_current_user, get_current_seller
from apps.users.models import Roles, User

router = APIRouter(prefix='/sellers', tags=['Sellers-API'])

@router.post(path='/create', response_model=SellerOut, status_code=201)
def create_seller(
    seller_data: SellerCreate,
    user_id: int | None = None,
    current_user:User = Depends(get_current_user),
    db:Session = Depends(get_db)
):

    if current_user.role == Roles.CUSTOMER:
        user_id = current_user.id
    elif current_user.role == Roles.ADMIN:
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={'msg':'admin must provide user id'}
            )

    return service.create_seller(db, seller_data=seller_data, user_id=user_id)

@router.patch(path='/update', response_model=SellerOut, status_code=200)
def update(
    upd_data: SellerUpdate,
    db: Session = Depends(get_db),
    seller: SellerProfile = Depends(get_current_seller)
):
    return service.update_seller(db, seller=seller, upd_data=upd_data)