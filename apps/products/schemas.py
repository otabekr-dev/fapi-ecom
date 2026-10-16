from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from datetime import datetime

class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    parent_id: int | None = None

class CategoryUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    parent_id: int | None = None

class CategoryOut(BaseModel):
    id: int
    name: str
    parent_id: int | None


    model_config = ConfigDict(from_attributes=True)


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str | None = None
    price: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    stock: int = Field(ge=0)
    seller_id: int
    category_id: int 
    is_active: bool = True

class ProductUpdate(BaseModel):
    name: str | None = Field(min_length=1, max_length=200, default=None)
    description: str | None = None
    price: Decimal | None = Field(gt=0, max_digits=10, decimal_places=2, default=None)
    stock: int | None = Field(ge=0, default=None)
    category_id: int | None = None
    is_active: bool | None = None

class ProductOut(BaseModel):
    id:int
    name:str
    description:str | None = None
    price: Decimal
    stock: int
    category_id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)