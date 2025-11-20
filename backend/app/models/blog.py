from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class BlogFormat(str, enum.Enum):
    MARKDOWN = "markdown"
    PDF = "pdf"
    HTML = "html"


class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    research_job_id = Column(Integer, ForeignKey("research_jobs.id"), nullable=False)

    # Blog content
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)  # Markdown format
    summary = Column(Text, nullable=True)  # Short summary/excerpt
    keywords = Column(String, nullable=True)  # Comma-separated keywords

    # Metadata
    word_count = Column(Integer, nullable=True)
    reading_time_minutes = Column(Integer, nullable=True)

    # File storage
    markdown_file_path = Column(String, nullable=True)
    pdf_file_path = Column(String, nullable=True)
    html_file_path = Column(String, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="blogs")
    research_job = relationship("ResearchJob", back_populates="blog")
