from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models import User, ResearchJob, JobStatus
from app.schemas import ResearchJobCreate, ResearchJobResponse, ResearchJobListResponse
from app.tasks.blog_tasks import generate_blog_task
from typing import Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/jobs", tags=["Research Jobs"])


@router.post("", response_model=ResearchJobResponse, status_code=status.HTTP_201_CREATED)
async def create_research_job(
    job_data: ResearchJobCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new research job and start blog generation"""
    # Check if user can create more blogs
    if not current_user.can_create_blog():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Monthly blog limit reached. You have used {current_user.blogs_created_this_month} of {current_user.get_blog_limit()} blogs this month. Please upgrade your plan."
        )

    # Create research job
    job = ResearchJob(
        user_id=current_user.id,
        sector=job_data.sector,
        location=job_data.location,
        additional_keywords=job_data.additional_keywords,
        tone=job_data.tone,
        status=JobStatus.PENDING,
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    logger.info(f"Created research job {job.id} for user {current_user.id}")

    # Start background task
    task = generate_blog_task.delay(job.id)
    job.celery_task_id = task.id
    db.commit()

    logger.info(f"Started Celery task {task.id} for job {job.id}")

    return ResearchJobResponse.from_orm(job)


@router.get("", response_model=ResearchJobListResponse)
async def list_research_jobs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    status: Optional[JobStatus] = None,
):
    """List all research jobs for the current user"""
    query = db.query(ResearchJob).filter(ResearchJob.user_id == current_user.id)

    if status:
        query = query.filter(ResearchJob.status == status)

    total = query.count()

    jobs = (
        query.order_by(ResearchJob.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return ResearchJobListResponse(
        jobs=[ResearchJobResponse.from_orm(job) for job in jobs],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{job_id}", response_model=ResearchJobResponse)
async def get_research_job(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a specific research job"""
    job = (
        db.query(ResearchJob)
        .filter(ResearchJob.id == job_id, ResearchJob.user_id == current_user.id)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Research job not found"
        )

    return ResearchJobResponse.from_orm(job)


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_research_job(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a research job"""
    job = (
        db.query(ResearchJob)
        .filter(ResearchJob.id == job_id, ResearchJob.user_id == current_user.id)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Research job not found"
        )

    # Only allow deletion of completed or failed jobs
    if job.status in [JobStatus.PENDING, JobStatus.RESEARCHING, JobStatus.GENERATING]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete a job that is in progress"
        )

    db.delete(job)
    db.commit()

    logger.info(f"Deleted research job {job_id}")

    return None
