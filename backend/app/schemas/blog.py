from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.blog import BlogFormat


class BlogResponse(BaseModel):
    id: int
    user_id: int
    research_job_id: int
    title: str
    content: str
    summary: Optional[str]
    keywords: Optional[str]
    word_count: Optional[int]
    reading_time_minutes: Optional[int]
    markdown_file_path: Optional[str]
    pdf_file_path: Optional[str]
    html_file_path: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class BlogListResponse(BaseModel):
    blogs: List[BlogResponse]
    total: int
    page: int
    page_size: int


class BlogSummary(BaseModel):
    id: int
    title: str
    summary: Optional[str]
    keywords: Optional[str]
    word_count: Optional[int]
    reading_time_minutes: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True
