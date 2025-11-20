from anthropic import Anthropic
from typing import Dict, Any, List
from app.core.config import settings
import re


class BlogGenerationService:
    """Service for generating blog content using Claude AI"""

    def __init__(self):
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = "claude-3-5-sonnet-20241022"

    async def generate_blog(
        self,
        sector: str,
        location: str,
        research_data: Dict[str, Any],
        keywords: List[str],
        tone: str = "professional",
        outline: Dict[str, Any] = None,
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

        Returns:
            Dictionary containing title, content, and summary
        """
        # Build the prompt for Claude
        prompt = self._build_blog_prompt(
            sector, location, research_data, keywords, tone, outline
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
    ) -> str:
        """Build the prompt for Claude to generate the blog"""

        trending_topics = research_data.get("trending_topics", [])
        trending_topics_text = "\n".join(
            [f"- {topic.get('title', '')}" for topic in trending_topics]
        )

        keywords_text = ", ".join(keywords[:10])

        prompt = f"""You are a professional content writer specializing in {sector}. Write a comprehensive, engaging, and SEO-optimized blog post about {sector} in {location}.

**Research Findings:**
{trending_topics_text}

**Target Keywords to Include Naturally:**
{keywords_text}

**Writing Style:**
- Tone: {tone}
- Length: 1200-1800 words
- Include relevant statistics and insights
- Make it engaging and actionable
- Use proper headings (H1, H2, H3)
- Include an introduction and conclusion

**Format Requirements:**
Please structure your response EXACTLY as follows:

TITLE: [Your compelling blog title here]

SUMMARY: [A 2-3 sentence summary of the blog post]

CONTENT:
[The full blog post in Markdown format with proper headings, paragraphs, and formatting]

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
