# Fine-Tuning Features Test Guide

## ✅ Migration Completed Successfully

All database columns have been added:
- ✅ custom_title
- ✅ target_word_count
- ✅ writing_style
- ✅ target_audience
- ✅ content_depth (default: 'moderate')
- ✅ seo_focus (default: 'medium')
- ✅ include_sections (JSON)
- ✅ custom_instructions

Backend has been restarted and is running successfully.

## Testing the New Features

### 1. Frontend Testing

**Access the Dashboard:**
```
http://localhost:3000/dashboard
```

**Click "Create New Blog" and you should see:**

**Basic Settings (Always visible):**
- Industry Sector * (required)
- Location * (required)
- Custom Title (optional)
- Target Word Count (optional) - Dropdown with 5 options
- Additional Keywords (optional)

**Advanced Settings (Click to expand):**
- Tone - Dropdown (Professional, Casual, Technical)
- Writing Style - Dropdown (Auto, Informative, Storytelling, How-To, Listicle, Opinion)
- Target Audience - Text input
- Content Depth - Dropdown (Overview, Moderate, Comprehensive)
- SEO Focus Level - Dropdown (Low, Medium, High)
- Include Sections - 5 checkboxes
- Custom Instructions - Text area

### 2. API Testing

**Test with minimal input (backward compatible):**
```bash
curl -X POST http://localhost:8000/api/v1/jobs \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "sector": "Technology",
    "location": "San Francisco"
  }'
```

**Test with full customization:**
```bash
curl -X POST http://localhost:8000/api/v1/jobs \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "sector": "Real Estate",
    "location": "Ghana",
    "custom_title": "The Future of Sustainable Housing in Ghana",
    "target_word_count": "2500-3000",
    "additional_keywords": "eco-friendly, green building",
    "tone": "professional",
    "writing_style": "how-to",
    "target_audience": "property developers",
    "content_depth": "comprehensive",
    "seo_focus": "high",
    "include_sections": ["case_studies", "statistics", "faqs"],
    "custom_instructions": "Focus on practical implementation challenges"
  }'
```

### 3. Expected Behavior

**When creating a blog:**
1. Form should have collapsible "Advanced Settings" section
2. Advanced settings should expand/collapse smoothly
3. All fields should be optional except Sector and Location
4. Checkboxes should work independently
5. Form should reset after successful creation

**In the generated blog:**
1. Custom title should be used if provided
2. Word count should match the selected range
3. Writing style should be evident in the content structure
4. Tone should match the selected option
5. Selected sections should appear in the content
6. Custom instructions should be reflected in the content

### 4. Database Verification

**Check a created job:**
```bash
docker-compose exec db psql -U postgres -d contentscout -c "SELECT id, sector, custom_title, target_word_count, writing_style, content_depth, seo_focus FROM research_jobs ORDER BY id DESC LIMIT 1;"
```

## Troubleshooting

### Frontend not showing new fields?
```bash
cd frontend
npm run dev
# Hard refresh browser (Cmd+Shift+R or Ctrl+Shift+F5)
```

### Backend errors?
```bash
docker-compose logs backend --tail 50
```

### Database issues?
```bash
# Check columns exist
docker-compose exec db psql -U postgres -d contentscout -c "\d research_jobs"
```

## Next Steps

1. ✅ Test basic blog creation (sector + location only)
2. ✅ Test with custom title
3. ✅ Test different word count options
4. ✅ Test advanced settings
5. ✅ Verify the generated blog respects all settings
6. 🎉 Enjoy your fine-tuned blog generation!

## Notes

- All new fields are **optional** and backward compatible
- Default values ensure existing functionality works unchanged
- Advanced settings are hidden by default for a clean UX
- The AI prompt builder intelligently uses all provided settings
