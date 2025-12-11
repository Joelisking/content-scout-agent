from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # App
    PROJECT_NAME: str = "Content Scout"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days

    # Database
    DATABASE_URL: str

    # Redis
    REDIS_URL: str

    # Claude AI
    ANTHROPIC_API_KEY: str
    AI_MODEL: Optional[str] = None  # Optional, defaults to hardcoded model in service

    # Email
    RESEND_API_KEY: str = ""
    FROM_EMAIL: str = "noreply@contentscout.com"
    ADMIN_EMAIL: str = "admin@contentscout.com"

    # Payments
    STRIPE_SECRET_KEY: str
    STRIPE_PUBLISHABLE_KEY: str
    STRIPE_WEBHOOK_SECRET: Optional[str] = None

    PAYSTACK_SECRET_KEY: str
    PAYSTACK_PUBLIC_KEY: str

    # Frontend
    FRONTEND_URL: str = "http://localhost:3000"

    # Environment
    ENVIRONMENT: str = "development"

    # Storage
    STORAGE_PATH: str = "/tmp/content-scout-blogs"
    USE_S3: bool = False
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_S3_BUCKET: Optional[str] = None
    AWS_REGION: Optional[str] = "us-east-1"

    # Subscription tiers
    FREE_TIER_BLOG_LIMIT: int = 3
    STARTER_TIER_BLOG_LIMIT: int = 20
    PRO_TIER_BLOG_LIMIT: int = -1  # Unlimited

    # Pricing (in cents for Stripe, kobo for Paystack)
    STARTER_PRICE_USD: int = 2900  # $29.00
    PRO_PRICE_USD: int = 9900      # $99.00

    # Paystack pricing in NGN (Nigerian Naira)
    STARTER_PRICE_NGN: int = 1500000  # ₦15,000
    PRO_PRICE_NGN: int = 5000000      # ₦50,000

    # Countries using Paystack (African countries)
    PAYSTACK_COUNTRIES: list = [
        "NG",  # Nigeria
        "GH",  # Ghana
        "ZA",  # South Africa
        "KE",  # Kenya
        "EG",  # Egypt
        "CI",  # Côte d'Ivoire
    ]

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra environment variables


settings = Settings()
