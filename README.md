# SentiNexuls

Advanced threat intelligence and breach simulation platform for critical infrastructure protection with full-stack React + FastAPI implementation.

## 🚀 Overview

SentiNexuls is a comprehensive cybersecurity platform that combines AI-powered threat detection, real-time vulnerability assessment, and breach simulation capabilities. The platform features a modern React frontend integrated with a FastAPI backend, designed to protect critical infrastructure across multiple sectors including energy, water, healthcare, and transportation.

## 🏗 Architecture

### Full-Stack Components
- **React Frontend**: Modern dashboard with real-time threat visualization
- **FastAPI Backend**: RESTful API with comprehensive endpoints
- **Agent Network**: Specialized AI agents for different security functions
- **Orchestrator**: Coordinates agent workflows and data flow
- **Simulation Engine**: Runs breach scenarios in containerized environments
- **Vault Integration**: Web4-native security with DID authentication
- **Logging System**: Comprehensive audit trails and monitoring

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- pip and npm

### Backend Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Start the FastAPI backend
cd backend
uvicorn main:app --reload

# Backend will be available at http://localhost:8000
# API docs at http://localhost:8000/docs
```

### Frontend Setup
```bash
# Install Node.js dependencies
cd frontend
npm install

# Start the React development server
npm run dev

# Frontend will be available at http://localhost:5173
```

### Full System
1. Start the backend first (port 8000)
2. Start the frontend (port 5173)
3. The frontend will automatically connect to the backend API
4. Access the dashboard at http://localhost:5173

## 📊 API Endpoints

### Core Endpoints
- `GET /api/v1/dashboard` - Live ENICO status and agent overview
- `GET /api/v1/intel-feed` - Dark web, OSINT, CVE alerts
- `POST /api/v1/simulate` - Run breach simulations
- `GET /api/v1/agents` - Agent health and retraining status
- `GET /api/v1/alerts` - Recent impact assessments and alert logs
- `GET /api/v1/vault-settings` - Vault ID, DID, token status

### System Endpoints
- `GET /health` - Backend health check
- `GET /api/v1/system/status` - Comprehensive system status
- `POST /api/v1/pipeline/execute` - Execute full agent pipeline

## 🤖 Components

### AI Agents
- **IntelSweepAgent**: Dark web monitoring and OSINT collection
- **VulnDetectAgent**: Vulnerability detection and assessment
- **ImpactAgent**: Risk assessment and impact modeling
- **SimAgent**: Breach simulation and validation
- **AlertAgent**: Alert generation and distribution

### Backend Services
- **FastAPI Application**: RESTful API with automatic documentation
- **Agent Orchestrator**: Coordinates agent workflows
- **Simulation Runner**: Executes breach scenarios
- **Vault Interface**: Web4 security and DID management
- **Logging System**: Structured audit trails

### Frontend Features
- **Real-time Dashboard**: Live threat intelligence and system status
- **Agent Network View**: Monitor agent health and performance
- **Simulation Lab**: Execute and monitor breach simulations
- **Audit Trail**: View system activities and decisions
- **Responsive Design**: Mobile and desktop optimized

## 🔧 Configuration

### Backend Configuration
- **Vault Settings**: `config/vault_config.py`
- **Agent Configuration**: Individual agent classes in `agents/`
- **API Settings**: `backend/main.py` and `backend/api_router.py`

### Frontend Configuration
- **API Integration**: `frontend/src/services/api.js`
- **Styling**: `frontend/tailwind.config.js`
- **Build Settings**: `frontend/vite.config.js`

## 🛠 Development

### Project Structure
```
SentiNexuls/
├── backend/                 # FastAPI backend
│   ├── main.py             # FastAPI application
│   └── api_router.py       # API endpoints
├── frontend/               # React frontend
│   ├── src/
│   │   ├── App.jsx         # Main React component
│   │   └── services/api.js # API integration
│   └── package.json        # Frontend dependencies
├── agents/                 # AI agent implementations
├── orchestrator/           # Agent coordination
├── simulation/             # Breach simulation engine
├── config/                 # Configuration files
├── logging/                # Logging system
└── requirements.txt        # Python dependencies
```

### Running Tests
```bash
# Backend tests
python -m pytest tests/

# Frontend tests (when implemented)
cd frontend && npm test
```

## 🔒 Security Features

- **Web4 Integration**: DID-based authentication and authorization
- **Vault Awareness**: Secure configuration and secret management
- **CORS Protection**: Proper cross-origin request handling
- **Input Validation**: Comprehensive request validation
- **Audit Logging**: Complete activity tracking

## 📈 Monitoring

- **Real-time Metrics**: Live system performance monitoring
- **Health Checks**: Automated system health verification
- **Error Tracking**: Comprehensive error logging and reporting
- **Performance Analytics**: Agent and system performance metrics

## 🚀 Deployment

### Development
- Backend: `uvicorn main:app --reload`
- Frontend: `npm run dev`

### Production
- Backend: `uvicorn main:app --host 0.0.0.0 --port 8000`
- Frontend: `npm run build` then serve `dist/` directory

## 📚 Documentation

- **API Documentation**: Available at `/docs` when backend is running
- **Frontend README**: `frontend/README.md`
- **Agent Documentation**: Individual agent files contain detailed docstrings

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License. 