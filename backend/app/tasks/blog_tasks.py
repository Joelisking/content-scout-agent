from celery import Task
from app.tasks.celery_app import celery_app
from app.core.database import SessionLocal
from app.models import ResearchJob, Blog, User, JobStatus
from app.services.research_service import ResearchService
from app.services.blog_generation_service import BlogGenerationService
from app.services.storage_service import StorageService
from app.services.email_service import EmailService
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DatabaseTask(Task):
    """Base task that provides database session"""
    _db = None

    @property
    def db(self):
        if self._db is None:
            self._db = SessionLocal()
        return self._db

    def after_return(self, *args, **kwargs):
        if self._db is not None:
            self._db.close()
            self._db = None


@celery_app.task(bind=True, base=DatabaseTask, name="generate_blog_task")
def generate_blog_task(self, job_id: int):
    """
    Celery task to generate a blog post

    This task:
    1. Conducts research on the sector/location
    2. Generates blog content using Claude AI
    3. Saves the blog as Markdown and PDF
    4. Sends email notification to user
    """
    db = self.db
    research_service = ResearchService()
    blog_service = BlogGenerationService()
    storage_service = StorageService()
    email_service = EmailService()

    try:
        # Get research job
        job = db.query(ResearchJob).filter(ResearchJob.id == job_id).first()
        if not job:
            logger.error(f"Research job {job_id} not found")
            return

        # Get user
        user = db.query(User).filter(User.id == job.user_id).first()
        if not user:
            logger.error(f"User {job.user_id} not found")
            return

        # Update job status to RESEARCHING
        job.status = JobStatus.RESEARCHING
        job.started_at = datetime.utcnow()
        db.commit()

        logger.info(f"Starting research for job {job_id}: {job.sector} in {job.location}")

        # Conduct research
        research_data = research_service.research_sector(
            sector=job.sector,
            location=job.location,
            additional_keywords=job.additional_keywords,
        )

        # Since research_sector is async, we need to run it synchronously
        import asyncio
        research_data = asyncio.run(research_data)

        # Store research data
        job.research_data = research_data
        job.keywords_found = research_data.get("keywords", [])
        db.commit()

        logger.info(f"Research completed. Found {len(job.keywords_found)} keywords")

        # Update job status to GENERATING
        job.status = JobStatus.GENERATING
        db.commit()

        logger.info(f"Generating blog content for job {job_id}")

        # Generate blog outline
        outline = research_service.generate_blog_outline(
            research_data, job.keywords_found
        )

        # Generate blog content using Claude
        blog_data = asyncio.run(
            blog_service.generate_blog(
                sector=job.sector,
                location=job.location,
                research_data=research_data,
                keywords=job.keywords_found,
                tone=job.tone,
                outline=outline,
            )
        )

        logger.info(f"Blog generated: {blog_data['title']}")

        # Save blog to database
        blog = Blog(
            user_id=user.id,
            research_job_id=job.id,
            title=blog_data["title"],
            content=blog_data["content"],
            summary=blog_data.get("summary"),
            keywords=", ".join(job.keywords_found[:10]),
            word_count=blog_data.get("word_count"),
            reading_time_minutes=blog_data.get("reading_time_minutes"),
        )
        db.add(blog)
        db.commit()
        db.refresh(blog)

        logger.info(f"Blog saved to database with ID {blog.id}")

        # Save files
        markdown_path = asyncio.run(
            storage_service.save_markdown(
                user_id=user.id,
                blog_id=blog.id,
                title=blog.title,
                content=blog.content,
            )
        )

        pdf_path = asyncio.run(
            storage_service.save_pdf(
                user_id=user.id,
                blog_id=blog.id,
                title=blog.title,
                content=blog.content,
                summary=blog.summary,
            )
        )

        # Update blog with file paths
        blog.markdown_file_path = markdown_path
        blog.pdf_file_path = pdf_path

        # Update user's blog count
        user.blogs_created_this_month += 1

        # Update job status to COMPLETED
        job.status = JobStatus.COMPLETED
        job.completed_at = datetime.utcnow()

        db.commit()

        logger.info(f"Blog generation completed for job {job_id}")

        # Send email notification
        asyncio.run(
            email_service.send_blog_ready_notification(
                to_email=user.email,
                user_name=user.full_name,
                blog_title=blog.title,
                blog_id=blog.id,
                sector=job.sector,
                location=job.location,
            )
        )

        logger.info(f"Email notification sent to {user.email}")

        return {
            "status": "success",
            "blog_id": blog.id,
            "job_id": job.id,
        }

    except Exception as e:
        logger.error(f"Error generating blog for job {job_id}: {str(e)}")

        # Update job with error
        job = db.query(ResearchJob).filter(ResearchJob.id == job_id).first()
        if job:
            job.status = JobStatus.FAILED
            job.error_message = str(e)
            job.completed_at = datetime.utcnow()
            db.commit()

            # Get user and send failure notification
            user = db.query(User).filter(User.id == job.user_id).first()
            if user:
                import asyncio
                asyncio.run(
                    email_service.send_job_failed_notification(
                        to_email=user.email,
                        user_name=user.full_name,
                        sector=job.sector,
                        location=job.location,
                        error_message=str(e),
                    )
                )

        raise


@celery_app.task(name="reset_monthly_blog_counts")
def reset_monthly_blog_counts():
    """
    Celery periodic task to reset monthly blog counts
    Should be scheduled to run on the 1st of each month
    """
    db = SessionLocal()
    try:
        db.query(User).update({"blogs_created_this_month": 0})
        db.commit()
        logger.info("Monthly blog counts reset successfully")
    except Exception as e:
        logger.error(f"Failed to reset monthly blog counts: {str(e)}")
        db.rollback()
    finally:
        db.close()
