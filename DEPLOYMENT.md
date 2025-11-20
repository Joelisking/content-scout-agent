# Content Scout - Deployment Guide

This guide will help you deploy Content Scout to production on various cloud platforms.

## Prerequisites

Before deploying, you'll need:

1. **API Keys:**
   - Anthropic Claude API key (from https://console.anthropic.com)
   - SendGrid API key (from https://sendgrid.com)
   - Stripe account and API keys (from https://stripe.com)
   - Paystack account and API keys (from https://paystack.com)

2. **Accounts:**
   - Cloud hosting account (Render, Railway, AWS, GCP, etc.)
   - GitHub account (for deployment via Git)

## Option 1: Deploy to Render (Recommended)

Render offers a generous free tier and is perfect for getting started.

### 1. Prepare Your Repository

```bash
# Push to GitHub
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo-url>
git push -u origin main
```

### 2. Create PostgreSQL Database

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "PostgreSQL"
3. Name: `contentscout-db`
4. Plan: Free (or paid for production)
5. Click "Create Database"
6. Copy the **Internal Database URL** (starts with `postgresql://`)

### 3. Create Redis Instance

1. Click "New +" → "Redis"
2. Name: `contentscout-redis`
3. Plan: Free (or paid)
4. Click "Create Redis"
5. Copy the **Internal Redis URL**

### 4. Deploy Backend Service

1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name:** `contentscout-backend`
   - **Environment:** Python 3
   - **Build Command:** `pip install -r backend/requirements.txt`
   - **Start Command:** `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free (or paid)

4. Add Environment Variables:
   ```
   DATABASE_URL=<your-internal-database-url>
   REDIS_URL=<your-internal-redis-url>
   SECRET_KEY=<generate-a-random-secret-key>
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=10080
   ANTHROPIC_API_KEY=<your-claude-api-key>
   SENDGRID_API_KEY=<your-sendgrid-key>
   FROM_EMAIL=noreply@yourdomain.com
   ADMIN_EMAIL=admin@yourdomain.com
   STRIPE_SECRET_KEY=<your-stripe-secret-key>
   STRIPE_PUBLISHABLE_KEY=<your-stripe-publishable-key>
   PAYSTACK_SECRET_KEY=<your-paystack-secret-key>
   PAYSTACK_PUBLIC_KEY=<your-paystack-public-key>
   FRONTEND_URL=https://your-frontend-url.onrender.com
   ENVIRONMENT=production
   STORAGE_PATH=/opt/render/project/src/blogs
   ```

5. Click "Create Web Service"

### 5. Deploy Celery Worker

1. Click "New +" → "Background Worker"
2. Connect your repository
3. Configure:
   - **Name:** `contentscout-worker`
   - **Environment:** Python 3
   - **Build Command:** `pip install -r backend/requirements.txt`
   - **Start Command:** `cd backend && celery -A app.tasks.celery_app worker --loglevel=info`

4. Add the same environment variables as the backend

5. Click "Create Background Worker"

### 6. Deploy Frontend

1. Click "New +" → "Static Site"
2. Connect your repository
3. Configure:
   - **Name:** `contentscout-frontend`
   - **Build Command:** `cd frontend && npm install && npm run build`
   - **Publish Directory:** `frontend/dist`

4. Add Environment Variable:
   ```
   VITE_API_URL=https://your-backend-url.onrender.com/api/v1
   ```

5. Click "Create Static Site"

### 7. Update CORS Settings

Once your frontend is deployed, update the backend's `FRONTEND_URL` environment variable with your actual frontend URL.

---

## Option 2: Deploy with Docker

### Using Docker Compose (Local/VPS)

1. Copy `.env.example` to `.env` and fill in your API keys

2. Start all services:
   ```bash
   docker-compose up -d
   ```

3. Check logs:
   ```bash
   docker-compose logs -f
   ```

4. Stop services:
   ```bash
   docker-compose down
   ```

### Deploy to AWS ECS/Fargate

1. Build and push Docker images:
   ```bash
   # Login to ECR
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <your-ecr-url>

   # Build and push backend
   docker build -f Dockerfile.backend -t contentscout-backend .
   docker tag contentscout-backend:latest <your-ecr-url>/contentscout-backend:latest
   docker push <your-ecr-url>/contentscout-backend:latest

   # Build and push frontend
   docker build -f Dockerfile.frontend -t contentscout-frontend .
   docker tag contentscout-frontend:latest <your-ecr-url>/contentscout-frontend:latest
   docker push <your-ecr-url>/contentscout-frontend:latest
   ```

2. Create ECS Task Definitions for:
   - Backend API
   - Celery Worker
   - Frontend (or use S3 + CloudFront for static hosting)

3. Set up RDS PostgreSQL and ElastiCache Redis

4. Configure Application Load Balancer

---

## Option 3: Deploy to Railway

Railway is similar to Render but with different pricing.

1. Install Railway CLI:
   ```bash
   npm install -g @railway/cli
   railway login
   ```

2. Create new project:
   ```bash
   railway init
   ```

3. Add PostgreSQL:
   ```bash
   railway add --plugin postgresql
   ```

4. Add Redis:
   ```bash
   railway add --plugin redis
   ```

5. Deploy backend:
   ```bash
   railway up
   ```

6. Add environment variables via Railway dashboard

---

## Post-Deployment Checklist

### 1. Database Migrations

The app will auto-create tables on first run, but for production:

```bash
# SSH into your backend service or run locally with production DB
cd backend
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### 2. Set Up Stripe Webhooks

1. Go to Stripe Dashboard → Developers → Webhooks
2. Add endpoint: `https://your-backend-url.com/api/v1/subscriptions/webhook/stripe`
3. Select events:
   - `invoice.payment_succeeded`
   - `invoice.payment_failed`
   - `customer.subscription.deleted`
4. Copy webhook secret and add to `STRIPE_WEBHOOK_SECRET` env var

### 3. Configure SendGrid

1. Verify your sender email in SendGrid
2. Set up domain authentication (optional but recommended)
3. Create API key with "Mail Send" permissions

### 4. Test Payment Integration

1. Use Stripe test mode for initial testing
2. Test both Stripe (US/Global) and Paystack (Africa) flows
3. Verify webhook handling

### 5. Monitor Background Jobs

- Check Celery worker logs for job processing
- Set up monitoring/alerting for failed jobs
- Consider using a tool like Flower for Celery monitoring

### 6. Set Up Custom Domain (Optional)

1. Point your domain to Render/Railway nameservers
2. Add custom domain in platform dashboard
3. Update `FRONTEND_URL` environment variable

### 7. Security Checklist

- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Use production API keys (not test keys)
- [ ] Enable HTTPS (automatic on Render/Railway)
- [ ] Set up rate limiting (optional)
- [ ] Configure CORS properly
- [ ] Review database security settings

---

## Environment Variables Reference

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |
| `REDIS_URL` | Redis connection string | `redis://host:6379/0` |
| `SECRET_KEY` | JWT secret key | `your-secret-key-here` |
| `ANTHROPIC_API_KEY` | Claude API key | `sk-ant-...` |
| `SENDGRID_API_KEY` | SendGrid API key | `SG....` |
| `STRIPE_SECRET_KEY` | Stripe secret key | `sk_live_...` |
| `PAYSTACK_SECRET_KEY` | Paystack secret key | `sk_live_...` |

### Optional Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `STORAGE_PATH` | `/tmp/content-scout-blogs` | Blog file storage |
| `FRONTEND_URL` | `http://localhost:3000` | Frontend URL for CORS |
| `ENVIRONMENT` | `development` | Environment mode |

---

## Troubleshooting

### Backend won't start

- Check logs for database connection errors
- Verify all environment variables are set
- Ensure PostgreSQL is running and accessible

### Celery worker not processing jobs

- Check Redis connection
- Verify worker is running: `docker-compose ps`
- Check worker logs: `docker-compose logs celery_worker`

### Frontend can't reach backend

- Verify `VITE_API_URL` is correct
- Check CORS settings in backend
- Ensure backend is running and accessible

### Payments not working

- Verify API keys are for the correct environment (test/live)
- Check webhook endpoints are configured
- Review Stripe/Paystack dashboard for errors

---

## Scaling Considerations

### Database

- Start with managed PostgreSQL (RDS, Render PostgreSQL)
- Enable connection pooling
- Add read replicas for high traffic

### Background Jobs

- Scale Celery workers horizontally
- Consider using priority queues
- Monitor job completion times

### File Storage

- Switch to S3 for production file storage
- Enable CDN for faster blog downloads
- Implement cleanup for old files

### Monitoring

- Set up application monitoring (Sentry, DataDog)
- Monitor API response times
- Track background job success rates
- Set up alerts for errors

---

## Support

For issues or questions:
- Check the main README.md
- Review application logs
- Open an issue on GitHub

Good luck with your deployment! 🚀
