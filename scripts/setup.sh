# scripts/setup.sh
#!/bin/bash

echo "🧠 Setting up EEG Mental Health Assistant..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create environment file
if [ ! -f .env ]; then
    echo "📝 Creating environment file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your API keys before continuing"
    exit 1
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p backend/app/services/ml/models/trained_models
mkdir -p ml_models/saved_models
mkdir -p deployment/ssl
mkdir -p logs

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
cd backend
pip install -r requirements.txt
cd ..

# Install Node.js dependencies  
echo "📦 Installing Node.js dependencies..."
cd frontend
npm install
cd ..

# Build and start services
echo "🚀 Building and starting services..."
docker-compose up --build -d

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 30

# Run database migrations
echo "🗄️ Running database migrations..."
docker-compose exec backend alembic upgrade head

# Seed initial data
echo "🌱 Seeding initial data..."
docker-compose exec backend python scripts/seed_data.py

echo "✅ Setup complete!"
echo ""
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "📖 Visit http://localhost:3000/how-to-use for detailed usage instructions"