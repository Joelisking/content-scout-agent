from anthropic import Anthropic
from typing import Dict, Any, List
from app.core.config import settings
import re


class BlogGenerationService:
    """Service for generating blog content using Claude AI"""

    def __init__(self):
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = settings.AI_MODEL or "claude-3-5-sonnet-20241022"

    async def generate_blog(
        self,
        sector: str,
        location: str,
        research_data: Dict[str, Any],
        keywords: List[str],
        tone: str = "professional",
        outline: Dict[str, Any] = None,
        custom_title: str = None,
        target_word_count: str = None,
        writing_style: str = None,
        target_audience: str = None,
        content_depth: str = "moderate",
        seo_focus: str = "medium",
        include_sections: List[str] = None,
        custom_instructions: str = None,
    ) -> Dict[str, str]:
        """
        Generate a comprehensive blog post using Claude AI

        Args:
            sector: Industry sector
            location: Target location
            research_data: Research findings
            keywords: Target keywords to include
            tone: Writing tone (professional, casual, technical)
            outline: Optional blog outline
            custom_title: Optional custom title
            target_word_count: Target word count range
            writing_style: Writing style preference
            target_audience: Target audience description
            content_depth: Content depth level
            seo_focus: SEO optimization level
            include_sections: List of sections to include
            custom_instructions: Custom generation instructions

        Returns:
            Dictionary containing title, content, and summary
        """
        # Build the prompt for Claude
        prompt = self._build_blog_prompt(
            sector=sector,
            location=location,
            research_data=research_data,
            keywords=keywords,
            tone=tone,
            outline=outline,
            custom_title=custom_title,
            target_word_count=target_word_count,
            writing_style=writing_style,
            target_audience=target_audience,
            content_depth=content_depth,
            seo_focus=seo_focus,
            include_sections=include_sections,
            custom_instructions=custom_instructions,
        )

        # Generate blog using Claude
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                temperature=0.7,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Extract the blog content
            blog_content = message.content[0].text

            # Parse the response to extract title, content, and summary
            parsed_blog = self._parse_blog_response(blog_content)

            return parsed_blog

        except Exception as e:
            raise Exception(f"Failed to generate blog: {str(e)}")

    def _build_blog_prompt(
        self,
        sector: str,
        location: str,
        research_data: Dict[str, Any],
        keywords: List[str],
        tone: str,
        outline: Dict[str, Any] = None,
        custom_title: str = None,
        target_word_count: str = None,
        writing_style: str = None,
        target_audience: str = None,
        content_depth: str = "moderate",
        seo_focus: str = "medium",
        include_sections: List[str] = None,
        custom_instructions: str = None,
    ) -> str:
        """Build the prompt for Claude to generate the blog"""

        trending_topics = research_data.get("trending_topics", [])
        trending_topics_text = "\n".join(
            [f"- {topic.get('title', '')}" for topic in trending_topics]
        )

        keywords_text = ", ".join(keywords[:10])

        # Determine word count target
        word_count = target_word_count or "1200-1800"

        # Build the prompt
        prompt = f"""You are a professional content writer specializing in {sector}. Write a comprehensive, engaging, and SEO-optimized blog post about {sector} in {location}.

**Research Findings:**
{trending_topics_text}

**Target Keywords to Include Naturally:**
{keywords_text}

**Writing Style:**
- Tone: {tone}"""

        if writing_style:
            style_descriptions = {
                "informative": "educational and fact-based, focusing on providing clear information",
                "storytelling": "narrative-driven with anecdotes and real-world examples",
                "how-to": "step-by-step instructional format with actionable guidance",
                "listicle": "list-based format with clear, numbered or bulleted points",
                "opinion": "thought-leadership style with strong perspectives and insights"
            }
            prompt += f"\n- Style: {writing_style} ({style_descriptions.get(writing_style, 'engaging and well-structured')})"

        prompt += f"\n- Length: {word_count} words"

        if target_audience:
            prompt += f"\n- Target Audience: {target_audience}"

        # Content depth guidance
        depth_descriptions = {
            "overview": "Provide a high-level overview focusing on key points and main concepts",
            "moderate": "Include relevant statistics and insights with balanced detail",
            "comprehensive": "Provide in-depth analysis with extensive data, examples, and thorough coverage of subtopics"
        }
        prompt += f"\n- Content Depth: {depth_descriptions.get(content_depth, depth_descriptions['moderate'])}"

        # SEO focus guidance
        seo_descriptions = {
            "low": "Focus on natural, reader-friendly content with minimal SEO optimization",
            "medium": "Balance SEO optimization with readability, using keywords naturally",
            "high": "Heavily optimize for SEO with strategic keyword placement, meta-friendly structure, and search intent focus"
        }
        prompt += f"\n- SEO Focus: {seo_descriptions.get(seo_focus, seo_descriptions['medium'])}"

        prompt += "\n- Make it engaging and actionable\n- Use proper headings (H1, H2, H3)\n- Include an introduction and conclusion"

        # Include sections if specified
        if include_sections and len(include_sections) > 0:
            prompt += "\n\n**Required Sections to Include:**"
            section_map = {
                "case_studies": "Real-world case studies or examples",
                "statistics": "Relevant statistics and data points",
                "expert_quotes": "Expert quotes or industry insights",
                "faqs": "Frequently Asked Questions section",
                "call_to_action": "Strong call-to-action conclusion"
            }
            for section in include_sections:
                section_desc = section_map.get(section, section.replace("_", " ").title())
                prompt += f"\n- {section_desc}"

        # Custom instructions
        if custom_instructions:
            prompt += f"\n\n**Additional Instructions:**\n{custom_instructions}"

        # Format requirements
        if custom_title:
            prompt += f"""

**Format Requirements:**
Please structure your response EXACTLY as follows:

TITLE: {custom_title}

SUMMARY: [A 2-3 sentence summary of the blog post]

CONTENT:
[The full blog post in Markdown format with proper headings, paragraphs, and formatting]"""
        else:
            prompt += """

**Format Requirements:**
Please structure your response EXACTLY as follows:

TITLE: [Your compelling blog title here]

SUMMARY: [A 2-3 sentence summary of the blog post]

CONTENT:
[The full blog post in Markdown format with proper headings, paragraphs, and formatting]"""

        # Additional guidelines
        prompt += f"""

**Additional Guidelines:**
1. Start with a hook that grabs attention
2. Use data and examples specific to {location}
3. Include practical insights and actionable takeaways
4. Ensure the content is original and valuable
5. Optimize for readability with short paragraphs
6. Include relevant subheadings
7. End with a strong conclusion

Write the blog post now:"""

        return prompt

    def _parse_blog_response(self, response: str) -> Dict[str, str]:
        """Parse Claude's response to extract title, summary, and content"""

        # Extract title
        title_match = re.search(r"TITLE:\s*(.+?)(?:\n|$)", response, re.IGNORECASE)
        title = title_match.group(1).strip() if title_match else "Untitled Blog Post"

        # Extract summary
        summary_match = re.search(
            r"SUMMARY:\s*(.+?)(?=\n\nCONTENT:|\nCONTENT:)",
            response,
            re.IGNORECASE | re.DOTALL
        )
        summary = summary_match.group(1).strip() if summary_match else ""

        # Extract content
        content_match = re.search(
            r"CONTENT:\s*(.+)", response, re.IGNORECASE | re.DOTALL
        )
        content = content_match.group(1).strip() if content_match else response

        # Clean up the content
        content = content.strip()

        # Calculate word count
        word_count = len(content.split())

        # Estimate reading time (average 200 words per minute)
        reading_time = max(1, round(word_count / 200))

        return {
            "title": title,
            "summary": summary,
            "content": content,
            "word_count": word_count,
            "reading_time_minutes": reading_time,
        }

    async def enhance_blog(
        self, original_content: str, enhancement_type: str = "seo"
    ) -> str:
        """
        Enhance an existing blog post

        Args:
            original_content: The original blog content
            enhancement_type: Type of enhancement (seo, readability, tone)

        Returns:
            Enhanced blog content
        """
        enhancement_prompts = {
            "seo": "Enhance this blog post for better SEO. Add relevant keywords naturally, improve meta descriptions, and optimize headings.",
            "readability": "Improve the readability of this blog post. Make it more engaging, break up long paragraphs, and add transitions.",
            "tone": "Adjust the tone of this blog post to be more professional and authoritative while maintaining engagement.",
        }

        prompt = f"""{enhancement_prompts.get(enhancement_type, enhancement_prompts['seo'])}

Original Content:
{original_content}

Provide the enhanced version:"""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )

            return message.content[0].text

        except Exception as e:
            raise Exception(f"Failed to enhance blog: {str(e)}")
