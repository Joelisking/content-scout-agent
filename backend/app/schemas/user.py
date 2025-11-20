from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.models.user import SubscriptionTier, PaymentProvider


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    company_name: Optional[str] = None
    country: str = Field(..., min_length=2, max_length=2)  # ISO country code


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    subscription_tier: SubscriptionTier
    payment_provider: Optional[PaymentProvider]
    blogs_created_this_month: int
    blog_limit: int
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    company_name: Optional[str] = None
    country: Optional[str] = None


class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)
