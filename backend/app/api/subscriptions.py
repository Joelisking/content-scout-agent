from fastapi import APIRouter, Depends, HTTPException, status, Request, Header
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models import User, SubscriptionTier
from app.schemas import (
    SubscriptionCreate,
    SubscriptionResponse,
    PricingInfo,
    PaymentMethodResponse,
)
from app.services.payment_service import PaymentService
from app.services.email_service import EmailService
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])


@router.get("/pricing", response_model=list[PricingInfo])
async def get_pricing(current_user: User = Depends(get_current_user)):
    """Get pricing information for user's country"""
    payment_service = PaymentService()
    pricing = payment_service.get_pricing_info(current_user.country)
    return pricing


@router.get("/payment-method", response_model=PaymentMethodResponse)
async def get_payment_method(current_user: User = Depends(get_current_user)):
    """Get payment method details (Stripe or Paystack) for user's country"""
    payment_service = PaymentService()
    payment_info = payment_service.get_publishable_key(current_user.country)

    return PaymentMethodResponse(
        payment_provider=payment_info["provider"],
        publishable_key=payment_info["publishable_key"],
    )


@router.get("/current", response_model=SubscriptionResponse)
async def get_current_subscription(current_user: User = Depends(get_current_user)):
    """Get current user's subscription details"""
    return SubscriptionResponse(
        tier=current_user.subscription_tier,
        payment_provider=current_user.payment_provider,
        status=current_user.subscription_status,
        current_period_end=current_user.current_period_end,
        blogs_created_this_month=current_user.blogs_created_this_month,
        blog_limit=current_user.get_blog_limit(),
    )


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_subscription(
    subscription_data: SubscriptionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new subscription (upgrade/change plan)"""
    # Validate tier
    if subscription_data.tier == SubscriptionTier.FREE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot subscribe to free tier"
        )

    payment_service = PaymentService()

    try:
        # Determine which payment provider to use
        if current_user.payment_provider.value == "stripe":
            # Create Stripe subscription
            result = await payment_service.create_subscription_stripe(
                user=current_user,
                tier=subscription_data.tier,
                payment_method_id=subscription_data.payment_method_id,
            )

            # Update user in database
            current_user.subscription_tier = subscription_data.tier
            current_user.subscription_id = result["subscription_id"]
            current_user.subscription_status = result["status"]
            current_user.current_period_end = datetime.fromtimestamp(
                result["current_period_end"]
            )

            db.commit()

            # Send confirmation email
            email_service = EmailService()
            pricing = payment_service.get_pricing_info(current_user.country)
            tier_pricing = next(
                (p for p in pricing if p["tier"] == subscription_data.tier), None
            )

            if tier_pricing:
                await email_service.send_subscription_confirmation(
                    to_email=current_user.email,
                    user_name=current_user.full_name,
                    tier=subscription_data.tier.value,
                    amount=tier_pricing["price"],
                    currency=tier_pricing["currency"],
                )

            return {
                "status": "success",
                "message": "Subscription created successfully",
                "client_secret": result.get("client_secret"),
            }

        else:  # Paystack
            # Create Paystack subscription
            result = await payment_service.create_subscription_paystack(
                user=current_user,
                tier=subscription_data.tier,
                authorization_code=subscription_data.payment_method_id,
            )

            # For Paystack, we return the authorization URL
            # User will be redirected to complete payment
            return {
                "status": "redirect",
                "authorization_url": result["authorization_url"],
                "reference": result["reference"],
            }

    except Exception as e:
        logger.error(f"Failed to create subscription: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/cancel", status_code=status.HTTP_200_OK)
async def cancel_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Cancel current subscription"""
    if current_user.subscription_tier == SubscriptionTier.FREE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No active subscription to cancel"
        )

    payment_service = PaymentService()

    try:
        # Cancel subscription based on payment provider
        if current_user.payment_provider.value == "stripe":
            success = await payment_service.cancel_subscription_stripe(current_user)
        else:
            success = await payment_service.cancel_subscription_paystack(current_user)

        if success:
            # Update user
            current_user.subscription_tier = SubscriptionTier.FREE
            current_user.subscription_id = None
            current_user.subscription_status = "canceled"

            db.commit()

            return {
                "status": "success",
                "message": "Subscription canceled successfully"
            }
        else:
            raise Exception("Failed to cancel subscription")

    except Exception as e:
        logger.error(f"Failed to cancel subscription: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/webhook/stripe")
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(None, alias="stripe-signature"),
    db: Session = Depends(get_db),
):
    """Handle Stripe webhooks"""
    payment_service = PaymentService()

    try:
        payload = await request.body()
        event = payment_service.construct_stripe_webhook_event(
            payload, stripe_signature
        )

        # Handle different event types
        if event["type"] == "invoice.payment_succeeded":
            # Payment successful, ensure subscription is active
            subscription_id = event["data"]["object"]["subscription"]
            customer_id = event["data"]["object"]["customer"]

            user = db.query(User).filter(
                User.stripe_customer_id == customer_id
            ).first()

            if user:
                user.subscription_status = "active"
                db.commit()
                logger.info(f"Subscription payment succeeded for user {user.id}")

        elif event["type"] == "invoice.payment_failed":
            # Payment failed
            customer_id = event["data"]["object"]["customer"]

            user = db.query(User).filter(
                User.stripe_customer_id == customer_id
            ).first()

            if user:
                user.subscription_status = "past_due"
                db.commit()
                logger.warning(f"Subscription payment failed for user {user.id}")

        elif event["type"] == "customer.subscription.deleted":
            # Subscription canceled
            subscription_id = event["data"]["object"]["id"]

            user = db.query(User).filter(
                User.subscription_id == subscription_id
            ).first()

            if user:
                user.subscription_tier = SubscriptionTier.FREE
                user.subscription_status = "canceled"
                user.subscription_id = None
                db.commit()
                logger.info(f"Subscription canceled for user {user.id}")

        return {"status": "success"}

    except Exception as e:
        logger.error(f"Stripe webhook error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/verify/paystack/{reference}")
async def verify_paystack_payment(
    reference: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Verify Paystack payment after redirect"""
    payment_service = PaymentService()

    try:
        transaction_data = await payment_service.verify_paystack_transaction(reference)

        if transaction_data["status"] == "success":
            # Extract metadata
            metadata = transaction_data.get("metadata", {})
            tier = metadata.get("tier")

            if tier:
                # Update user subscription
                current_user.subscription_tier = SubscriptionTier(tier)
                current_user.subscription_status = "active"
                # Note: Paystack doesn't have subscription IDs like Stripe
                # You might store the reference or handle recurring billing differently

                db.commit()

                # Send confirmation email
                email_service = EmailService()
                pricing = payment_service.get_pricing_info(current_user.country)
                tier_pricing = next(
                    (p for p in pricing if p["tier"].value == tier), None
                )

                if tier_pricing:
                    await email_service.send_subscription_confirmation(
                        to_email=current_user.email,
                        user_name=current_user.full_name,
                        tier=tier,
                        amount=tier_pricing["price"],
                        currency=tier_pricing["currency"],
                    )

                return {
                    "status": "success",
                    "message": "Payment verified and subscription activated"
                }

        return {
            "status": "failed",
            "message": "Payment verification failed"
        }

    except Exception as e:
        logger.error(f"Paystack verification error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
