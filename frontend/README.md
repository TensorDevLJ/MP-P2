# EEG Mental Health Assistant

A comprehensive, privacy-first AI-powered mental health platform that combines objective EEG brain signals with subjective self-reports to provide personalized mental health insights, recommendations, and care navigation.

## 🧠 Features

### Core Analysis
- **EEG Signal Processing**: Advanced brain signal analysis with frequency band decomposition
- **Text Sentiment Analysis**: Depression and anxiety screening from user input  
- **Fusion Engine**: Combines EEG and text data for comprehensive mental state assessment
- **Interactive Visualizations**: Real-time charts for band powers, PSD, and spectrograms

### AI Assistant
- **Health Chatbot**: AI-powered conversational support with crisis detection
- **Personalized Recommendations**: Evidence-based wellness activities and coping strategies
- **Safety Guardrails**: Automatic escalation to crisis resources when needed
- **Natural Language Explanations**: Clear, accessible explanations of technical results

### Progress & Care
- **Trend Tracking**: Visual progress monitoring with mood calendars and goal tracking
- **Care Provider Discovery**: Find nearby mental health professionals with maps integration
- **Notification System**: Smart reminders for wellness activities and check-ins
- **Privacy Controls**: Comprehensive data management with export and deletion options

## 🛠️ Technology Stack

- **Frontend**: React 18 + Vite + Tailwind CSS
- **Charts**: Chart.js with React wrappers for scientific visualization
- **State Management**: React Query for server state, React hooks for local state
- **Authentication**: JWT-based auth with role-based access control
- **Maps**: Google Maps integration for provider discovery
- **Notifications**: Web Push API with Service Worker support
- **Animations**: Framer Motion for smooth interactions

## 📁 Project Structure

```
src/
├── components/
│   ├── auth/                    # Authentication components
│   ├── dashboard/              # Dashboard and overview components  
│   ├── analysis/               # EEG analysis and visualization
│   ├── chat/                   # AI chatbot components
│   ├── care/                   # Healthcare provider discovery
│   ├── trends/                 # Progress tracking and analytics
│   ├── notifications/          # Notification system
│   └── common/                 # Shared UI components
├── pages/                      # Route-level page components
├── hooks/                      # Custom React hooks
├── services/                   # API clients and external services
├── utils/                      # Helper functions and constants
└── styles/                     # Global and component CSS
```

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ and npm
- Modern web browser with Service Worker support

### Installation

1. **Clone and install dependencies**
```bash
git clone <repository-url>
cd eeg-mental-health-assistant
npm install
```

2. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your API endpoints and keys
```

3. **Start development server**
```bash
npm run dev
```

4. **Access the application**
Open [http://localhost:5173](http://localhost:5173) in your browser

### Environment Variables

Create a `.env` file with these variables:

```env
VITE_API_URL=http://localhost:8000
VITE_GOOGLE_MAPS_API_KEY=your_google_maps_key
VITE_VAPID_PUBLIC_KEY=your_vapid_public_key
```

## 🧪 Usage

### EEG Analysis
1. **Upload Data**: Drag and drop CSV files with EEG channel data
2. **Configure Analysis**: Set sampling rate, channels, and epoch parameters
3. **Add Context**: Optionally include text about your current mood/state
4. **View Results**: Interactive charts show frequency bands, PSD, and spectrograms
5. **Get Insights**: AI-generated explanations and personalized recommendations

### Health Assistant
1. **Ask Questions**: Chat about mental health topics, EEG results, or general wellness
2. **Get Explanations**: Understand your analysis results in plain language
3. **Receive Guidance**: Evidence-based coping strategies and wellness activities
4. **Crisis Support**: Automatic detection and resource provision for high-risk situations

### Progress Tracking
1. **Set Goals**: Define wellness objectives like meditation streaks or regular analysis
2. **Track Trends**: Visualize mood patterns and EEG metrics over time
3. **Monitor Achievements**: Celebrate milestones and maintain motivation
4. **Export Data**: Download comprehensive reports for healthcare providers

## 🔒 Privacy & Security

- **End-to-End Encryption**: All data encrypted in transit and at rest
- **Data Minimization**: Raw EEG files deleted within 24 hours after processing
- **User Control**: Complete data export and deletion capabilities
- **HIPAA Compliance**: Medical-grade privacy protections
- **Transparent Processing**: Clear explanations of what data is collected and how it's used

## 📊 Supported Data Formats

### EEG Data
- **CSV**: Columns for timestamps and EEG channels (e.g., EEG.AF3, EEG.AF4)
- **JSON**: Structured format with metadata and signal arrays
- **TXT**: Raw numeric data with configurable parsing
- **Sampling Rates**: 128Hz to 1000Hz (auto-detected from filename)
- **Channels**: Standard 10-20 system electrode positions

### Text Input  
- **Free-form text**: Journal entries, mood descriptions, symptom reports
- **Character limits**: 10-5000 characters for meaningful analysis
- **Languages**: English primary, with expansion planned for Hindi, Spanish, French

## 🎨 Design System

### Colors
- **Primary**: Blue (#3B82F6) - Trust, technology, calm
- **Success**: Green (#22c55e) - Positive states, achievements
- **Warning**: Amber (#F59E0B) - Caution, mild concerns
- **Error**: Red (#EF4444) - High risk, critical alerts

### Typography
- **Font**: Inter (primary), system fallbacks
- **Scales**: Modular scale for consistent hierarchy
- **Line Height**: 150% for body text, 120% for headings

### Spacing
- **Base unit**: 8px grid system
- **Component padding**: 16px, 24px, 32px
- **Layout gaps**: 24px, 32px, 48px

## 🔧 Development

### Available Scripts
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

### Code Organization
- **Component-based architecture** with clear separation of concerns
- **Custom hooks** for state management and API integration  
- **Service layer** for external API communication
- **Utility functions** for common operations and formatting
- **Type safety** with PropTypes and JSDoc annotations

### Testing Strategy
- **Component testing** with React Testing Library
- **API integration testing** with MSW (Mock Service Worker)
- **E2E testing** with Playwright for critical user journeys
- **Accessibility testing** with axe-core and manual verification

## 🌐 Browser Support

- **Modern browsers**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Mobile browsers**: iOS Safari 14+, Chrome Mobile 90+
- **PWA features**: Service Worker, Web Push, offline functionality
- **Accessibility**: WCAG 2.1 AA compliance

## 📱 Progressive Web App

This application includes PWA features:

- **Offline support** for core functionality
- **Push notifications** for wellness reminders
- **Home screen installation** on mobile devices
- **Background sync** for data when connection returns

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Contribution Guidelines
- Follow existing code style and patterns
- Add tests for new functionality
- Update documentation for user-facing changes
- Ensure accessibility compliance
- Include medical disclaimer for health-related features

## ⚠️ Medical Disclaimer

**IMPORTANT**: This platform provides supportive insights based on AI analysis and should NOT be used as a substitute for professional medical diagnosis or treatment. 

- Results are for informational purposes only
- Always consult qualified healthcare providers for medical advice
- In crisis situations, contact emergency services or crisis hotlines immediately
- The platform includes built-in crisis detection and resource provision

### Crisis Resources
- **National Suicide Prevention Lifeline**: 988
- **Crisis Text Line**: Text HOME to 741741
- **Emergency Services**: 911

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Mental health research community for evidence-based practices
- Open source EEG processing libraries (MNE-Python inspiration)
- Healthcare providers who review and validate our recommendations
- Users who trust us with their mental health journey

---

**Built with ❤️ for mental health awareness and accessible care**