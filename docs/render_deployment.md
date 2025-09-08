# Render Deployment Guide

## Overview

This guide covers deploying the EEG Mental Health Assistant on Render using free APIs and services.

## Prerequisites

- Render account (free tier available)
- GitHub repository with your code
- Free API keys from Cohere, Groq, and/or Gemini
- Optional: Google Maps API key, SendGrid, Twilio accounts

## Free API Setup

### 1. Cohere API (Free Tier: 100 requests/month)

```bash
# Sign up at https://cohere.ai/
# Get your API key from the dashboard
# Free tier includes 100 requests per month
```

### 2. Groq API (Free Tier: 14,400 requests/day)

```bash
# Sign up at https://console.groq.com/
# Get your API key
# Free tier includes 14,400 requests per day with Llama models
```

### 3. Google Gemini API (Free Tier: 60 requests/minute)

```bash
# Sign up at https://makersuite.google.com/
# Get your API key
# Free tier includes 60 requests per minute
```

## Render Deployment

### 1. Database Setup

Create a PostgreSQL database on Render:

1. Go to Render Dashboard
2. Click "New" → "PostgreSQL"
3. Choose the free plan
4. Name: `eeg-health-db`
5. Database Name: `eeg_mental_health`
6. User: `eeg_user`

### 2. Redis Setup

Create a Redis instance on Render:

1. Click "New" → "Redis"
2. Choose the free plan
3. Name: `eeg-health-redis`
4. Set maxmemory-policy to `allkeys-lru`

### 3. Web Service Deployment

Deploy the main API service:

1. Click "New" → "Web Service"
2. Connect your GitHub repository
3. Configure the service:

```bash
Name: eeg-health-api
Environment: Python 3
Build Command: pip install -r backend/requirements.txt
Start Command: cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### 4. Environment Variables

Set these environment variables in your Render service:

**Required:**
```bash
ENVIRONMENT=production
SECRET_KEY=<generate-secure-key>
DATABASE_URL=<from-your-postgres-service>
REDIS_URL=<from-your-redis-service>
```

**AI APIs (at least one required):**
```bash
COHERE_API_KEY=<your-cohere-key>
GROQ_API_KEY=<your-groq-key>
GEMINI_API_KEY=<your-gemini-key>
```

**Optional Services:**
```bash
GOOGLE_MAPS_API_KEY=<google-maps-key>
SENDGRID_API_KEY=<sendgrid-key>
TWILIO_ACCOUNT_SID=<twilio-sid>
TWILIO_AUTH_TOKEN=<twilio-token>
FCM_SERVER_KEY=<fcm-key>
SENTRY_DSN=<sentry-dsn>
```

### 5. Background Worker Service

Deploy the Celery worker:

1. Click "New" → "Background Worker"
2. Connect the same repository
3. Configure:

```bash
Name: eeg-health-worker
Environment: Python 3
Build Command: pip install -r backend/requirements.txt
Start Command: cd backend && celery -A app.tasks.celery_tasks worker --loglevel=info --concurrency=2
```

Use the same environment variables as the web service.

### 6. Database Migration

After deployment, run the migration:

```bash
# Connect to your web service shell and run:
python scripts/migrate.py
```

## Using render.yaml (Alternative)

You can also use the `render.yaml` file for infrastructure as code:

1. Place `render.yaml` in your repository root
2. Connect your repository to Render
3. Render will automatically create all services

## Free Tier Limitations

### Render Free Tier:
- Web services: 750 hours/month
- Background workers: 750 hours/month  
- PostgreSQL: 1GB storage, 97 hours/month
- Redis: 25MB storage

### API Limitations:
- **Cohere**: 100 requests/month
- **Groq**: 14,400 requests/day
- **Gemini**: 60 requests/minute, 1,500 requests/day

## Monitoring and Maintenance

### Health Checks

Render automatically monitors your service health via the `/health` endpoint.

### Logs

View logs in the Render dashboard:
1. Go to your service
2. Click "Logs" tab
3. Monitor for errors and performance

### Database Backups

Render automatically backs up PostgreSQL databases on the free tier.

### Scaling

To scale beyond free tier:
1. Upgrade to paid plans for more resources
2. Add multiple worker instances
3. Use larger database plans

## Troubleshooting

### Common Issues

**Service Won't Start:**
- Check build logs for dependency issues
- Verify environment variables are set
- Ensure database connection string is correct

**API Rate Limits:**
- Monitor usage in API dashboards
- Implement request caching
- Use multiple API keys if needed

**Database Connection Issues:**
- Verify DATABASE_URL format
- Check database service status
- Ensure migrations have run

**Worker Not Processing Jobs:**
- Check Redis connection
- Verify REDIS_URL format
- Monitor worker logs for errors

## Performance Optimization

### Caching Strategy
- Use Redis for frequently accessed data
- Cache API responses when possible
- Implement request deduplication

### Database Optimization
- Add indexes for common queries
- Use connection pooling
- Monitor query performance

### API Usage Optimization
- Batch requests when possible
- Implement exponential backoff
- Use the most efficient API for each task

## Security Considerations

### Environment Variables
- Never commit API keys to version control
- Use Render's environment variable encryption
- Rotate keys regularly

### Database Security
- Use strong passwords
- Enable SSL connections
- Implement row-level security

### API Security
- Implement rate limiting
- Validate all inputs
- Use HTTPS for all communications

## Cost Management

### Free Tier Monitoring
- Track service hours usage
- Monitor database storage
- Watch API request counts

### Optimization Tips
- Use efficient algorithms
- Minimize database queries
- Cache expensive operations
- Use background workers for heavy tasks

## Support and Resources

### Render Support
- Documentation: https://render.com/docs
- Community: https://community.render.com
- Status: https://status.render.com

### API Documentation
- Cohere: https://docs.cohere.ai
- Groq: https://console.groq.com/docs
- Gemini: https://ai.google.dev/docs

### Monitoring Tools
- Render Dashboard for service metrics
- Database performance monitoring
- API usage tracking in provider dashboards