# AI Financial Copilot

An intelligent multi-agent system for financial analysis, portfolio management, and investment advisory powered by Large Language Models.

## 🚀 Features

- **Multi-Agent Architecture**: Specialized agents for different financial tasks
  - 🧠 Planner Agent: Orchestrates other agents based on user intent
  - 📊 Market Data Agent: Fetches real-time stock prices and market data
  - 💼 Portfolio Agent: Analyzes portfolio composition and performance
  - ⚠️ Risk Agent: Calculates risk metrics and provides risk assessments
  - 📰 News Agent: Analyzes financial news and market sentiment

- **Conversational Interface**: Natural language chat for financial queries
- **Portfolio Management**: Track and analyze investment portfolios
- **Risk Analysis**: Calculate Sharpe ratio, VaR, volatility, and other metrics
- **Market Intelligence**: Real-time market data and news analysis
- **MLOps Integration**: Prompt versioning, evaluation, and monitoring

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Frontend  │─────▶│   Backend    │─────▶│  LLM APIs   │
│  (Next.js)  │      │  (FastAPI)   │      │ (OpenAI)    │
└─────────────┘      └──────────────┘      └─────────────┘
                            │
                            ├───▶ PostgreSQL (Data)
                            ├───▶ Redis (Cache)
                            └───▶ External APIs (Market Data)
```

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.11+
- **Database**: PostgreSQL
- **Cache**: Redis
- **LLMs**: OpenAI GPT-4, Anthropic Claude
- **Market Data**: Alpha Vantage, Yahoo Finance

### Frontend
- **Framework**: Next.js 14
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios

### Infrastructure
- **Containerization**: Docker, Docker Compose
- **Reverse Proxy**: Nginx
- **CI/CD**: GitHub Actions

## 📦 Installation

### Prerequisites
- Docker and Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for local development)
- API Keys: OpenAI, Alpha Vantage

### Quick Start with Docker

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-financial-copilot.git
cd ai-financial-copilot
```

2. Create environment file:
```bash
cp backend/.env.example backend/.env
# Edit backend/.env with your API keys
```

3. Start all services:
```bash
docker-compose -f infra/docker-compose.yml up
```

4. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Local Development

#### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## 🔧 Configuration

### Environment Variables

Create `backend/.env` file:
```env
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
DATABASE_URL=postgresql://user:password@localhost:5432/financial_copilot
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key
```

## 📊 Usage Examples

### Chat with the AI Financial Copilot

```python
# Example queries:
"What's the current price of Apple stock?"
"Analyze my portfolio risk"
"Should I diversify into bonds?"
"Latest news about Tesla"
```

### API Examples

```python
import requests

# Get stock quote
response = requests.post(
    "http://localhost:8000/api/v1/chat",
    json={"message": "What's AAPL trading at?"}
)

# Analyze portfolio
response = requests.post(
    "http://localhost:8000/api/v1/portfolio/123/analyze"
)
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v --cov=app
```

### Frontend Tests
```bash
cd frontend
npm test
```

### Agent Evaluation
```bash
cd mlops/evaluation
python evaluator.py
```

## 📈 MLOps

The system includes MLOps capabilities:

- **Prompt Versioning**: Track and version system prompts
- **Evaluation**: Automated testing with test queries
- **Monitoring**: Track agent performance and routing accuracy
- **Experiments**: A/B testing for different configurations

## 🚀 Deployment

### Docker Deployment
```bash
docker-compose -f infra/docker-compose.yml up -d
```

### Cloud Deployment
- Configure environment variables
- Set up managed PostgreSQL and Redis
- Deploy containers to cloud platform (AWS ECS, GCP Cloud Run, etc.)

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This is an AI-powered financial assistant for informational purposes only. It does not constitute financial advice. Always consult with a qualified financial advisor before making investment decisions.

## 📧 Contact

- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

## 🙏 Acknowledgments

- OpenAI for GPT models
- Anthropic for Claude
- Alpha Vantage for market data API
- FastAPI and Next.js communities

---

**Built with ❤️ by [Your Name]**
