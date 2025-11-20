# Content Scout - Quick Start Guide

Get Content Scout running locally in 10 minutes!

## Prerequisites

- Docker & Docker Compose installed
- Claude API key from Anthropic
- SendGrid API key (free tier available)
- Stripe test account (optional, for payments)
- Paystack test account (optional, for payments)

## Step 1: Clone and Setup

```bash
cd content-scout-agent
```

## Step 2: Configure Environment

Create your environment file:

```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env` and add your API keys:

```env
# Minimum required configuration
DATABASE_URL=postgresql://postgres:postgres@db:5432/contentscout
REDIS_URL=redis://redis:6379/0
SECRET_KEY=your-secret-key-change-this
ANTHROPIC_API_KEY=sk-ant-your-claude-api-key-here
SENDGRID_API_KEY=SG.your-sendgrid-key-here
FROM_EMAIL=noreply@contentscout.com
ADMIN_EMAIL=admin@contentscout.com

# Payment keys (use test keys for development)
STRIPE_SECRET_KEY=sk_test_your_stripe_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_key
PAYSTACK_SECRET_KEY=sk_test_your_paystack_key
PAYSTACK_PUBLIC_KEY=pk_test_your_paystack_key

FRONTEND_URL=http://localhost:3000
ENVIRONMENT=development
STORAGE_PATH=/tmp/content-scout-blogs
```

## Step 3: Start Services

```bash
docker-compose up --build
```

This will start:
- PostgreSQL database (port 5432)
- Redis (port 6379)
- Backend API (port 8000)
- Celery worker (background jobs)
- Frontend (port 3000)

## Step 4: Access the Application

Open your browser:

- **Frontend:** http://localhost:3000
- **API Docs:** http://localhost:8000/docs
- **API:** http://localhost:8000

## Step 5: Create an Account

1. Go to http://localhost:3000
2. Click "Get Started" or "Sign Up"
3. Fill in your details:
   - Email
   - Password (min 8 characters)
   - Full name
   - Company name (optional)
   - Country (determines payment provider)
4. Click "Create Account"

You'll be automatically logged in and redirected to the dashboard!

## Step 6: Create Your First Blog

1. Click "Create New Blog" on the dashboard
2. Fill in the form:
   - **Sector:** e.g., "Real Estate"
   - **Location:** e.g., "Ghana" or "Lagos, Nigeria"
   - **Keywords:** e.g., "luxury homes, investment" (optional)
   - **Tone:** Professional, Casual, or Technical
3. Click "Create Blog"

The AI will:
1. Research trending topics in your sector and location
2. Generate a comprehensive blog post
3. Save it as Markdown and PDF
4. Send you an email when it's ready (3-5 minutes)

## Step 7: View and Download Your Blog

1. Go to "Blogs" in the navigation
2. Click on your generated blog
3. Read the content
4. Download as Markdown or PDF

## Development Workflow

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f celery_worker
docker-compose logs -f frontend
```

### Stop Services

```bash
docker-compose down
```

### Rebuild After Changes

```bash
docker-compose up --build
```

### Access Database

```bash
docker-compose exec db psql -U postgres -d contentscout
```

### Access Redis CLI

```bash
docker-compose exec redis redis-cli
```

## API Testing

Access the interactive API documentation:

```
http://localhost:8000/docs
```

Test endpoints:
1. Click "Authorize" button
2. Register a user via `/api/v1/auth/register`
3. Copy the `access_token` from response
4. Paste token in Authorization dialog
5. Test any endpoint!

## Frontend Development

To work on the frontend without Docker:

```bash
cd frontend
npm install
npm run dev
```

The frontend will run on http://localhost:3000

## Backend Development

To work on the backend without Docker:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Start Celery worker separately:

```bash
celery -A app.tasks.celery_app worker --loglevel=info
```

## Common Issues

### Port Already in Use

If you get port conflicts:

```bash
# Stop all containers
docker-compose down

# Edit docker-compose.yml to change ports
# Then restart
docker-compose up
```

### Database Connection Error

```bash
# Reset the database
docker-compose down -v
docker-compose up --build
```

### Celery Worker Not Processing Jobs

Check logs:

```bash
docker-compose logs celery_worker
```

Verify Redis is running:

```bash
docker-compose ps redis
```

### Email Not Sending

- Verify your SendGrid API key is correct
- Check SendGrid dashboard for errors
- Look at backend logs for email errors

## Next Steps

1. **Explore the Dashboard**
   - View your usage stats
   - Check your subscription tier
   - See recent jobs

2. **Try Different Configurations**
   - Different sectors (Healthcare, SaaS, E-commerce)
   - Different locations
   - Different tones

3. **Test Payments**
   - Go to Settings
   - Try upgrading to Starter or Pro
   - Use Stripe test cards: `4242 4242 4242 4242`

4. **Customize**
   - Modify the frontend theme
   - Adjust blog generation prompts
   - Add custom features

## Subscription Tiers

| Tier | Blogs/Month | Price |
|------|-------------|-------|
| Free | 3 | $0 |
| Starter | 20 | $29 |
| Pro | Unlimited | $99 |

Free tier is automatically activated on signup!

## Getting API Keys

### Claude (Anthropic)

1. Go to https://console.anthropic.com
2. Sign up for an account
3. Go to API Keys
4. Create new key
5. Copy and paste into `.env`

### SendGrid

1. Go to https://sendgrid.com
2. Sign up (free tier available)
3. Go to Settings → API Keys
4. Create API Key with "Mail Send" permission
5. Copy and paste into `.env`

### Stripe (Testing)

1. Go to https://stripe.com
2. Sign up for account
3. Use test mode keys from Dashboard
4. No credit card needed for testing!

### Paystack (Testing)

1. Go to https://paystack.com
2. Sign up (primarily for African countries)
3. Use test mode keys
4. Free for testing!

## Support

Need help? Check:
- README.md for full documentation
- DEPLOYMENT.md for production deployment
- API docs at http://localhost:8000/docs
- Backend logs for errors

Happy blogging! ✨
