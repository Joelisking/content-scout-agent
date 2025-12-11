from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.research_job import JobStatus


class ResearchJobCreate(BaseModel):
    # Basic settings
    sector: str = Field(..., min_length=2, max_length=100, description="Industry sector (e.g., Real Estate, Healthcare)")
    location: str = Field(..., min_length=2, max_length=100, description="Target location (e.g., Ghana, Lagos)")
    custom_title: Optional[str] = Field(None, max_length=200, description="Custom blog title (optional, AI will generate if not provided)")
    target_word_count: Optional[str] = Field(None, description="Target word count range (e.g., '1200-1800', '2500-3000')")
    additional_keywords: Optional[str] = Field(None, description="Optional comma-separated keywords")

    # Advanced settings
    tone: str = Field(default="professional", description="Blog tone: professional, casual, or technical")
    writing_style: Optional[str] = Field(None, description="Writing style: informative, storytelling, how-to, listicle, or opinion")
    target_audience: Optional[str] = Field(None, max_length=200, description="Target audience (e.g., 'business professionals', 'general consumers')")
    content_depth: str = Field(default="moderate", description="Content depth: overview, moderate, or comprehensive")
    seo_focus: str = Field(default="medium", description="SEO optimization level: low, medium, or high")
    include_sections: Optional[List[str]] = Field(None, description="Sections to include (e.g., ['case_studies', 'statistics', 'faqs'])")
    custom_instructions: Optional[str] = Field(None, description="Free-text custom instructions for blog generation")


class ResearchJobResponse(BaseModel):
    id: int
    user_id: int
    sector: str
    location: str
    custom_title: Optional[str]
    target_word_count: Optional[str]
    additional_keywords: Optional[str]
    tone: str
    writing_style: Optional[str]
    target_audience: Optional[str]
    content_depth: str
    seo_focus: str
    include_sections: Optional[List[str]]
    custom_instructions: Optional[str]
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
