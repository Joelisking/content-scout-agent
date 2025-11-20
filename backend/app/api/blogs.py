from fastapi import APIRouter, Depends, HTTPException, status, Query, Response
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models import User, Blog
from app.schemas import BlogResponse, BlogListResponse, BlogSummary
from app.services.storage_service import StorageService
from typing import Optional
import logging
import os

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/blogs", tags=["Blogs"])


@router.get("", response_model=BlogListResponse)
async def list_blogs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
):
    """List all blogs for the current user"""
    query = db.query(Blog).filter(Blog.user_id == current_user.id)

    total = query.count()

    blogs = (
        query.order_by(Blog.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return BlogListResponse(
        blogs=[BlogResponse.from_orm(blog) for blog in blogs],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{blog_id}", response_model=BlogResponse)
async def get_blog(
    blog_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a specific blog"""
    blog = (
        db.query(Blog)
        .filter(Blog.id == blog_id, Blog.user_id == current_user.id)
        .first()
    )

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found"
        )

    return BlogResponse.from_orm(blog)


@router.get("/{blog_id}/download/markdown")
async def download_markdown(
    blog_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Download blog as Markdown file"""
    blog = (
        db.query(Blog)
        .filter(Blog.id == blog_id, Blog.user_id == current_user.id)
        .first()
    )

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found"
        )

    if not blog.markdown_file_path or not os.path.exists(blog.markdown_file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Markdown file not found"
        )

    from slugify import slugify
    filename = f"{slugify(blog.title)}.md"

    return FileResponse(
        path=blog.markdown_file_path,
        media_type="text/markdown",
        filename=filename,
    )


@router.get("/{blog_id}/download/pdf")
async def download_pdf(
    blog_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Download blog as PDF file"""
    blog = (
        db.query(Blog)
        .filter(Blog.id == blog_id, Blog.user_id == current_user.id)
        .first()
    )

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found"
        )

    if not blog.pdf_file_path or not os.path.exists(blog.pdf_file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="PDF file not found"
        )

    from slugify import slugify
    filename = f"{slugify(blog.title)}.pdf"

    return FileResponse(
        path=blog.pdf_file_path,
        media_type="application/pdf",
        filename=filename,
    )


@router.delete("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(
    blog_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a blog"""
    blog = (
        db.query(Blog)
        .filter(Blog.id == blog_id, Blog.user_id == current_user.id)
        .first()
    )

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found"
        )

    # Delete files
    storage_service = StorageService()
    await storage_service.delete_blog_files(
        blog.markdown_file_path,
        blog.pdf_file_path
    )

    # Delete from database
    db.delete(blog)
    db.commit()

    logger.info(f"Deleted blog {blog_id}")

    return None


@router.get("/stats/summary")
async def get_blog_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get blog statistics for the current user"""
    total_blogs = db.query(Blog).filter(Blog.user_id == current_user.id).count()

    total_words = db.query(Blog).filter(Blog.user_id == current_user.id).with_entities(
        Blog.word_count
    ).all()
    total_word_count = sum([w[0] for w in total_words if w[0]])

    return {
        "total_blogs": total_blogs,
        "total_word_count": total_word_count,
        "blogs_this_month": current_user.blogs_created_this_month,
        "blog_limit": current_user.get_blog_limit(),
        "remaining_blogs": max(0, current_user.get_blog_limit() - current_user.blogs_created_this_month) if current_user.get_blog_limit() > 0 else -1,
    }
