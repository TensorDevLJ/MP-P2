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


# Check all services are healthy
docker-compose -f docker-compose.prod.yml ps
```

### 4. Production Configuration

**Database Backup:**
```bash
# Automated daily backups
docker-compose -f docker-compose.prod.yml exec postgres pg_dump -U eeg_user eeg_mental_health > backup_$(date +%Y%m%d).sql
```

**Log Rotation:**
```bash
# Setup logrotate for container logs
sudo tee /etc/logrotate.d/docker-eeg << EOF
/var/lib/docker/containers/*/*-json.log {
    rotate 7
    daily
    compress
    missingok
    copytruncate
}
EOF
```

## Cloud Deployment Options

### AWS ECS Deployment

```bash
# Build and push to ECR
aws ecr create-repository --repository-name eeg-mental-health-api
docker build -t eeg-mental-health-api backend/
docker tag eeg-mental-health-api:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/eeg-mental-health-api:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/eeg-mental-health-api:latest
```

### Heroku Deployment

```bash
# Install Heroku CLI
heroku create eeg-mental-health-api

# Set config vars
heroku config:set SECRET_KEY=<secret-key>
heroku config:set DATABASE_URL=<postgres-url>

# Deploy
git subtree push --prefix backend heroku main
```

### DigitalOcean App Platform

Create `app.yaml`:
```yaml
name: eeg-mental-health-assistant
services:
- name: api
  source_dir: /backend
  github:
    repo: your-username/eeg-mental-health-assistant
    branch: main
  run_command: gunicorn app.main:app -w 2 -k uvicorn.workers.UvicornWorker
  environment_slug: python
  instance_count: 2
  instance_size_slug: basic-xxs
  envs:
  - key: ENVIRONMENT
    value: production
  - key: SECRET_KEY
    value: <secret-key>
    type: SECRET
```

## Monitoring and Maintenance

### Application Monitoring

**Prometheus Metrics:**
- Request latency and throughput
- Error rates by endpoint
- Database connection pool usage
- Celery task queue length
- ML model inference times

**Grafana Dashboards:**
- System overview
- API performance
- ML pipeline metrics
- User activity patterns

### Health Checks

```bash
# API health
curl http://localhost:8000/health

# Database connectivity
docker-compose exec postgres pg_isready -U eeg_user

# Redis connectivity  
docker-compose exec redis redis-cli ping

# Worker status
docker-compose exec celery-worker celery -A app.tasks.celery_tasks status
```

### Log Management

**Centralized Logging:**
```bash
# View all logs
docker-compose logs -f

# Specific service logs
docker-compose logs -f api
docker-compose logs -f celery-worker

# Export logs
docker-compose logs api > api_logs_$(date +%Y%m%d).txt
```

### Backup Strategy

**Database Backups:**
```bash
# Create backup
docker-compose exec postgres pg_dump -U eeg_user -Fc eeg_mental_health > backup_$(date +%Y%m%d).dump

# Restore backup
docker-compose exec postgres pg_restore -U eeg_user -d eeg_mental_health backup_20250101.dump
```

**File Storage Backups:**
- EEG files: Automatically replicated in S3
- ML models: Version controlled and backed up
- User uploads: Retention policy based on user consent

## Security Considerations

### Network Security
- All traffic encrypted with TLS 1.3
- Firewall rules limiting database access
- VPN access for administrative functions

### Application Security
- JWT tokens with short expiration (30 minutes)
- Rate limiting on all endpoints
- Input validation and sanitization
- SQL injection protection via ORM

### Data Protection
- Encryption at rest (AES-256)
- Personal data anonymization options
- GDPR compliance features
- Regular security audits

### Compliance
- HIPAA technical safeguards implementation
- SOC 2 Type II compliance preparation
- Data processing agreements
- Incident response procedures

## Scaling Considerations

### Horizontal Scaling
```bash
# Scale API workers
docker-compose -f docker-compose.prod.yml up -d --scale api=3

# Scale Celery workers
docker-compose -f docker-compose.prod.yml up -d --scale celery-worker=4
```

### Performance Optimization
- Database connection pooling
- Redis caching for frequent queries
- CDN for static assets
- ML model optimization (quantization, pruning)

### Load Testing
```bash
# Install load testing tools
pip install locust

# Run load tests
locust -f scripts/load_test.py --host=http://localhost:8000
```

## Troubleshooting

### Common Issues

**Database Connection Errors:**
```bash
# Check PostgreSQL status
docker-compose logs postgres

# Reset database
docker-compose down -v
docker-compose up -d postgres
```

**Celery Worker Issues:**
```bash
# Restart workers
docker-compose restart celery-worker

# Clear Redis queue
docker-compose exec redis redis-cli FLUSHALL
```

**High Memory Usage:**
```bash
# Monitor resource usage
docker stats

# Adjust worker concurrency
export CELERY_CONCURRENCY=2
docker-compose up -d celery-worker
```

### Log Analysis

**Error Patterns:**
```bash
# Find authentication errors
docker-compose logs api | grep "401\|403"

# Find slow requests
docker-compose logs api | grep "slow_request"

# Database connection issues
docker-compose logs postgres | grep "ERROR"
```

## Support and Updates

### Updating the System
```bash
# Pull latest changes
git pull origin main

# Rebuild containers
docker-compose build

# Apply updates
docker-compose up -d

# Run any new migrations
docker-compose exec api python scripts/migrate.py
```

### Getting Help
- Check logs first: `docker-compose logs -f`
- Review health endpoints: `/health`
- Monitor metrics in Grafana
- Check GitHub issues for known problems

For production support:
- Set up monitoring alerts
- Implement automated failover
- Maintain incident response runbooks
- Regular backup verification