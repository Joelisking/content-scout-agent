import resend
from app.core.config import settings
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending email notifications"""

    def __init__(self):
        resend.api_key = settings.RESEND_API_KEY
        self.from_email = settings.FROM_EMAIL

    async def send_welcome_email(self, to_email: str, user_name: str):
        """Send welcome email to new user"""
        subject = "Welcome to Content Scout!"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .button {{ display: inline-block; padding: 12px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚀 Welcome to Content Scout!</h1>
                </div>
                <div class="content">
                    <h2>Hi {user_name}!</h2>
                    <p>Thank you for joining Content Scout, your AI-powered research and content generation platform.</p>

                    <p><strong>What you can do with Content Scout:</strong></p>
                    <ul>
                        <li>🔍 Research trending topics in any industry</li>
                        <li>✍️ Generate high-quality blog posts with AI</li>
                        <li>📊 Discover popular keywords and insights</li>
                        <li>📧 Get notified when your content is ready</li>
                    </ul>

                    <p>You're currently on the <strong>Free Plan</strong> which includes 3 blog posts per month.</p>

                    <p>Ready to create your first blog?</p>
                    <a href="{settings.FRONTEND_URL}/dashboard" class="button">Go to Dashboard</a>

                    <p>If you have any questions, feel free to reach out to us!</p>

                    <p>Best regards,<br>The Content Scout Team</p>
                </div>
                <div class="footer">
                    <p>© 2024 Content Scout. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """

        await self._send_email(to_email, subject, html_content)

    async def send_blog_ready_notification(
        self,
        to_email: str,
        user_name: str,
        blog_title: str,
        blog_id: int,
        sector: str,
        location: str,
    ):
        """Notify user when their blog is ready"""
        subject = f"Your blog '{blog_title}' is ready!"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .blog-info {{ background: white; padding: 20px; border-left: 4px solid #667eea; margin: 20px 0; }}
                .button {{ display: inline-block; padding: 12px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>✅ Your Blog is Ready!</h1>
                </div>
                <div class="content">
                    <h2>Hi {user_name}!</h2>
                    <p>Great news! Your AI-generated blog post is ready to view and download.</p>

                    <div class="blog-info">
                        <h3>📝 {blog_title}</h3>
                        <p><strong>Sector:</strong> {sector}</p>
                        <p><strong>Location:</strong> {location}</p>
                    </div>

                    <p>Your blog has been researched, written, and optimized with the latest trending topics and keywords.</p>

                    <a href="{settings.FRONTEND_URL}/blogs/{blog_id}" class="button">View Your Blog</a>

                    <p><strong>Available formats:</strong></p>
                    <ul>
                        <li>📄 Markdown (for easy editing)</li>
                        <li>📑 PDF (for sharing)</li>
                    </ul>

                    <p>Happy publishing!</p>

                    <p>Best regards,<br>The Content Scout Team</p>
                </div>
                <div class="footer">
                    <p>© 2024 Content Scout. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """

        await self._send_email(to_email, subject, html_content)

    async def send_job_failed_notification(
        self,
        to_email: str,
        user_name: str,
        sector: str,
        location: str,
        error_message: str,
    ):
        """Notify user when blog generation fails"""
        subject = "Blog Generation Failed"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #dc3545; color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .error-box {{ background: #ffe6e6; border-left: 4px solid #dc3545; padding: 15px; margin: 20px 0; }}
                .button {{ display: inline-block; padding: 12px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>❌ Blog Generation Failed</h1>
                </div>
                <div class="content">
                    <h2>Hi {user_name},</h2>
                    <p>We encountered an issue while generating your blog post.</p>

                    <p><strong>Job Details:</strong></p>
                    <ul>
                        <li>Sector: {sector}</li>
                        <li>Location: {location}</li>
                    </ul>

                    <div class="error-box">
                        <strong>Error:</strong> {error_message}
                    </div>

                    <p>Don't worry - this blog generation won't count against your monthly limit. Please try again or contact our support team if the issue persists.</p>

                    <a href="{settings.FRONTEND_URL}/dashboard" class="button">Try Again</a>

                    <p>We apologize for the inconvenience.</p>

                    <p>Best regards,<br>The Content Scout Team</p>
                </div>
                <div class="footer">
                    <p>© 2024 Content Scout. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """

        await self._send_email(to_email, subject, html_content)

    async def send_subscription_confirmation(
        self,
        to_email: str,
        user_name: str,
        tier: str,
        amount: float,
        currency: str,
    ):
        """Send subscription confirmation email"""
        subject = f"Subscription Confirmed - {tier.title()} Plan"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .subscription-box {{ background: white; padding: 20px; border-left: 4px solid #10b981; margin: 20px 0; }}
                .button {{ display: inline-block; padding: 12px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎉 Subscription Confirmed!</h1>
                </div>
                <div class="content">
                    <h2>Hi {user_name}!</h2>
                    <p>Thank you for upgrading to the <strong>{tier.title()} Plan</strong>!</p>

                    <div class="subscription-box">
                        <h3>Subscription Details</h3>
                        <p><strong>Plan:</strong> {tier.title()}</p>
                        <p><strong>Amount:</strong> {currency} {amount:.2f}/month</p>
                    </div>

                    <p>You now have access to premium features and increased blog generation limits!</p>

                    <a href="{settings.FRONTEND_URL}/dashboard" class="button">Start Creating</a>

                    <p>Thank you for your business!</p>

                    <p>Best regards,<br>The Content Scout Team</p>
                </div>
                <div class="footer">
                    <p>© 2024 Content Scout. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """

        await self._send_email(to_email, subject, html_content)

    async def _send_email(
        self, to_email: str, subject: str, html_content: str
    ) -> bool:
        """Internal method to send email via Resend"""
        try:
            params: resend.Emails.SendParams = {
                "from": self.from_email,
                "to": [to_email],
                "subject": subject,
                "html": html_content,
            }

            response = resend.Emails.send(params)
            email_id = getattr(response, 'id', 'success')
            logger.info(f"Email sent to {to_email}: {email_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False
