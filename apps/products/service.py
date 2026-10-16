from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from sqlalchemy import select
from apps.products import repository
from apps.products.models import Product, Category
from apps.products.schemas import CategoryUpdate, CategoryCreate, ProductUpdate, ProductCreate

def create_category(
    db: Session,
    category_data: CategoryCreate
) -> Category:
    parent_id = category_data.parent_id

    if parent_id is not None:
        parent = repository.get_category_by_id(db, category_id=parent_id)

        if parent is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Parent category not found"
            )

    return repository.create_category(
        db,
        name=category_data.name,
        parent_id=parent_id
    )


def get_categories(db: Session) -> list[Category]:
    return repository.get_categories(db)


def retrieve_category(
    db: Session,
    category_id: int
) -> Category:
    category = repository.get_category_by_id(db, category_id=category_id)

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    return category


def update_category(
    db: Session,
    category_id: int,
    update_data: CategoryUpdate
) -> Category:
    category = repository.get_category_by_id(db, category_id=category_id)

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    data = update_data.model_dump(exclude_unset=True)

    if "parent_id" in data:
        current_parent_id = data["parent_id"]

        while current_parent_id is not None:
            if current_parent_id == category.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Circular hierarchy is not allowed"
                )

            parent = repository.get_category_by_id(
                db,
                category_id=current_parent_id
            )

            if parent is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Parent category not found"
                )

            current_parent_id = parent.parent_id

    return repository.update_category(
        db,
        category=category,
        update_data=update_data
    )


def create_product(
    db: Session,
    product_data: ProductCreate
) -> Product:
    category = repository.get_category_by_id(
        db,
        category_id=product_data.category_id
    )

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    return repository.create_product(
        db,
        name=product_data.name,
        price=product_data.price,
        stock=product_data.stock,
        category_id=product_data.category_id,
        description=product_data.description,
        seller_id=product_data.seller_id
    )


def retrieve_product(
    db: Session,
    product_id: int
) -> Product:
    product = repository.get_product_by_id(db, product_id=product_id)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return product


def update_product(
    db: Session,
    product_id: int,
    product_update: ProductUpdate
) -> Product:
    product = repository.get_product_by_id(db, product_id=product_id)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    data = product_update.model_dump(exclude_unset=True)

    if "category_id" in data and data["category_id"] is not None:
        category = repository.get_category_by_id(
            db,
            category_id=data["category_id"]
        )

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )

    return repository.update_product(
        db,
        product=product,
        update_data=product_update
    )


def list_products(
    db: Session,
    category_id: int | None = None,
    skip: int = 0,
    limit: int = 20
) -> list[Product]:
    return repository.get_products(
        db,
        skip=skip,
        limit=limit,
        category_id=category_id
    )