# Content Scout

AI-powered research and blog generation platform for businesses.

## Features

- 🔍 **Smart Research**: Automatically researches trending topics in any sector and location
- ✍️ **AI Blog Generation**: Creates high-quality, SEO-optimized blog posts using Claude AI
- 📧 **Email Notifications**: Get notified when your content is ready
- 💳 **Smart Payments**: Stripe (global) and Paystack (Africa) integration
- 📊 **Multi-tier Plans**: Free, Starter, and Pro subscription tiers
- 🎨 **Modern UI**: Beautiful dark-themed dashboard
- 📥 **Export Options**: Download blogs as Markdown or PDF

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Database
- **Celery + Redis** - Background job processing
- **SQLAlchemy** - ORM
- **Claude API** - AI blog generation
- **SendGrid** - Email delivery
- **Stripe & Paystack** - Payment processing

### Frontend
- **React + TypeScript** - UI framework
- **Tailwind CSS** - Styling
- **Vite** - Build tool
- **React Query** - Data fetching

## Project Structure

```
content-scout-agent/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Config, security, deps
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── tasks/          # Celery tasks
│   ├── alembic/            # Database migrations
│   ├── requirements.txt
│   └── main.py
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API client
│   │   └── types/         # TypeScript types
│   ├── package.json
│   └── vite.config.ts
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
└── README.md
```

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Claude API key (from Anthropic)
- SendGrid API key
- Stripe account (+ Paystack for Africa)

### Environment Setup

1. Clone the repository
```bash
git clone <repo-url>
cd content-scout-agent
```

2. Create environment file:
```bash
cp backend/.env.example backend/.env
```

3. Configure environment variables in `backend/.env`:
```env
# Database
DATABASE_URL=postgresql://postgres:postgres@db:5432/contentscout

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Claude AI
ANTHROPIC_API_KEY=your-claude-api-key

# Email
SENDGRID_API_KEY=your-sendgrid-key
FROM_EMAIL=noreply@contentscout.com

# Payments
STRIPE_SECRET_KEY=your-stripe-secret-key
STRIPE_PUBLISHABLE_KEY=your-stripe-publishable-key
PAYSTACK_SECRET_KEY=your-paystack-secret-key
PAYSTACK_PUBLIC_KEY=your-paystack-public-key

# Redis
REDIS_URL=redis://redis:6379/0
```

### Run with Docker

```bash
# Build and start all services
docker-compose up --build

# Backend will be available at: http://localhost:8000
# Frontend will be available at: http://localhost:3000
# API docs at: http://localhost:8000/docs
```

## Subscription Tiers

| Feature | Free | Starter ($29/mo) | Pro ($99/mo) |
|---------|------|------------------|--------------|
| Blogs per month | 3 | 20 | Unlimited |
| Research depth | Basic | Standard | Deep |
| Export formats | Markdown | Markdown, PDF | Markdown, PDF, HTML |
| Email support | - | ✓ | Priority ✓ |
| Custom branding | - | - | ✓ |

## Deployment

### Deploy to Render

1. Create new Web Service for backend
2. Create new Static Site for frontend
3. Add PostgreSQL database
4. Add Redis instance
5. Configure environment variables

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed instructions.

### Deploy to Railway/AWS/GCP

Docker configuration works with any container platform.

## API Documentation

Once running, visit `http://localhost:8000/docs` for interactive API documentation.

## Development

### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

### Run Celery Worker
```bash
cd backend
celery -A app.tasks.celery_app worker --loglevel=info
```

## Contributing

Contributions welcome! Please read CONTRIBUTING.md first.

## License

MIT License - see LICENSE file for details
