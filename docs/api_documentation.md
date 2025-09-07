# EEG Mental Health Assistant API Documentation

## Overview

The EEG Mental Health Assistant API provides a comprehensive backend for analyzing EEG signals and text inputs to assess mental health indicators. The system combines objective neurophysiological data with subjective self-reports to provide personalized mental health insights and recommendations.

## Authentication

All API endpoints (except `/health` and authentication endpoints) require JWT authentication.

### Authentication Flow

1. **Register**: `POST /api/v1/auth/signup`
2. **Login**: `POST /api/v1/auth/login` 
3. **Use Token**: Include `Authorization: Bearer <token>` header in requests

### Example Authentication

```bash
# Register
curl -X POST "http://localhost:8000/api/v1/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!",
    "display_name": "John Doe",
    "consent_research": true
  }'

# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user@example.com",
    "password": "SecurePass123!"
  }'
```

## Core API Endpoints

### EEG Analysis

#### Upload EEG File
```http
POST /api/v1/eeg/upload
Content-Type: multipart/form-data
Authorization: Bearer <token>

file: <CSV file with EEG data>
```

**Response:**
```json
{
  "file_key": "eeg/user-id/session-id/filename.csv",
  "filename": "recording.csv",
  "size_bytes": 1048576,
  "sampling_rate": 128,
  "channels": ["EEG.AF3", "EEG.F7", "EEG.F3"],
  "duration_seconds": 300.5
}
```

#### Process EEG Data
```http
POST /api/v1/eeg/process
Content-Type: application/json
Authorization: Bearer <token>

{
  "file_key": "eeg/user-id/session-id/filename.csv",
  "sampling_rate": 128,
  "channel": "EEG.AF3",
  "epoch_length": 2.0,
  "overlap": 0.5
}
```

#### Get EEG Results
```http
GET /api/v1/eeg/result/{job_id}
Authorization: Bearer <token>
```

**Response:**
```json
{
  "job_id": "session-uuid",
  "status": "completed",
  "emotion_results": {
    "label": "stressed",
    "probabilities": {
      "happy": 0.10,
      "sad": 0.15,
      "neutral": 0.20,
      "stressed": 0.45,
      "relaxed": 0.10
    },
    "confidence": 0.75
  },
  "anxiety_results": {
    "label": "moderate",
    "probabilities": {
      "low": 0.20,
      "moderate": 0.65,
      "high": 0.15
    },
    "confidence": 0.65
  },
  "eeg_features": {
    "band_powers": {
      "mean": {
        "delta": 0.15,
        "theta": 0.25,
        "alpha": 0.30,
        "beta": 0.25,
        "gamma": 0.05
      }
    }
  },
  "charts_data": {
    "bands_timeseries": {
      "times": [0, 2, 4, 6, 8, 10],
      "data": {
        "alpha": [0.3, 0.28, 0.32, 0.29, 0.31, 0.30],
        "beta": [0.25, 0.27, 0.23, 0.26, 0.24, 0.25]
      }
    },
    "psd": {
      "frequencies": [0.5, 1.0, 1.5, 2.0, ...],
      "power": [0.1, 0.12, 0.08, 0.15, ...]
    },
    "spectrogram_base64": "iVBORw0KGgoAAAANSUhEUgAA..."
  },
  "explanations": [
    "Elevated beta power suggests active mental processing",
    "Alpha-beta ratio indicates mild stress levels"
  ]
}
```

### Text Analysis

#### Analyze Text Input
```http
POST /api/v1/text/analyze
Content-Type: application/json
Authorization: Bearer <token>

{
  "text": "I've been feeling really down lately and nothing seems to bring me joy anymore. Having trouble sleeping and feeling hopeless about the future."
}
```

**Response:**
```json
{
  "session_id": "text-session-uuid",
  "depression_analysis": {
    "label": "moderate",
    "probabilities": {
      "not_depressed": 0.15,
      "moderate": 0.70,
      "severe": 0.15
    },
    "confidence": 0.70
  },
  "sentiment_analysis": {
    "label": "negative",
    "score": 0.85
  },
  "safety_flags": {
    "has_crisis_indicators": false,
    "risk_level": "low"
  }
}
```

### Combined Analysis

#### Run Combined EEG + Text Analysis
```http
POST /api/v1/analysis/combined
Content-Type: application/json
Authorization: Bearer <token>

{
  "file_key": "eeg/user-id/session-id/filename.csv",
  "text_input": "Feeling anxious and overwhelmed today...",
  "sampling_rate": 128,
  "channel": "EEG.AF3"
}
```

### Chatbot

#### Send Chat Message
```http
POST /api/v1/chat/message
Content-Type: application/json
Authorization: Bearer <token>

{
  "message": "Can you explain what my EEG results mean?",
  "session_id": "optional-session-context"
}
```

**Response:**
```json
{
  "response": "Based on your recent EEG analysis, the elevated beta waves suggest your brain was in an active, alert state. This often happens when we're focused or experiencing some stress...",
  "crisis_detected": false,
  "suggestions": [
    "What do the different brain wave patterns mean?",
    "How can I reduce stress levels?",
    "When should I consider professional help?"
  ],
  "disclaimer": "This assistant provides supportive information only..."
}
```

### Healthcare Providers

#### Find Nearby Providers
```http
GET /api/v1/care/nearby?lat=37.7749&lng=-122.4194&specialty=psychiatrist&radius=10000
Authorization: Bearer <token>
```

### Notifications

#### Schedule Reminder
```http
POST /api/v1/notifications/schedule-reminder
Content-Type: application/json
Authorization: Bearer <token>

{
  "type": "meditation_reminder",
  "title": "Time to Meditate",
  "message": "Your daily 10-minute meditation session is ready",
  "scheduled_for": "2025-01-15T09:00:00Z",
  "channels": ["push", "email"]
}
```

## Data Models

### User Profile
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "display_name": "John Doe",
  "timezone": "America/New_York",
  "consent_research": true,
  "consent_data_sharing": false,
  "created_at": "2025-01-01T00:00:00Z"
}
```

### Analysis Session
```json
{
  "id": "uuid",
  "user_id": "uuid", 
  "session_type": "combined",
  "status": "completed",
  "emotion_results": {...},
  "anxiety_results": {...},
  "depression_results": {...},
  "fusion_results": {...},
  "created_at": "2025-01-01T12:00:00Z"
}
```

## Error Handling

The API uses standard HTTP status codes:

- `200` - Success
- `400` - Bad Request (validation errors)
- `401` - Unauthorized (invalid/missing token)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found
- `422` - Unprocessable Entity (schema validation)
- `500` - Internal Server Error

Error responses follow this format:
```json
{
  "detail": "Error message",
  "error_code": "VALIDATION_ERROR",
  "timestamp": "2025-01-01T12:00:00Z"
}
```

## Rate Limiting

- Authentication: 3 requests per minute
- File uploads: 1 request per second
- General API: 5 requests per second
- Chat messages: 10 requests per minute

## Security

### Data Protection
- All data encrypted at rest (AES-256)
- TLS 1.3 for data in transit
- Row Level Security (RLS) on all user data
- Audit logging for all actions

### Safety Features
- Crisis detection in text analysis
- Automatic escalation for high-risk cases
- Emergency resource provision
- Medical disclaimer enforcement

### Privacy Compliance
- GDPR-compliant data export
- Right to be forgotten implementation
- Granular consent management
- Data retention controls

## Rate Limits and Quotas

| Endpoint Category | Rate Limit | Quota |
|------------------|------------|-------|
| Authentication | 3/min | - |
| File Upload | 1/sec | 100MB/day |
| EEG Processing | 5/hour | 50 files/day |
| Text Analysis | 60/hour | 1000 analyses/day |
| Chat Messages | 10/min | 500 messages/day |

## Monitoring and Observability

### Health Checks
- `GET /health` - System health status
- `GET /` - Basic service status

### Metrics Endpoints
- `GET /metrics` - Prometheus metrics
- Response times, error rates, resource usage

### Logging
- Structured JSON logging with correlation IDs
- Error tracking with Sentry integration
- Audit trails for security compliance

## Development and Testing

### Running Locally
```bash
cd deployment
docker-compose up -d
```

### Testing Endpoints
Access interactive documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Sample API Calls
See `/scripts/test_api.py` for comprehensive API testing examples.