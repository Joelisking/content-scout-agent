import os
from pathlib import Path
from typing import Optional
import markdown2
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from app.core.config import settings
from slugify import slugify
import logging

logger = logging.getLogger(__name__)


class StorageService:
    """Service for storing and managing blog files"""

    def __init__(self):
        self.storage_path = Path(settings.STORAGE_PATH)
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def _get_user_directory(self, user_id: int) -> Path:
        """Get or create user's storage directory"""
        user_dir = self.storage_path / f"user_{user_id}"
        user_dir.mkdir(parents=True, exist_ok=True)
        return user_dir

    def _generate_filename(self, title: str, blog_id: int, extension: str) -> str:
        """Generate a clean filename from blog title"""
        slug = slugify(title)[:50]  # Limit length
        return f"{blog_id}_{slug}.{extension}"

    async def save_markdown(
        self, user_id: int, blog_id: int, title: str, content: str
    ) -> str:
        """Save blog content as Markdown file"""
        try:
            user_dir = self._get_user_directory(user_id)
            filename = self._generate_filename(title, blog_id, "md")
            file_path = user_dir / filename

            # Add title to markdown content
            full_content = f"# {title}\n\n{content}"

            # Write to file
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(full_content)

            logger.info(f"Saved Markdown file: {file_path}")
            return str(file_path)

        except Exception as e:
            logger.error(f"Failed to save Markdown file: {str(e)}")
            raise

    async def save_pdf(
        self,
        user_id: int,
        blog_id: int,
        title: str,
        content: str,
        summary: Optional[str] = None,
    ) -> str:
        """Save blog content as PDF file"""
        try:
            user_dir = self._get_user_directory(user_id)
            filename = self._generate_filename(title, blog_id, "pdf")
            file_path = user_dir / filename

            # Create PDF
            doc = SimpleDocTemplate(
                str(file_path),
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18,
            )

            # Container for the 'Flowable' objects
            elements = []

            # Define styles
            styles = getSampleStyleSheet()
            styles.add(ParagraphStyle(
                name='Justify',
                alignment=TA_JUSTIFY,
                fontSize=11,
                leading=14,
            ))
            styles.add(ParagraphStyle(
                name='BlogTitle',
                parent=styles['Heading1'],
                fontSize=24,
                alignment=TA_CENTER,
                spaceAfter=30,
            ))
            styles.add(ParagraphStyle(
                name='Summary',
                fontSize=12,
                alignment=TA_JUSTIFY,
                textColor='#666666',
                italic=True,
                spaceAfter=20,
            ))

            # Add title
            elements.append(Paragraph(title, styles['BlogTitle']))
            elements.append(Spacer(1, 12))

            # Add summary if provided
            if summary:
                elements.append(Paragraph(f"<i>{summary}</i>", styles['Summary']))
                elements.append(Spacer(1, 12))

            # Convert Markdown to HTML
            html_content = markdown2.markdown(
                content,
                extras=["fenced-code-blocks", "tables", "header-ids"]
            )

            # Clean up HTML for PDF (remove some markdown artifacts)
            # Split by paragraphs and add to PDF
            paragraphs = html_content.split('\n\n')

            for para in paragraphs:
                if para.strip():
                    # Handle headings
                    if para.startswith('<h2>'):
                        clean_para = para.replace('<h2>', '').replace('</h2>', '')
                        elements.append(Spacer(1, 12))
                        elements.append(Paragraph(clean_para, styles['Heading2']))
                        elements.append(Spacer(1, 6))
                    elif para.startswith('<h3>'):
                        clean_para = para.replace('<h3>', '').replace('</h3>', '')
                        elements.append(Spacer(1, 12))
                        elements.append(Paragraph(clean_para, styles['Heading3']))
                        elements.append(Spacer(1, 6))
                    else:
                        # Regular paragraph
                        elements.append(Paragraph(para, styles['Justify']))
                        elements.append(Spacer(1, 12))

            # Build PDF
            doc.build(elements)

            logger.info(f"Saved PDF file: {file_path}")
            return str(file_path)

        except Exception as e:
            logger.error(f"Failed to save PDF file: {str(e)}")
            raise

    async def get_file_content(self, file_path: str) -> bytes:
        """Read and return file content"""
        try:
            with open(file_path, "rb") as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to read file {file_path}: {str(e)}")
            raise

    async def delete_blog_files(
        self, markdown_path: Optional[str], pdf_path: Optional[str]
    ) -> bool:
        """Delete blog files"""
        try:
            if markdown_path and os.path.exists(markdown_path):
                os.remove(markdown_path)

            if pdf_path and os.path.exists(pdf_path):
                os.remove(pdf_path)

            return True

        except Exception as e:
            logger.error(f"Failed to delete files: {str(e)}")
            return False

    def get_file_size(self, file_path: str) -> int:
        """Get file size in bytes"""
        try:
            return os.path.getsize(file_path)
        except Exception:
            return 0
