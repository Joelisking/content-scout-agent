from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.user import SubscriptionTier, PaymentProvider


class SubscriptionCreate(BaseModel):
    tier: SubscriptionTier
    payment_method_id: Optional[str] = None  # Stripe payment method ID or Paystack authorization code


class SubscriptionResponse(BaseModel):
    tier: SubscriptionTier
    payment_provider: Optional[PaymentProvider]
    status: Optional[str]
    current_period_end: Optional[datetime]
    blogs_created_this_month: int
    blog_limit: int


class PricingInfo(BaseModel):
    tier: SubscriptionTier
    price_usd: Optional[int] = None
    price_local: Optional[int] = None
    currency: str
    blogs_per_month: int
    features: list[str]


class PaymentMethodResponse(BaseModel):
    payment_provider: PaymentProvider
    publishable_key: str


class WebhookEvent(BaseModel):
    """For handling Stripe/Paystack webhooks"""
    type: str
    data: dict
