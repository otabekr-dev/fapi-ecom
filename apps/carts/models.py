from typing import TYPE_CHECKING
from sqlalchemy import DateTime, ForeignKey, Integer, UniqueConstraint, CheckConstraint
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func
from apps.core.database import Base

if TYPE_CHECKING:
    from apps.products.models import Product


class Cart(Base):
    __tablename__ = 'carts'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id : Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    items : Mapped[list['CartItems']] = relationship(
        back_populates='cart',
        cascade='all, delete-orphan'
    )


class CartItems(Base):
    __tablename__ = 'cart_items'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey('carts.id', ondelete='CASCADE'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id', ondelete='CASCADE'))
    quantity: Mapped[int] = mapped_column(Integer, default=1, server_default='1')

    cart: Mapped['Cart'] = relationship(back_populates='items')
    product: Mapped['Product'] = relationship()

    __table_args__ = (
        UniqueConstraint('cart_id', 'product_id'),
        CheckConstraint('quantity > 0', name='cart_item_quantity_positive')
    )