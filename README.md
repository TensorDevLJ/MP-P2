# EEG Mental Health Assistant


A privacy-first, AI-powered mental health companion that combines EEG brain wave analysis with text sentiment analysis to provide personalized mental wellness insights and recommendations.

## 🧠 Overview

The EEG Mental Health Assistant uses state-of-the-art machine learning to analyze:
- **EEG Signals**: Objective brain wave patterns indicating emotional and anxiety states
- **Text Input**: Subjective self-reports analyzed for depression and sentiment indicators
- **Combined Analysis**: Fused insights with safety-first decision making

**⚠️ Important Disclaimer**: This tool provides supportive insights and is NOT a medical device or diagnostic tool. Always consult healthcare professionals for medical advice.

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  React Frontend │    │  FastAPI Backend│    │   ML Pipeline   │
│                 │───▶│                 │───▶│                 │
│ • Upload UI     │    │ • Authentication│    │ • EEG Processing│
│ • Visualization │    │ • API Endpoints │    │ • CNN-LSTM Model│
│ • Chat Interface│    │ • Background     │    │ • Text Analysis │
└─────────────────┘    │   Tasks         │    │ • Fusion Engine │
                       └─────────────────┘    └─────────────────┘
                                │
                       ┌─────────────────┐
                       │  Data Storage   │
                       │                 │
                       │ • PostgreSQL    │
                       │ • Redis Queue   │
                       │ • S3 Files      │
                       └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for development)
- Node.js 18+ (for frontend development)

### Installation

1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd eeg-mental-health-assistant
   ```

2. **Run Setup Script**
   ```bash
   chmod +x scripts/setup.sh
   ./scripts/setup.sh
   ```

3. **Configure Environment**
   ```bash
   # Copy environment template
   cp deployment/.env.example deployment/.env
   
   # Edit with your API keys (optional for basic functionality)
   nano deployment/.env
   ```

4. **Start Services**
   ```bash
   cd deployment
   docker-compose up -d
   ```

5. **Access Applications**
   - API Documentation: http://localhost:8000/docs
   - Grafana Monitoring: http://localhost:3000
   - Prometheus Metrics: http://localhost:9090

## 📊 Features

### Core Analysis
- **EEG Signal Processing**: Advanced filtering, epoching, and feature extraction
- **Brain Wave Analysis**: Delta, theta, alpha, beta, gamma band power analysis
- **Emotion Detection**: Happy, sad, neutral, stressed, relaxed classification
- **Anxiety Assessment**: Low, moderate, high anxiety level detection
- **Text Analysis**: Depression severity assessment using RoBERTa
- **Safety Detection**: Automatic crisis language identification

### Intelligence & Guidance
- **Fusion Engine**: Combines EEG and text insights with safety rules
- **AI Chatbot**: Health-focused conversational assistant with safety guardrails
- **Personalized Recommendations**: Evidence-based interventions and coping strategies
- **Progress Tracking**: Longitudinal analysis of mental health patterns

### Care & Support
- **Provider Discovery**: Google Maps integration to find nearby mental health professionals
- **Smart Notifications**: Multi-channel reminders and check-ins (push, email, SMS)
- **Crisis Support**: Immediate emergency resources when concerning patterns detected
- **Data Export**: GDPR-compliant data portability

### Privacy & Security
- **End-to-End Encryption**: AES-256 encryption for all sensitive data
- **Granular Consent**: Control over data usage and sharing
- **Row Level Security**: Database-level access controls
- **Audit Trails**: Complete logging of all data access

## 🧪 API Usage

### Authentication
```bash
# Register new user
curl -X POST "http://localhost:8000/api/v1/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!",
    "display_name": "John Doe"
  }'

# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user@example.com", 
    "password": "SecurePass123!"
  }'
```

### EEG Analysis
```bash
# Upload EEG file
curl -X POST "http://localhost:8000/api/v1/eeg/upload" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@path/to/eeg_data.csv"

# Process EEG data
curl -X POST "http://localhost:8000/api/v1/eeg/process" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "file_key": "uploaded_file_key",
    "channel": "EEG.AF3", 
    "sampling_rate": 128
  }'
```

### Text Analysis
```bash
# Analyze text for depression indicators
curl -X POST "http://localhost:8000/api/v1/text/analyze" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "I have been feeling down and unmotivated lately..."
  }'
```

## 🛠️ Development

### Backend Development

```bash
# Set up Python environment
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
python -m pytest tests/ -v

# Format code
black .
isort .
```

### Training ML Models

```bash
# Generate synthetic training data
cd ml_models
python datasets/generate_synthetic_data.py

# Train EEG model
python training/train_eeg_model.py --epochs 50 --batch_size 32

# Train text model  
python training/train_text_model.py --epochs 3 --batch_size 16

# Evaluate models
python evaluation/model_evaluation.py
```

### Database Management

```bash
# Run migrations
python scripts/migrate.py

# Create sample data
python scripts/seed_data.py

# Backup database
docker-compose exec postgres pg_dump -U eeg_user eeg_mental_health > backup.sql
```

## 🔧 Configuration

### Environment Variables

**Required:**
- `SECRET_KEY`: JWT signing key
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string

**Optional API Keys:**
- `OPENAI_API_KEY`: For chatbot functionality
- `GOOGLE_MAPS_API_KEY`: For provider discovery
- `SENDGRID_API_KEY`: For email notifications
- `TWILIO_*`: For SMS notifications

### ML Model Configuration

```python
# EEG Model Settings
DEFAULT_SAMPLING_RATE = 128
DEFAULT_EPOCH_LENGTH = 2.0
DEFAULT_OVERLAP = 0.5

# Model Paths
EEG_MODEL_PATH = "ml_models/saved_models/eeg_cnn_lstm.pth"
TEXT_MODEL_PATH = "ml_models/saved_models/roberta_depression"
```

## 📈 Monitoring

### Health Checks
- **API Health**: `GET /health`
- **Database**: Connection pool status
- **Redis**: Queue length and connectivity
- **ML Models**: Inference latency and accuracy

### Metrics (Prometheus)
- Request latency and throughput
- Error rates by endpoint
- ML model performance
- Resource utilization

### Logging
- Structured JSON logging
- Error tracking with Sentry
- Audit trails for compliance
- Performance monitoring

## 🔒 Security

### Data Protection
- **Encryption**: AES-256 at rest, TLS 1.3 in transit
- **Access Control**: JWT authentication with short expiration
- **Database Security**: Row Level Security (RLS) policies
- **Input Validation**: Comprehensive request validation

### Privacy Features
- **Data Minimization**: Only collect necessary information
- **Consent Management**: Granular control over data usage
- **Right to Deletion**: Complete data removal on request
- **Export Capability**: GDPR-compliant data portability

### Safety Features
- **Crisis Detection**: Automatic identification of concerning language
- **Emergency Resources**: Immediate provision of crisis support contacts
- **Professional Referral**: Guidance to appropriate care levels
- **Medical Disclaimers**: Clear limitations and recommendations

## 🚀 Deployment

### Development
```bash
cd deployment
docker-compose up -d
```

### Production
```bash
# Use production configuration
docker-compose -f docker-compose.prod.yml up -d

# Set up SSL certificates
certbot certonly --standalone -d your-domain.com

# Configure monitoring
# See deployment/README.md for detailed instructions
```

### Cloud Platforms
- **AWS**: ECS with RDS and ElastiCache
- **Google Cloud**: Cloud Run with Cloud SQL
- **Azure**: Container Instances with PostgreSQL
- **Heroku**: Direct deployment support

## 📚 Documentation

- **[API Documentation](docs/api_documentation.md)**: Complete API reference
- **[Deployment Guide](docs/deployment_guide.md)**: Production deployment instructions
- **[User Guide](docs/user_guide.md)**: End-user documentation
- **[Development Setup](docs/development.md)**: Developer onboarding

## 🧪 Testing

### Automated Testing
```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=app --cov-report=html

# Load testing
locust -f scripts/load_test.py --host=http://localhost:8000
```

### Manual Testing
```bash
# API integration tests
python scripts/test_api.py

# ML pipeline tests
python ml_models/notebooks/eeg_analysis_demo.py
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Add tests for new features
- Update documentation
- Ensure security best practices
- Test with sample data

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This software is provided for educational and research purposes. It is not intended for medical diagnosis or treatment. Users experiencing mental health crises should contact emergency services or qualified healthcare providers immediately.

The AI models provide insights based on patterns in data but cannot account for all factors affecting mental health. This tool should complement, not replace, professional mental healthcare.

## 📞 Support

- **Documentation**: Check the docs/ directory
- **Issues**: GitHub Issues for bug reports
- **Security**: security@eeghealth.app for security concerns
- **General**: support@eeghealth.app

## 🙏 Acknowledgments

- MNE-Python community for EEG processing tools
- Hugging Face for transformer models
- FastAPI and SQLAlchemy communities
- Mental health research community
- Open source contributors

---

**Built with ❤️ for mental health awareness and support**



