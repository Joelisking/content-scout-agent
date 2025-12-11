from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class JobStatus(str, enum.Enum):
    PENDING = "pending"
    RESEARCHING = "researching"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"


class ResearchJob(Base):
    __tablename__ = "research_jobs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Basic configuration
    sector = Column(String, nullable=False)  # e.g., "Real Estate"
    location = Column(String, nullable=False)  # e.g., "Ghana", "Lagos, Nigeria"
    custom_title = Column(String, nullable=True)  # Optional custom title
    target_word_count = Column(String, nullable=True)  # e.g., "1200-1800", "2500-3000"
    additional_keywords = Column(Text, nullable=True)  # Optional comma-separated keywords

    # Advanced configuration
    tone = Column(String, default="professional")  # professional, casual, technical
    writing_style = Column(String, nullable=True)  # informative, storytelling, how-to, listicle, opinion
    target_audience = Column(String, nullable=True)  # e.g., "business professionals", "general consumers"
    content_depth = Column(String, default="moderate")  # overview, moderate, comprehensive
    seo_focus = Column(String, default="medium")  # low, medium, high
    include_sections = Column(JSON, nullable=True)  # List of sections to include
    custom_instructions = Column(Text, nullable=True)  # Free-text custom requirements

    # Job status
    status = Column(Enum(JobStatus), default=JobStatus.PENDING, nullable=False)
    error_message = Column(Text, nullable=True)

    # Research results
    research_data = Column(JSON, nullable=True)  # Store trending keywords, topics, etc.
    keywords_found = Column(JSON, nullable=True)  # List of trending keywords

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Celery task ID for tracking
    celery_task_id = Column(String, nullable=True)

    # Relationships
    user = relationship("User", back_populates="research_jobs")
    blog = relationship("Blog", back_populates="research_job", uselist=False)
