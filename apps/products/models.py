from typing import TYPE_CHECKING
from sqlalchemy import String, DateTime, Text, Numeric, Integer, ForeignKey, Boolean, func, UniqueConstraint
from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from apps.core.database import Base
if TYPE_CHECKING:
    from apps.sellers.models import SellerProfile

class Category(Base):
    __tablename__ = 'categories'

    id : Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    parent_id : Mapped[int | None] = mapped_column(
        ForeignKey('categories.id'), nullable=True
    )

    parent : Mapped['Category | None'] = relationship(
        remote_side='Category.id',
        back_populates='children'
    )

    children : Mapped[list['Category']] = relationship(
        back_populates='parent'
    )

    products : Mapped[list['Product']] = relationship(back_populates='category')

    __table_args__ = (
        UniqueConstraint('parent_id', 'name', name='unique_category_parent_name',  postgresql_nulls_not_distinct=True),
    )

class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200))
    seller_id: Mapped[int] = mapped_column(ForeignKey('sellers.id'), index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    stock: Mapped[int] = mapped_column(Integer, default=0)
    category_id : Mapped[int] = mapped_column(ForeignKey('categories.id'), index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    category: Mapped[Category] = relationship(back_populates='products')

    seller: Mapped['SellerProfile'] = relationship()