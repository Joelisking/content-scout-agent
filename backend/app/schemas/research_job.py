from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.research_job import JobStatus


class ResearchJobCreate(BaseModel):
    sector: str = Field(..., min_length=2, max_length=100, description="Industry sector (e.g., Real Estate, Healthcare)")
    location: str = Field(..., min_length=2, max_length=100, description="Target location (e.g., Ghana, Lagos)")
    additional_keywords: Optional[str] = Field(None, description="Optional comma-separated keywords")
    tone: str = Field(default="professional", description="Blog tone: professional, casual, or technical")


class ResearchJobResponse(BaseModel):
    id: int
    user_id: int
    sector: str
    location: str
    additional_keywords: Optional[str]
    tone: str
    status: JobStatus
    error_message: Optional[str]
    research_data: Optional[Dict[str, Any]]
    keywords_found: Optional[List[str]]
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    celery_task_id: Optional[str]

    class Config:
        from_attributes = True


class ResearchJobListResponse(BaseModel):
    jobs: List[ResearchJobResponse]
    total: int
    page: int
    page_size: int
