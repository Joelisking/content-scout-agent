-- Migration: Add fine-tuning fields to research_jobs table
-- Date: 2024-12-10
-- Description: Adds optional fields for blog customization (custom title, word count, writing style, etc.)

-- Add basic configuration fields
ALTER TABLE research_jobs ADD COLUMN IF NOT EXISTS custom_title VARCHAR;
ALTER TABLE research_jobs ADD COLUMN IF NOT EXISTS target_word_count VARCHAR;

-- Add advanced configuration fields
ALTER TABLE research_jobs ADD COLUMN IF NOT EXISTS writing_style VARCHAR;
ALTER TABLE research_jobs ADD COLUMN IF NOT EXISTS target_audience VARCHAR;
ALTER TABLE research_jobs ADD COLUMN IF NOT EXISTS content_depth VARCHAR DEFAULT 'moderate';
ALTER TABLE research_jobs ADD COLUMN IF NOT EXISTS seo_focus VARCHAR DEFAULT 'medium';
ALTER TABLE research_jobs ADD COLUMN IF NOT EXISTS include_sections JSON;
ALTER TABLE research_jobs ADD COLUMN IF NOT EXISTS custom_instructions TEXT;

-- Add comments for documentation
COMMENT ON COLUMN research_jobs.custom_title IS 'Optional custom blog title (AI generates if not provided)';
COMMENT ON COLUMN research_jobs.target_word_count IS 'Target word count range (e.g., "1200-1800", "2500-3000")';
COMMENT ON COLUMN research_jobs.writing_style IS 'Writing style: informative, storytelling, how-to, listicle, opinion';
COMMENT ON COLUMN research_jobs.target_audience IS 'Target audience description (e.g., "business professionals")';
COMMENT ON COLUMN research_jobs.content_depth IS 'Content depth: overview, moderate, comprehensive';
COMMENT ON COLUMN research_jobs.seo_focus IS 'SEO optimization level: low, medium, high';
COMMENT ON COLUMN research_jobs.include_sections IS 'JSON array of sections to include (e.g., ["case_studies", "faqs"])';
COMMENT ON COLUMN research_jobs.custom_instructions IS 'Free-text custom instructions for blog generation';
