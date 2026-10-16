from sqlalchemy.orm import Session
from decimal import Decimal
from apps.products.models import Category, Product
from apps.products.schemas import ProductUpdate, CategoryUpdate
from sqlalchemy import select

def get_category_by_id(db:Session, category_id:int)-> Category|None:
    result = db.execute(select(Category).where(Category.id==category_id))
    return result.scalar_one_or_none()

def get_category_by_name(db:Session, category_name:str)-> Category|None:
    result = db.execute(select(Category).where(Category.name==category_name))
    return result.scalar_one_or_none()

def get_categories(db:Session)-> list[Category]:
    result = db.execute(select(Category).order_by(Category.id))
    return list(result.scalars().all())

def create_category(db: Session, name:str, parent_id:int | None = None) -> Category:
    category = Category(name=name, parent_id=parent_id)

    db.add(category)
    db.commit()
    db.refresh(category)

    return category

def update_category(db:Session, category:Category, update_data: CategoryUpdate) -> Category:
    data = update_data.model_dump(exclude_unset=True)

    for field, value in data.items():
        setattr(category, field, value)

    db.commit()
    db.refresh(category)

    return category


def get_product_by_id(db:Session, product_id:int)-> Product | None:
    result = db.execute(select(Product).where(Product.id==product_id))
    return result.scalar_one_or_none()


def create_product(
    db: Session,
    seller_id: int,
    name: str,
    price: Decimal,
    stock: int,
    category_id:int,
    description: str | None = None
)-> Product:
    product = Product(
        name=name,
        price=price,
        stock=stock,
        category_id=category_id,
        description=description,
        seller_id=seller_id
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product

def get_products(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    category_id: int | None = None
)-> list[Product]:
    query = select(Product).where(Product.is_active.is_(True))

    if category_id is not None:
        query = query.where(Product.category_id==category_id)

    query = query.order_by(Product.id).offset(skip).limit(limit)

    result = db.execute(query)

    return list(result.scalars().all())

def update_product(
    db: Session,
    product: Product,
    update_data: ProductUpdate
)-> Product:
    data = update_data.model_dump(exclude_unset=True)

    for field, value in data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)

    return product

def get_product_for_update(db: Session, product_ids:list[int])-> list[Product]:
    result = db.execute(
        select(Product)
        .where(Product.id.in_(product_ids))
        .order_by(Product.id)
        .with_for_update()
        .execution_options(populate_existing=True)
    )

    return list(result.scalars().all())