# EEG Mental Health Assistant - Simplified Version

A clean, simplified AI-powered mental health assistant that analyzes text input for depression screening using transformer models and free AI APIs.

## 🧠 Features

- **Text Analysis**: AI-powered depression screening from user input
- **Depression Classification**: Classifies as not depressed, mild, moderate, or severe
- **AI Chatbot**: Supportive conversations using Gemini/Cohere APIs
- **Simple Setup**: No Docker required, SQLite database
- **Privacy-First**: Local processing with secure data handling

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+ (for frontend)

### Backend Setup

1. **Install dependencies**
```bash
cd backend
pip install -r requirements.txt
```

2. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. **Get free API keys**
- **Gemini**: https://makersuite.google.com/ (Free: 60 requests/minute)
- **Cohere**: https://cohere.ai/ (Free: 100 requests/month)

4. **Run the backend**
```bash
python run.py
```

The API will be available at http://localhost:8000

### Frontend Setup

1. **Install dependencies**
```bash
cd frontend
npm install
```

2. **Start development server**
```bash
npm run dev
```

The frontend will be available at http://localhost:3000

## 📊 Usage

### Text Analysis
1. Navigate to the "Analyze" page
2. Enter your thoughts or feelings in the text area
3. Click "Analyze Mental Health"
4. Get instant depression screening results with recommendations

### AI Assistant
1. Go to the "Assistant" page
2. Chat about mental health topics
3. Get supportive responses and guidance
4. Automatic crisis detection and resource provision

## 🔒 Depression Classification

The system classifies depression into 4 levels:

- **Not Depressed**: No significant indicators
- **Mild Depression**: Early stage, manageable with self-care
- **Moderate Depression**: Clear symptoms, intervention recommended
- **Severe Depression**: Significant impairment, immediate support needed

## 🤖 AI Integration

### Gemini API (Primary)
- 60 requests per minute (free tier)
- Advanced text understanding
- Natural conversation capabilities

### Cohere API (Backup)
- 100 requests per month (free tier)
- Reliable text classification
- Good fallback option

### Rule-based Fallback
- Keyword-based analysis when APIs unavailable
- Ensures system always works
- Privacy-focused local processing

## 🛡️ Safety Features

- **Crisis Detection**: Automatic identification of self-harm language
- **Emergency Resources**: Immediate crisis hotline information
- **Professional Guidance**: Clear recommendations for seeking help
- **Medical Disclaimers**: Appropriate limitations and warnings

## 📁 Project Structure

```
backend/
├── app/
│   ├── api/v1/endpoints/    # API endpoints
│   ├── core/               # Configuration and database
│   ├── models/             # Database models
│   └── services/           # Business logic
├── uploads/                # File storage
└── run.py                 # Application runner

frontend/
├── src/
│   ├── components/         # React components
│   ├── pages/             # Page components
│   ├── services/          # API clients
│   └── utils/             # Utilities
└── package.json
```

## 🔧 Configuration

### Environment Variables

**Required:**
```env
SECRET_KEY=your-secret-key
GEMINI_API_KEY=your-gemini-key
```

**Optional:**
```env
COHERE_API_KEY=your-cohere-key
PINECONE_API_KEY=your-pinecone-key
DATABASE_URL=sqlite:///./eeg_health.db
```

## 🧪 Testing

### Backend Testing
```bash
cd backend
python -m pytest tests/ -v
```

### API Testing
```bash
# Test the API endpoints
curl http://localhost:8000/health
```

## 📈 Monitoring

- Built-in health checks at `/health`
- Structured logging with request tracking
- Simple error handling and reporting

## ⚠️ Important Notes

### Medical Disclaimer
This tool provides supportive insights and is NOT a medical device or diagnostic tool. Always consult healthcare professionals for medical advice.

### Crisis Support
If you're experiencing thoughts of self-harm:
- **National Suicide Prevention Lifeline**: 988
- **Crisis Text Line**: Text HOME to 741741
- **Emergency Services**: 911

### Privacy
- All data stored locally in SQLite
- No cloud dependencies
- User controls their own data

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

---

**Built with ❤️ for accessible mental health support**