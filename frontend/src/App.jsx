import React, { useState, useEffect } from 'react';
import { apiService, checkBackendHealth } from './services/api';

// Import icons individually to avoid potential issues
import { 
  Bell, 
  Grid, 
  Globe, 
  Users, 
  FlaskConical, 
  ScrollText, 
  Zap, 
  Shield, 
  Target,
  Settings
} from 'lucide-react';

// --- Utility Components ---
const Card = ({ children, className = '', title = '' }) => {
  return (
    <div className={`bg-gray-800 rounded-lg p-4 shadow-lg border border-gray-700 relative ${className}`}>
      {title && <h3 className="text-lg font-semibold text-blue-300 mb-3">{title}</h3>}
      {children}
    </div>
  );
};

const LoadingSpinner = () => (
  <div className="flex items-center justify-center p-8">
    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-400"></div>
    <span className="ml-2 text-gray-400">Loading...</span>
  </div>
);

const ErrorMessage = ({ message, onRetry }) => (
  <div className="flex flex-col items-center justify-center p-8 text-center">
    <div className="text-red-400 mb-2">⚠️</div>
    <p className="text-red-400 mb-4">{message}</p>
    {onRetry && (
      <button 
        onClick={onRetry}
        className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md"
      >
        Retry
      </button>
    )}
  </div>
);

// --- Dashboard Component ---
const Dashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [intelData, setIntelData] = useState(null);
  const [agentsData, setAgentsData] = useState(null);
  const [alertsData, setAlertsData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const [dashboard, intel, agents, alerts] = await Promise.all([
        apiService.getDashboard(),
        apiService.getIntelFeed(),
        apiService.getAgents(),
        apiService.getAlerts()
      ]);

      setDashboardData(dashboard);
      setIntelData(intel);
      setAgentsData(agents);
      setAlertsData(alerts);
    } catch (err) {
      setError(`Failed to load dashboard: ${err.message}`);
      console.error('Dashboard fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
    
    // Refresh data every 30 seconds
    const interval = setInterval(fetchDashboardData, 30000);
    return () => clearInterval(interval);
  }, []);

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} onRetry={fetchDashboardData} />;

  return (
    <div className="p-6 space-y-6">
      {/* Status Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card title="ENICO Status">
          <div className="flex items-center justify-center p-6">
            <Shield size={32} className="text-green-400 mr-4" />
            <div>
              <p className="text-lg font-bold text-white">
                {dashboardData?.enico_status?.status || 'Unknown'}
              </p>
              <p className="text-sm text-gray-400">
                Vault: {dashboardData?.enico_status?.vault_id || 'N/A'}
              </p>
            </div>
          </div>
        </Card>

        <Card title="Agent Overview">
          <div className="flex items-center justify-center p-6">
            <Users size={32} className="text-blue-400 mr-4" />
            <div>
              <p className="text-lg font-bold text-white">
                {dashboardData?.agent_overview?.active_agents || 0}/{dashboardData?.agent_overview?.total_agents || 0}
              </p>
              <p className="text-sm text-gray-400">Agents Online</p>
            </div>
          </div>
        </Card>

        <Card title="Threat Summary">
          <div className="flex items-center justify-center p-6">
            <Target size={32} className="text-red-400 mr-4" />
            <div>
              <p className="text-lg font-bold text-white">
                {dashboardData?.threat_summary?.active_threats || 0}
              </p>
              <p className="text-sm text-gray-400">
                {dashboardData?.threat_summary?.critical_alerts || 0} Critical
              </p>
            </div>
          </div>
        </Card>
      </div>

      {/* Global Threat Map */}
      <Card title="Global Infrastructure Threat Map">
        <div className="h-64 flex flex-col items-center justify-center bg-gradient-to-br from-blue-900 to-indigo-900 text-white relative overflow-hidden rounded-lg">
          <div className="relative z-10 text-center">
            <Globe size={64} className="mx-auto mb-4 text-blue-400 animate-pulse" />
            <p className="text-xl font-bold mb-2">Global Infrastructure Threat Map</p>
            <p className="text-sm text-gray-300 text-center px-4">
              Monitoring {intelData?.total_threats || 0} active threats across critical infrastructure.
              {intelData?.critical_threats > 0 && (
                <span className="text-red-400 font-bold"> {intelData.critical_threats} Critical</span>
              )}
            </p>
            <p className="text-xs text-gray-500 mt-2">*(Interactive 3D globe visualization placeholder)*</p>
          </div>
        </div>
      </Card>

      {/* Recent Activity */}
      <Card title="Recent Activity Feed">
        <div className="space-y-2 max-h-64 overflow-auto">
          {alertsData?.recent_alerts?.slice(0, 5).map((alert, index) => (
            <div key={index} className="flex items-start text-sm border-b border-gray-700 pb-2 last:border-b-0">
              <span className="text-gray-500 w-20 flex-shrink-0">
                {new Date().toLocaleTimeString()}
              </span>
              <div className="flex-grow ml-2">
                <span className="text-blue-400 font-mono text-xs">ALT-{String(index + 1).padStart(3, '0')}</span>
                <span className="text-gray-300 ml-1">: {alert?.title || 'System Alert'}</span>
              </div>
              <span className="text-xs ml-4 flex-shrink-0 text-yellow-400">
                {alert?.severity || 'INFO'}
              </span>
            </div>
          )) || (
            <div className="text-gray-400 text-center p-4">No recent activity</div>
          )}
        </div>
      </Card>

      {/* API Data Display */}
      <Card title="Live API Data">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <h4 className="text-blue-300 font-semibold mb-2">Dashboard Data</h4>
            <pre className="bg-gray-900 p-3 rounded text-xs overflow-auto max-h-32">
              {JSON.stringify(dashboardData, null, 2)}
            </pre>
          </div>
          <div>
            <h4 className="text-blue-300 font-semibold mb-2">Intel Feed</h4>
            <pre className="bg-gray-900 p-3 rounded text-xs overflow-auto max-h-32">
              {JSON.stringify(intelData, null, 2)}
            </pre>
          </div>
        </div>
      </Card>
    </div>
  );
};

// --- Placeholder Components ---
const AgentNetwork = () => (
  <div className="p-6">
    <Card className="p-6 text-center">
      <Users size={48} className="mx-auto mb-4 text-blue-400" />
      <h2 className="text-xl font-semibold text-blue-300 mb-4">Agent Network</h2>
      <p className="text-lg text-gray-300">Agent Network interface will be integrated with live API data</p>
      <p className="text-sm text-gray-400 mt-2">Coming soon with real-time agent status and performance metrics</p>
    </Card>
  </div>
);

const SimulationLab = () => (
  <div className="p-6">
    <Card className="p-6 text-center">
      <FlaskConical size={48} className="mx-auto mb-4 text-green-400" />
      <h2 className="text-xl font-semibold text-blue-300 mb-4">Simulation Lab</h2>
      <p className="text-lg text-gray-300">Simulation Lab interface will be integrated with live API data</p>
      <p className="text-sm text-gray-400 mt-2">Coming soon with real-time simulation execution and results</p>
    </Card>
  </div>
);

const AuditTrail = () => (
  <div className="p-6">
    <Card className="p-6 text-center">
      <ScrollText size={48} className="mx-auto mb-4 text-purple-400" />
      <h2 className="text-xl font-semibold text-blue-300 mb-4">Audit Trail</h2>
      <p className="text-lg text-gray-300">Audit Trail interface will be integrated with live API data</p>
      <p className="text-sm text-gray-400 mt-2">Coming soon with real-time audit logs and transaction history</p>
    </Card>
  </div>
);

// --- Main App Component ---
const App = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [backendStatus, setBackendStatus] = useState('checking');

  useEffect(() => {
    // Check backend health on startup
    checkBackendHealth()
      .then(health => {
        setBackendStatus(health.status === 'healthy' ? 'connected' : 'disconnected');
      })
      .catch(() => {
        setBackendStatus('disconnected');
      });
  }, []);

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard />;
      case 'agent-network':
        return <AgentNetwork />;
      case 'simulation-lab':
        return <SimulationLab />;
      case 'audit-trail':
        return <AuditTrail />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white font-inter">
      {/* Top Navigation Bar */}
      <header className="flex items-center justify-between p-4 bg-gray-800 border-b border-gray-700 shadow-xl">
        <div className="flex items-center">
          <h1 className="text-2xl font-bold text-blue-400 mr-8 flex items-center">
            <Zap size={28} className="mr-2 animate-pulse" /> SentiNexuls Vault
          </h1>
          <span className="text-sm text-gray-400 mr-4">
            Backend: 
            <span className={`ml-1 font-bold ${backendStatus === 'connected' ? 'text-green-400' : backendStatus === 'disconnected' ? 'text-red-400' : 'text-yellow-400'}`}>
              {backendStatus === 'connected' ? '🟢 Connected' : backendStatus === 'disconnected' ? '🔴 Disconnected' : '🟡 Checking...'}
            </span>
          </span>
        </div>
        <div className="flex items-center space-x-6">
          <span className="text-lg font-bold px-4 py-2 rounded-full bg-blue-600 text-white">
            LIVE API MODE
          </span>
          <Bell
            size={24}
            className="text-blue-400 cursor-pointer"
            onClick={() => alert('Real-time notifications from API endpoints')}
          />
        </div>
      </header>

      {/* Main Layout */}
      <div className="flex">
        {/* Left Sidebar */}
        <nav className="w-64 bg-gray-800 border-r border-gray-700 p-4 min-h-[calc(100vh-80px)] shadow-xl">
          <ul className="space-y-3">
            <li 
              className={`p-3 rounded-lg cursor-pointer flex items-center font-medium ${activeTab === 'dashboard' ? 'bg-blue-700 text-white' : 'text-gray-300 hover:bg-gray-700'}`} 
              onClick={() => setActiveTab('dashboard')}
            >
              <Grid size={20} className="mr-3" /> Dashboard
            </li>
            <li 
              className={`p-3 rounded-lg cursor-pointer flex items-center font-medium ${activeTab === 'agent-network' ? 'bg-blue-700 text-white' : 'text-gray-300 hover:bg-gray-700'}`} 
              onClick={() => setActiveTab('agent-network')}
            >
              <Users size={20} className="mr-3" /> Agent Network
            </li>
            <li 
              className={`p-3 rounded-lg cursor-pointer flex items-center font-medium ${activeTab === 'simulation-lab' ? 'bg-blue-700 text-white' : 'text-gray-300 hover:bg-gray-700'}`} 
              onClick={() => setActiveTab('simulation-lab')}
            >
              <FlaskConical size={20} className="mr-3" /> Simulation Lab
            </li>
            <li 
              className={`p-3 rounded-lg cursor-pointer flex items-center font-medium ${activeTab === 'audit-trail' ? 'bg-blue-700 text-white' : 'text-gray-300 hover:bg-gray-700'}`} 
              onClick={() => setActiveTab('audit-trail')}
            >
              <ScrollText size={20} className="mr-3" /> Audit Trail
            </li>
          </ul>
        </nav>

        {/* Content Area */}
        <main className="flex-1 overflow-auto">
          {renderContent()}
        </main>
      </div>
    </div>
  );
};

export default App;