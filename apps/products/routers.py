from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from apps.core.database import get_db
from apps.core.dependencies import require_admin, require_product_owner_or_admin, require_seller_or_admin
from apps.products import service
from apps.products.schemas import CategoryCreate, CategoryOut, CategoryUpdate, ProductUpdate, ProductCreate, ProductOut


p_router = APIRouter(prefix='/products', tags=['Product API'])
c_router = APIRouter(prefix='/categories', tags=['Category API'])


@c_router.post(path='/create', response_model=CategoryOut, status_code=201, dependencies=[Depends(require_admin)])
def create_category(category_data: CategoryCreate, db: Session = Depends(get_db)):
    return service.create_category(db, category_data)


@c_router.get(path='/list', response_model=list[CategoryOut], status_code=200)
def get_categories(db: Session = Depends(get_db)):
    return service.get_categories(db)


@c_router.patch(path='/update/{category_id}/', response_model=CategoryOut, status_code=200, dependencies=[Depends(require_admin)])
def update_category(category_id: int, update_data: CategoryUpdate, db: Session = Depends(get_db)):
    return service.update_category(db, category_id=category_id, update_data=update_data)


@p_router.post(path='/create', response_model=ProductOut, status_code=201, dependencies=[Depends(require_seller_or_admin)])
def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    return service.create_product(db, product_data=product_data)


@p_router.get(path='/list', response_model=list[ProductOut], status_code=200)
def get_products(
    category_id: int | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return service.list_products(db, category_id=category_id, skip=skip, limit=limit)


@p_router.get('/retrieve/{product_id}/', response_model=ProductOut, status_code=200)
def retrieve_product(product_id: int, db: Session = Depends(get_db)):
    return service.retrieve_product(db, product_id=product_id)


@p_router.patch(path='/update/{product_id}/', response_model=ProductOut, status_code=200, dependencies=[Depends(require_product_owner_or_admin)])
def update_product(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)):
    return service.update_product(db, product_id=product_id, product_update=product_update)