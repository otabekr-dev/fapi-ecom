from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import String, DateTime, Boolean, func, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from apps.users.models import User

from apps.core.database import Base

class SellerProfile(Base):
    __tablename__ = 'sellers'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id : Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), unique=True)
    shop_name : Mapped[str] = mapped_column(String(100), unique=True)
    description : Mapped[str|None] = mapped_column(Text, nullable=True)
    is_active : Mapped[bool] = mapped_column(Boolean, server_default='true', default=True)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user : Mapped['User']= relationship(back_populates='seller_profile')