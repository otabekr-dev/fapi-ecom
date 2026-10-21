import enum 
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, Integer, CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.core.database import Base
from apps.products.models import Product


class Status(str, enum.Enum):
    PENDING = 'PENDING'
    PAID = 'PAID'
    SHIPPED = 'SHIPPED'
    DELIVERED = 'DELIVERED'
    CANCELLED = 'CANCELLED'


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    status: Mapped[Status] = mapped_column(Enum(Status), default=Status.PENDING)
    total_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    items: Mapped['OrderItem'] = relationship(back_populates='order')


class OrderItem(Base):
    __tablename__ = 'order_items'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id', ondelete='CASCADE'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    order : Mapped[Order] = relationship(back_populates='items')
    product : Mapped[Product] = relationship()

    __table_args__ = (
        CheckConstraint('quantity > 0', name='ordered_item_quantity'),
    )