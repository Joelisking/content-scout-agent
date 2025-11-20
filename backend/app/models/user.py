from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class SubscriptionTier(str, enum.Enum):
    FREE = "free"
    STARTER = "starter"
    PRO = "pro"


class PaymentProvider(str, enum.Enum):
    STRIPE = "stripe"
    PAYSTACK = "paystack"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    company_name = Column(String, nullable=True)
    country = Column(String, nullable=False)  # ISO country code (e.g., "GH", "US")
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    # Subscription details
    subscription_tier = Column(
        Enum(SubscriptionTier),
        default=SubscriptionTier.FREE,
        nullable=False
    )
    payment_provider = Column(Enum(PaymentProvider), nullable=True)
    stripe_customer_id = Column(String, nullable=True)
    paystack_customer_code = Column(String, nullable=True)
    subscription_id = Column(String, nullable=True)  # Stripe/Paystack subscription ID
    subscription_status = Column(String, nullable=True)  # active, canceled, past_due
    current_period_end = Column(DateTime(timezone=True), nullable=True)

    # Usage tracking
    blogs_created_this_month = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    research_jobs = relationship("ResearchJob", back_populates="user")
    blogs = relationship("Blog", back_populates="user")

    def can_create_blog(self) -> bool:
        """Check if user can create another blog based on their tier"""
        from app.core.config import settings

        if self.subscription_tier == SubscriptionTier.FREE:
            return self.blogs_created_this_month < settings.FREE_TIER_BLOG_LIMIT
        elif self.subscription_tier == SubscriptionTier.STARTER:
            return self.blogs_created_this_month < settings.STARTER_TIER_BLOG_LIMIT
        elif self.subscription_tier == SubscriptionTier.PRO:
            return True  # Unlimited
        return False

    def get_blog_limit(self) -> int:
        """Get the blog limit for user's current tier"""
        from app.core.config import settings

        if self.subscription_tier == SubscriptionTier.FREE:
            return settings.FREE_TIER_BLOG_LIMIT
        elif self.subscription_tier == SubscriptionTier.STARTER:
            return settings.STARTER_TIER_BLOG_LIMIT
        elif self.subscription_tier == SubscriptionTier.PRO:
            return -1  # Unlimited
        return 0
