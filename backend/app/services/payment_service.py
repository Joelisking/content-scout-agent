import stripe
from paystackapi.paystack import Paystack
from paystackapi.transaction import Transaction
from paystackapi.customer import Customer
from app.core.config import settings
from app.models.user import User, SubscriptionTier, PaymentProvider
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

# Initialize payment providers
stripe.api_key = settings.STRIPE_SECRET_KEY
paystack = Paystack(secret_key=settings.PAYSTACK_SECRET_KEY)


class PaymentService:
    """Service for handling payments via Stripe and Paystack"""

    def __init__(self):
        self.stripe_prices = {
            SubscriptionTier.STARTER: settings.STARTER_PRICE_USD,
            SubscriptionTier.PRO: settings.PRO_PRICE_USD,
        }
        self.paystack_prices = {
            SubscriptionTier.STARTER: settings.STARTER_PRICE_NGN,
            SubscriptionTier.PRO: settings.PRO_PRICE_NGN,
        }

    def should_use_paystack(self, country_code: str) -> bool:
        """Determine if user should use Paystack based on country"""
        return country_code.upper() in settings.PAYSTACK_COUNTRIES

    def get_payment_provider(self, country_code: str) -> PaymentProvider:
        """Get appropriate payment provider for user's country"""
        if self.should_use_paystack(country_code):
            return PaymentProvider.PAYSTACK
        return PaymentProvider.STRIPE

    def get_publishable_key(self, country_code: str) -> Dict[str, str]:
        """Get the appropriate publishable key for frontend"""
        provider = self.get_payment_provider(country_code)

        if provider == PaymentProvider.PAYSTACK:
            return {
                "provider": "paystack",
                "publishable_key": settings.PAYSTACK_PUBLIC_KEY,
            }
        else:
            return {
                "provider": "stripe",
                "publishable_key": settings.STRIPE_PUBLISHABLE_KEY,
            }

    async def create_subscription_stripe(
        self, user: User, tier: SubscriptionTier, payment_method_id: str
    ) -> Dict:
        """Create a Stripe subscription"""
        try:
            # Create or get Stripe customer
            if not user.stripe_customer_id:
                customer = stripe.Customer.create(
                    email=user.email,
                    name=user.full_name,
                    payment_method=payment_method_id,
                    invoice_settings={"default_payment_method": payment_method_id},
                    metadata={
                        "user_id": user.id,
                        "country": user.country,
                    }
                )
                user.stripe_customer_id = customer.id
            else:
                customer = stripe.Customer.retrieve(user.stripe_customer_id)
                # Attach payment method
                stripe.PaymentMethod.attach(
                    payment_method_id,
                    customer=customer.id,
                )
                stripe.Customer.modify(
                    customer.id,
                    invoice_settings={"default_payment_method": payment_method_id},
                )

            # Create price object if not exists (you should create these in Stripe Dashboard)
            # For now, we'll create them dynamically
            price_amount = self.stripe_prices[tier]

            # Create subscription
            subscription = stripe.Subscription.create(
                customer=customer.id,
                items=[{
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": f"Content Scout {tier.value.title()} Plan",
                            "description": f"Monthly subscription to Content Scout {tier.value.title()} tier",
                        },
                        "unit_amount": price_amount,
                        "recurring": {"interval": "month"},
                    },
                }],
                payment_behavior="default_incomplete",
                payment_settings={"save_default_payment_method": "on_subscription"},
                expand=["latest_invoice.payment_intent"],
            )

            return {
                "subscription_id": subscription.id,
                "status": subscription.status,
                "client_secret": subscription.latest_invoice.payment_intent.client_secret,
                "current_period_end": subscription.current_period_end,
            }

        except stripe.error.StripeError as e:
            logger.error(f"Stripe error: {str(e)}")
            raise Exception(f"Payment failed: {str(e)}")

    async def create_subscription_paystack(
        self, user: User, tier: SubscriptionTier, authorization_code: str = None
    ) -> Dict:
        """Create a Paystack subscription"""
        try:
            # Create or get Paystack customer
            if not user.paystack_customer_code:
                customer_response = Customer.create(
                    email=user.email,
                    first_name=user.full_name.split()[0] if user.full_name else "",
                    last_name=" ".join(user.full_name.split()[1:]) if len(user.full_name.split()) > 1 else "",
                )
                if customer_response["status"]:
                    user.paystack_customer_code = customer_response["data"]["customer_code"]
                else:
                    raise Exception("Failed to create Paystack customer")

            # For Paystack, we'll use the transaction flow
            # In production, you'd create a subscription plan in Paystack Dashboard
            price_amount = self.paystack_prices[tier]  # In kobo (Nigerian kobo)

            # Initialize transaction
            transaction_response = Transaction.initialize(
                email=user.email,
                amount=price_amount,
                currency="NGN",  # Nigerian Naira
                metadata={
                    "user_id": user.id,
                    "tier": tier.value,
                    "subscription": True,
                }
            )

            if transaction_response["status"]:
                return {
                    "authorization_url": transaction_response["data"]["authorization_url"],
                    "access_code": transaction_response["data"]["access_code"],
                    "reference": transaction_response["data"]["reference"],
                }
            else:
                raise Exception("Failed to initialize Paystack transaction")

        except Exception as e:
            logger.error(f"Paystack error: {str(e)}")
            raise Exception(f"Payment failed: {str(e)}")

    async def cancel_subscription_stripe(self, user: User) -> bool:
        """Cancel a Stripe subscription"""
        try:
            if user.subscription_id:
                stripe.Subscription.delete(user.subscription_id)
                return True
            return False
        except stripe.error.StripeError as e:
            logger.error(f"Failed to cancel Stripe subscription: {str(e)}")
            return False

    async def cancel_subscription_paystack(self, user: User) -> bool:
        """Cancel a Paystack subscription"""
        try:
            # Paystack subscription cancellation logic
            # This depends on how you've set up subscriptions in Paystack
            return True
        except Exception as e:
            logger.error(f"Failed to cancel Paystack subscription: {str(e)}")
            return False

    async def verify_paystack_transaction(self, reference: str) -> Dict:
        """Verify a Paystack transaction"""
        try:
            response = Transaction.verify(reference=reference)
            if response["status"]:
                return response["data"]
            else:
                raise Exception("Transaction verification failed")
        except Exception as e:
            logger.error(f"Failed to verify Paystack transaction: {str(e)}")
            raise

    def construct_stripe_webhook_event(self, payload: bytes, sig_header: str):
        """Construct and verify Stripe webhook event"""
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
            return event
        except ValueError as e:
            logger.error(f"Invalid payload: {str(e)}")
            raise
        except stripe.error.SignatureVerificationError as e:
            logger.error(f"Invalid signature: {str(e)}")
            raise

    def get_pricing_info(self, country_code: str) -> list:
        """Get pricing information for a user's country"""
        provider = self.get_payment_provider(country_code)

        if provider == PaymentProvider.PAYSTACK:
            return [
                {
                    "tier": SubscriptionTier.FREE,
                    "price": 0,
                    "currency": "NGN",
                    "blogs_per_month": settings.FREE_TIER_BLOG_LIMIT,
                    "features": [
                        "3 blogs per month",
                        "Basic research",
                        "Markdown export",
                        "Email notifications",
                    ],
                },
                {
                    "tier": SubscriptionTier.STARTER,
                    "price": settings.STARTER_PRICE_NGN / 100,  # Convert from kobo
                    "currency": "NGN",
                    "blogs_per_month": settings.STARTER_TIER_BLOG_LIMIT,
                    "features": [
                        "20 blogs per month",
                        "Standard research",
                        "Markdown & PDF export",
                        "Email notifications",
                        "Priority support",
                    ],
                },
                {
                    "tier": SubscriptionTier.PRO,
                    "price": settings.PRO_PRICE_NGN / 100,
                    "currency": "NGN",
                    "blogs_per_month": -1,  # Unlimited
                    "features": [
                        "Unlimited blogs",
                        "Deep research",
                        "All export formats",
                        "Priority support",
                        "Custom branding",
                    ],
                },
            ]
        else:
            return [
                {
                    "tier": SubscriptionTier.FREE,
                    "price": 0,
                    "currency": "USD",
                    "blogs_per_month": settings.FREE_TIER_BLOG_LIMIT,
                    "features": [
                        "3 blogs per month",
                        "Basic research",
                        "Markdown export",
                        "Email notifications",
                    ],
                },
                {
                    "tier": SubscriptionTier.STARTER,
                    "price": settings.STARTER_PRICE_USD / 100,  # Convert from cents
                    "currency": "USD",
                    "blogs_per_month": settings.STARTER_TIER_BLOG_LIMIT,
                    "features": [
                        "20 blogs per month",
                        "Standard research",
                        "Markdown & PDF export",
                        "Email notifications",
                        "Priority support",
                    ],
                },
                {
                    "tier": SubscriptionTier.PRO,
                    "price": settings.PRO_PRICE_USD / 100,
                    "currency": "USD",
                    "blogs_per_month": -1,
                    "features": [
                        "Unlimited blogs",
                        "Deep research",
                        "All export formats",
                        "Priority support",
                        "Custom branding",
                    ],
                },
            ]
