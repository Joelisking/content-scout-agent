from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import create_access_token, verify_password, get_password_hash
from app.core.deps import get_current_user
from app.models import User
from app.models.user import SubscriptionTier, PaymentProvider
from app.schemas import UserCreate, UserLogin, TokenResponse, UserResponse
from app.services.email_service import EmailService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Determine payment provider based on country
    from app.services.payment_service import PaymentService
    payment_service = PaymentService()
    payment_provider = payment_service.get_payment_provider(user_data.country)

    # Create new user
    user = User(
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        full_name=user_data.full_name,
        company_name=user_data.company_name,
        country=user_data.country.upper(),
        subscription_tier=SubscriptionTier.FREE,
        payment_provider=payment_provider,
        is_active=True,
        is_verified=False,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    logger.info(f"New user registered: {user.email} (ID: {user.id})")

    # Send welcome email
    email_service = EmailService()
    try:
        await email_service.send_welcome_email(user.email, user.full_name)
    except Exception as e:
        logger.error(f"Failed to send welcome email: {str(e)}")
        # Don't fail registration if email fails

    # Create access token
    access_token = create_access_token(data={"sub": str(user.id)})

    # Build user response
    user_response = UserResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        company_name=user.company_name,
        country=user.country,
        is_active=user.is_active,
        is_verified=user.is_verified,
        subscription_tier=user.subscription_tier,
        payment_provider=user.payment_provider,
        blogs_created_this_month=user.blogs_created_this_month,
        blog_limit=user.get_blog_limit(),
        created_at=user.created_at,
    )

    return TokenResponse(
        access_token=access_token,
        user=user_response
    )


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user"""
    # Find user by email
    user = db.query(User).filter(User.email == credentials.email).first()

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )

    # Create access token
    access_token = create_access_token(data={"sub": str(user.id)})

    # Build user response
    user_response = UserResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        company_name=user.company_name,
        country=user.country,
        is_active=user.is_active,
        is_verified=user.is_verified,
        subscription_tier=user.subscription_tier,
        payment_provider=user.payment_provider,
        blogs_created_this_month=user.blogs_created_this_month,
        blog_limit=user.get_blog_limit(),
        created_at=user.created_at,
    )

    logger.info(f"User logged in: {user.email}")

    return TokenResponse(
        access_token=access_token,
        user=user_response
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        company_name=current_user.company_name,
        country=current_user.country,
        is_active=current_user.is_active,
        is_verified=current_user.is_verified,
        subscription_tier=current_user.subscription_tier,
        payment_provider=current_user.payment_provider,
        blogs_created_this_month=current_user.blogs_created_this_month,
        blog_limit=current_user.get_blog_limit(),
        created_at=current_user.created_at,
    )
