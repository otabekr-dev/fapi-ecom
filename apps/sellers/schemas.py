from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class SellerCreate(BaseModel):
    shop_name: str = Field(max_length=300)
    description: str | None = None


class SellerUpdate(BaseModel):
    shop_name: str | None = Field(max_length=300, default=None)
    description: str| None = None

class SellerOut(BaseModel):
    id:int
    shop_name:str
    description:str | None = None
    is_active: bool
    created_at: datetime


    model_config = ConfigDict(from_attributes=True)