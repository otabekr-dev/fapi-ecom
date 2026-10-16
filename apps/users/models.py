from typing import TYPE_CHECKING
import enum
from datetime import datetime
from sqlalchemy import String, DateTime, Enum, Boolean, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from apps.core.database import Base

if TYPE_CHECKING:
    from apps.sellers.models import SellerProfile

class Roles(enum.Enum):
    ADMIN = 'ADMIN'
    SELLER = 'SELLER'
    CUSTOMER = 'CUSTOMER'


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True)
    role: Mapped[Roles] = mapped_column(Enum(Roles), default=Roles.CUSTOMER)
    hashed_password: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default='true')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    seller_profile: Mapped['SellerProfile | None'] = relationship(back_populates='user', uselist=False)