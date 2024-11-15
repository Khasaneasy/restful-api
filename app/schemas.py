from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    is_active: bool

    class Config:
        orm_mode = True


class ReferalCode(BaseModel):
    expires_at: datetime


class ReferralCodeResponse(BaseModel):
    code: str
    owner_id: int
    expires_at: datetime

    class Config:
        orm_mode = True
