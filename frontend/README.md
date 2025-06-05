# SentiNexuls Frontend

React-based frontend for the SentiNexuls threat intelligence platform, integrated with the FastAPI backend.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- npm or yarn
- SentiNexuls backend running on `http://localhost:8000`

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

## 🔧 Configuration

### API Integration
The frontend is configured to proxy API requests to the backend:
- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000/api/v1`
- Proxy configured in `vite.config.js`

### Environment Setup
1. Ensure the FastAPI backend is running first
2. The frontend will automatically check backend health on startup
3. Real-time data updates every 30 seconds

## 📊 Features

### Dashboard
- **Live Threat Alerts**: Real-time critical infrastructure alerts
- **Global Threat Map**: Visual threat intelligence overview
- **Agent Network Pulse**: Live agent status and performance
- **Activity Feed**: Recent system activities and alerts
- **KPI Metrics**: Key threat indicators and system health

### API Integration
- **Dashboard Data**: `/api/v1/dashboard`
- **Intel Feed**: `/api/v1/intel-feed`
- **Agent Status**: `/api/v1/agents`
- **Alerts**: `/api/v1/alerts`
- **Vault Settings**: `/api/v1/vault-settings`
- **Simulations**: `/api/v1/simulate`

### Real-time Features
- Auto-refresh every 30 seconds
- Backend health monitoring
- Error handling with retry functionality
- Loading states for all components

## 🛠 Development

### Project Structure
```
frontend/
├── src/
│   ├── App.jsx              # Main application component
│   ├── main.jsx             # React entry point
│   ├── index.css            # Global styles with Tailwind
│   └── services/
│       └── api.js           # API service layer
├── index.html               # HTML template
├── vite.config.js           # Vite configuration
├── tailwind.config.js       # Tailwind CSS configuration
└── package.json             # Dependencies and scripts
```

### Available Scripts
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build

### Styling
- **Tailwind CSS**: Utility-first CSS framework
- **Custom Components**: Reusable UI components
- **Dark Theme**: Cybersecurity-focused dark interface
- **Responsive Design**: Mobile and desktop optimized

## 🔗 Backend Integration

### API Service
The `apiService` in `src/services/api.js` handles all backend communication:

```javascript
import { apiService } from './services/api';

// Get dashboard data
const dashboard = await apiService.getDashboard();

// Run simulation
const result = await apiService.runSimulation({
  vuln_data: {...},
  target_metadata: {...}
});
```

### Error Handling
- Automatic retry functionality
- User-friendly error messages
- Fallback to offline mode if backend unavailable

## 🚀 Production Deployment

### Build
```bash
npm run build
```

### Serve
The built files in `dist/` can be served by any static file server or integrated with the FastAPI backend.

### Environment Variables
- `VITE_API_BASE_URL`: Backend API base URL (default: proxied)
- `VITE_REFRESH_INTERVAL`: Data refresh interval in ms (default: 30000)

## 🔧 Troubleshooting

### Backend Connection Issues
1. Ensure FastAPI backend is running on port 8000
2. Check browser console for API errors
3. Verify CORS configuration in backend
4. Check network connectivity

### Development Issues
1. Clear node_modules and reinstall: `rm -rf node_modules && npm install`
2. Clear Vite cache: `npx vite --force`
3. Check browser console for errors

## 📈 Performance

- **Lazy Loading**: Components load on demand
- **API Caching**: Intelligent request caching
- **Optimized Builds**: Vite-powered fast builds
- **Code Splitting**: Automatic code splitting for optimal loading

## 🔒 Security

- **API Proxy**: All API calls proxied through Vite dev server
- **CORS Handling**: Proper CORS configuration
- **Input Validation**: Client-side input validation
- **Error Boundaries**: Graceful error handling

## 🤝 Contributing

1. Follow the existing code style
2. Add proper error handling for new API calls
3. Update this README for new features
4. Test with both connected and disconnected backend states 