from pydantic import BaseModel,ConfigDict, computed_field
from apps.products.schemas import ProductOut
from decimal import Decimal
from apps.orders.models import Status
from datetime import datetime

class OrderItemOut(BaseModel):
    id:int
    product_id:int
    quantity: int
    price: Decimal
    products: ProductOut

    model_config = ConfigDict(from_attributes=True)

    @computed_field
    @property
    def subtotal(self) -> Decimal:
        return self.quantity * self.price

class OrderOut(BaseModel):
    id:int
    status: Status
    total_price: Decimal
    created_at: datetime
    items: list[OrderItemOut]

    model_config = ConfigDict(from_attributes=True)

class OrderStatusUpdate(BaseModel):
    status: Status    