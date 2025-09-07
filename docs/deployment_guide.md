# Deployment Guide

## Overview

This guide covers deploying the EEG Mental Health Assistant in development, staging, and production environments.

## Prerequisites

- Docker and Docker Compose
- Domain name with SSL certificates (production)
- Cloud storage for EEG files (AWS S3 recommended)
- External service API keys (optional but recommended)

## Environment Setup

### 1. Clone and Setup

```bash
git clone <repository-url>
cd eeg-mental-health-assistant
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### 2. Environment Variables

Copy and customize the environment file:

```bash
cp .env.example deployment/.env
```

**Required Variables:**
```bash
# Database
POSTGRES_DB=eeg_mental_health
POSTGRES_USER=eeg_user  
POSTGRES_PASSWORD=<secure-password>

# Redis
REDIS_PASSWORD=<redis-password>

# Application
SECRET_KEY=<32-byte-secret-key>
ENVIRONMENT=production

# Database URL (adjust for your setup)
DATABASE_URL=postgresql://eeg_user:password@postgres:5432/eeg_mental_health
REDIS_URL=redis://:password@redis:6379/0
```

**Optional API Keys:**
```bash
# AI Services
OPENAI_API_KEY=<openai-key>

# Location Services  
GOOGLE_MAPS_API_KEY=<google-maps-key>

# Notifications
SENDGRID_API_KEY=<sendgrid-key>
TWILIO_ACCOUNT_SID=<twilio-sid>
TWILIO_AUTH_TOKEN=<twilio-token>
FCM_SERVER_KEY=<fcm-key>

# Cloud Storage
AWS_ACCESS_KEY_ID=<aws-key>
AWS_SECRET_ACCESS_KEY=<aws-secret>
S3_BUCKET=<bucket-name>

# Monitoring
SENTRY_DSN=<sentry-dsn>
```

## Development Deployment

### Local Development
```bash
cd deployment
docker-compose up -d

# View logs
docker-compose logs -f api

# Run database migrations
docker-compose exec api python scripts/migrate.py

# Create sample data (optional)
docker-compose exec api python scripts/seed_data.py
```

Services will be available at:
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Grafana: http://localhost:3000
- Prometheus: http://localhost:9090

### Development Commands

```bash
# Stop services
docker-compose down

# Rebuild after code changes
docker-compose build api celery-worker
docker-compose up -d

# Access database
docker-compose exec postgres psql -U eeg_user -d eeg_mental_health

# View worker logs
docker-compose logs -f celery-worker

# Run tests
docker-compose exec api python -m pytest tests/
```

## Production Deployment

### 1. Server Setup

**Minimum Requirements:**
- 4 CPU cores
- 8GB RAM  
- 100GB SSD storage
- Ubuntu 20.04 LTS or similar

**Recommended:**
- 8 CPU cores
- 16GB RAM
- 500GB SSD storage
- Load balancer for high availability

### 2. SSL Certificates

For production, obtain SSL certificates:

```bash
# Using Let's Encrypt (recommended)
sudo apt install certbot
sudo certbot certonly --standalone -d your-domain.com

# Copy certificates to deployment folder
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem deployment/ssl/cert.pem
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem deployment/ssl/key.pem
```

### 3. Production Deployment

```bash
# Set environment to production
export ENVIRONMENT=production

# Use production compose file
cd deployment
docker-compose -f docker-compose.prod.yml up -d

# Run migrations
docker-compose -f docker-compose.prod.yml exec api python scripts/migrate.py

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