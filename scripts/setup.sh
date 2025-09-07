#!/bin/bash

# EEG Mental Health Assistant - Setup Script
# This script sets up the development environment

set -e

echo "🧠 EEG Mental Health Assistant - Setup Script"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed${NC}"
    echo "Please install Docker and Docker Compose first"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Error: Docker Compose is not installed${NC}"
    echo "Please install Docker Compose first"
    exit 1
fi

echo -e "${GREEN}✓ Docker and Docker Compose found${NC}"

# Create necessary directories
echo "📁 Creating project directories..."
mkdir -p {backend/{uploads,logs,ml_models/saved_models},deployment/{ssl,logs,backups},docs}

# Copy environment template if .env doesn't exist
if [ ! -f deployment/.env ]; then
    echo "📝 Creating environment configuration..."
    cat > deployment/.env << EOF
# Database Configuration
POSTGRES_DB=eeg_mental_health
POSTGRES_USER=eeg_user
POSTGRES_PASSWORD=secure_password_$(openssl rand -hex 8)

# Redis Configuration
REDIS_PASSWORD=redis_password_$(openssl rand -hex 8)

# Application Security
SECRET_KEY=$(openssl rand -hex 32)
ENVIRONMENT=development

# External API Keys (optional - add your keys here)
OPENAI_API_KEY=
GOOGLE_MAPS_API_KEY=
SENDGRID_API_KEY=
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=
FCM_SERVER_KEY=

# AWS S3 (for production file storage)
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=us-east-1
S3_BUCKET=

# Monitoring
SENTRY_DSN=
GRAFANA_PASSWORD=admin_$(openssl rand -hex 6)
EOF

    echo -e "${GREEN}✓ Created deployment/.env file${NC}"
    echo -e "${YELLOW}⚠️  Please update the API keys in deployment/.env${NC}"
fi

# Generate self-signed SSL certificates for development
if [ ! -f deployment/ssl/cert.pem ]; then
    echo "🔒 Generating SSL certificates for development..."
    mkdir -p deployment/ssl
    
    openssl req -x509 -newkey rsa:4096 -nodes -out deployment/ssl/cert.pem -keyout deployment/ssl/key.pem -days 365 \
        -subj "/C=US/ST=CA/L=San Francisco/O=EEG Health/OU=Development/CN=localhost"
    
    echo -e "${GREEN}✓ SSL certificates generated${NC}"
fi

# Build and start services
echo "🐳 Building Docker containers..."
cd deployment

# Pull base images
docker-compose pull

# Build custom images
docker-compose build

echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 30

# Check service health
echo "🔍 Checking service health..."

# Check PostgreSQL
if docker-compose exec -T postgres pg_isready -U eeg_user -d eeg_mental_health; then
    echo -e "${GREEN}✓ PostgreSQL is ready${NC}"
else
    echo -e "${RED}✗ PostgreSQL not ready${NC}"
fi

# Check Redis
if docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Redis is ready${NC}"
else
    echo -e "${RED}✗ Redis not ready${NC}"
fi

# Check API
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ FastAPI is ready${NC}"
else
    echo -e "${RED}✗ FastAPI not ready${NC}"
fi

# Run database migrations
echo "📊 Setting up database..."
docker-compose exec api python -c "
from app.core.database import engine, Base
Base.metadata.create_all(bind=engine)
print('Database tables created successfully')
"

# Create sample data (optional)
read -p "Do you want to create sample data for testing? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📝 Creating sample data..."
    docker-compose exec api python scripts/seed_data.py
fi

echo ""
echo -e "${GREEN}🎉 Setup completed successfully!${NC}"
echo ""
echo "Services running:"
echo "  • API: http://localhost:8000"
echo "  • API Docs: http://localhost:8000/docs"
echo "  • Grafana: http://localhost:3000 (admin/admin)"
echo "  • Prometheus: http://localhost:9090"
echo ""
echo "Next steps:"
echo "  1. Update API keys in deployment/.env"
echo "  2. Test the API at http://localhost:8000/docs"
echo "  3. Build the frontend application"
echo ""
echo "To stop all services: cd deployment && docker-compose down"
echo "To view logs: cd deployment && docker-compose logs -f [service-name]"