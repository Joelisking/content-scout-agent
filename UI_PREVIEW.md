# UI Preview - Fine-Tuning Features

## Create New Blog Modal

```
┌────────────────────────────────────────────────────────────┐
│  Create New Blog                                      ✕    │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Industry Sector *          │  Location *                 │
│  ┌────────────────────┐     │  ┌────────────────────┐    │
│  │ Real Estate        │     │  │ Ghana              │    │
│  └────────────────────┘     │  └────────────────────┘    │
│                                                            │
│  Custom Title (optional)                                   │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ Leave blank for AI to generate                       │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│  Target Word Count      │  Additional Keywords            │
│  ┌────────────────────┐ │  ┌────────────────────┐        │
│  │ Default (1200-1800)▼│ │  │ luxury, investment │        │
│  └────────────────────┘ │  └────────────────────┘        │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ Advanced Settings                               ▼    │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│                       [Cancel]  [Create Blog]              │
└────────────────────────────────────────────────────────────┘
```

## When Advanced Settings is Expanded

```
┌────────────────────────────────────────────────────────────┐
│  Create New Blog                                      ✕    │
├────────────────────────────────────────────────────────────┤
│  [... Basic Settings Above ...]                           │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ Advanced Settings                               ▲    │ │
│  ├──────────────────────────────────────────────────────┤ │
│  │                                                      │ │
│  │  Tone                  │  Writing Style             │ │
│  │  ┌──────────────────┐  │  ┌──────────────────┐     │ │
│  │  │ Professional    ▼│  │  │ Auto            ▼│     │ │
│  │  └──────────────────┘  │  └──────────────────┘     │ │
│  │                                                      │ │
│  │  Target Audience                                     │ │
│  │  ┌────────────────────────────────────────────────┐ │ │
│  │  │ e.g., business professionals                   │ │ │
│  │  └────────────────────────────────────────────────┘ │ │
│  │                                                      │ │
│  │  Content Depth        │  SEO Focus Level           │ │
│  │  ┌──────────────────┐ │  ┌──────────────────┐     │ │
│  │  │ Moderate        ▼│ │  │ Medium          ▼│     │ │
│  │  └──────────────────┘ │  └──────────────────┘     │ │
│  │                                                      │ │
│  │  Include Sections                                    │ │
│  │  ☑ Case Studies      ☑ Statistics                  │ │
│  │  ☑ Expert Quotes     ☑ FAQs                        │ │
│  │  ☑ Call to Action                                   │ │
│  │                                                      │ │
│  │  Custom Instructions                                 │ │
│  │  ┌────────────────────────────────────────────────┐ │ │
│  │  │ Any specific requirements or guidelines...     │ │ │
│  │  │                                                │ │ │
│  │  │                                                │ │ │
│  │  └────────────────────────────────────────────────┘ │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│                       [Cancel]  [Create Blog]              │
└────────────────────────────────────────────────────────────┘
```

## Color Scheme

- Background: Dark theme (`bg-dark-900`)
- Inputs: `bg-dark-800` with `border-dark-700`
- Advanced Section: `bg-dark-800/30` with rounded borders
- Primary Button: Gradient primary
- Hover states: Smooth transitions

## Interactive Elements

1. **Advanced Settings Toggle**
   - Click to expand/collapse
   - ChevronDown ▼ when collapsed
   - ChevronUp ▲ when expanded
   - Smooth height transition

2. **Dropdowns**
   - Target Word Count: 5 options
   - Tone: 3 options
   - Writing Style: 6 options (including Auto)
   - Content Depth: 3 options
   - SEO Focus: 3 options

3. **Checkboxes**
   - Independent selection
   - Can select multiple sections
   - Primary color when checked

4. **Text Areas**
   - Custom Title: Single line
   - Additional Keywords: Single line
   - Target Audience: Single line
   - Custom Instructions: Multi-line (3 rows)

## Responsive Design

- **Desktop (md+)**: 2-column grid for paired inputs
- **Mobile**: Single column stack
- Modal max-width: 2xl
- Centered with backdrop blur
