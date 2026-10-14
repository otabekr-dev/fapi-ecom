from pydantic import BaseModel, Field, ConfigDict
from .models import Roles
from datetime import datetime

class UserCreate(BaseModel):
    username: str = Field(min_length=5, max_length=50)
    password: str = Field(min_length=8, max_length=64)
    email: str = Field(min_length=8, max_length=255, default=None) 

class UserOut(BaseModel):
    id: int
    username: str
    email: str | None = None
    role: Roles
    created_at: datetime


    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
