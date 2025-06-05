import React, { useState, useEffect } from 'react';
import {
  Bell, Grid, Globe, Users, FlaskConical, ScrollText, BarChart2, Zap, Target, Shield, HeartPulse, HardHat, Beaker, CheckCircle, Package, Lock, DollarSign, Gem, Code, Handshake, Network, Store, Settings, PlusCircle, Maximize
} from 'lucide-react';
import { apiService, checkBackendHealth } from './services/api';

// --- Utility Components ---

const Card = ({ children, className = '', title = '' }) => {
  return (
    <div className={`bg-gray-800 rounded-lg p-4 shadow-lg border border-gray-700 relative ${className}`}>
      {title && <h3 className="text-lg font-semibold text-blue-300 mb-3">{title}</h3>}
      {children}
    </div>
  );
};

const SectionTitle = ({ children, className = '' }) => (
  <h2 className={`text-xl font-semibold text-blue-300 mb-4 ${className}`}>{children}</h2>
);

const KpiCard = ({ icon: Icon, title, value, change, changeType }) => {
  const changeColor = changeType === 'up' ? 'text-red-400' : changeType === 'down' ? 'text-green-400' : 'text-gray-400';
  const changeArrow = changeType === 'up' ? '↑' : changeType === 'down' ? '↓' : '';
  return (
    <div className="flex flex-col items-center justify-center p-6 text-center">
      <div className="text-blue-400 mb-2">{Icon && <Icon size={32} />}</div>
      <p className="text-sm text-gray-300 mb-1">{title}</p>
      <p className="text-2xl font-bold text-white">{value}</p>
      {change && <p className={`text-xs ${changeColor}`}>{changeArrow} {change}</p>}
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

// --- Dashboard Components ---

const CriticalThreatAlerts = ({ alerts, loading, error, onRetry }) => {
  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} onRetry={onRetry} />;
  if (!alerts || alerts.length === 0) {
    return <div className="text-gray-400 text-center p-8">No critical alerts at this time</div>;
  }

  return (
    <div className="space-y-4">
      {alerts.map(alert => (
        <div key={alert.alert_id} className={`${alert.severity === 'CRITICAL' ? 'bg-red-900/40 border-red-700' : alert.severity === 'HIGH' ? 'bg-orange-900/40 border-orange-700' : 'bg-yellow-900/40 border-yellow-700'} p-6 rounded-lg relative`}>
          <div className="flex items-center mb-2">
            <Zap size={24} className={alert.severity === 'CRITICAL' ? 'text-red-400' : 'text-orange-400'} />
            <h3 className="text-lg font-semibold text-white ml-2">{alert.title}</h3>
          </div>
          <p className="text-gray-300 text-sm mb-1">Impact Score: <span className="font-medium">{alert.impact_score}</span></p>
          <p className="text-gray-300 text-sm mb-1">Affected Systems: <span className="font-medium">{alert.affected_systems?.join(', ')}</span></p>
          <p className="text-gray-300 text-sm mb-2">Status: <span className="font-medium">{alert.status}</span></p>
          <p className="text-gray-400 text-xs mb-3">{alert.description}</p>
          <div className="flex justify-between items-center text-xs text-gray-400">
            <span>Dispatched to: {alert.dispatched_to?.join(', ')}</span>
            <span className="text-blue-400">{new Date(alert.timestamp).toLocaleString()}</span>
          </div>
          <button
            className={`mt-4 w-full py-2 rounded-md font-semibold ${alert.severity === 'CRITICAL' ? 'bg-red-600 hover:bg-red-700' : 'bg-orange-600 hover:bg-orange-700'} text-white`}
            onClick={() => alert(`Action: ${alert.severity === 'CRITICAL' ? 'Initiate Emergency Response' : 'Review Mitigation Plan'} for ${alert.title}`)}
          >
            {alert.severity === 'CRITICAL' ? 'INITIATE EMERGENCY RESPONSE' : 'REVIEW MITIGATION PLAN'}
          </button>
        </div>
      ))}
    </div>
  );
};

const GlobalThreatMap = ({ intelData, loading, error }) => {
  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;

  const threatCount = intelData?.total_threats || 0;
  const criticalThreats = intelData?.critical_threats || 0;

  return (
    <div className="h-96 flex flex-col items-center justify-center bg-gradient-to-br from-blue-900 to-indigo-900 text-white relative overflow-hidden">
      <div className="absolute inset-0 z-0 opacity-20">
        <div className="w-full h-full bg-[radial-gradient(#00F8FF_1px,transparent_1px)] [background-size:20px_20px] [mask-image:radial-gradient(ellipse_at_center,white,transparent)]"></div>
      </div>
      <div className="relative z-10 text-center">
        <Globe size={64} className="mx-auto mb-4 text-blue-400 animate-pulse" />
        <p className="text-xl font-bold mb-2">Global Infrastructure Threat Map</p>
        <p className="text-sm text-gray-300 text-center px-4">
          Monitoring {threatCount} active threats across critical infrastructure.
          {criticalThreats > 0 && <span className="text-red-400 font-bold"> {criticalThreats} Critical</span>}
        </p>
        <p className="text-xs text-gray-500 mt-2">*(Interactive 3D globe visualization placeholder)*</p>
        <p className="text-xs text-green-400 mt-2 flex items-center justify-center">
          <Network size={16} className="mr-1" /> Last Updated: {intelData?.last_updated ? new Date(intelData.last_updated).toLocaleString() : 'Unknown'}
        </p>
      </div>
    </div>
  );
};

const AgentNetworkPulse = ({ setActiveTab, agentsData, loading, error }) => {
  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;

  const activeAgents = agentsData?.system_health?.active_agents || 0;
  const totalAgents = agentsData?.system_health?.total_agents || 0;
  const throughput = agentsData?.system_health?.pipeline_throughput || 'Unknown';
  const executions = agentsData?.performance_metrics?.total_executions_today || 0;

  return (
    <div className="p-6 flex flex-col items-center justify-center">
      <Users size={32} className="text-green-400 mb-2" />
      <p className="text-sm text-gray-300 mb-1">Total Active Agents</p>
      <p className="text-2xl font-bold text-white">{activeAgents}/{totalAgents} Online</p>
      <p className="text-xs text-gray-400 mt-2">Executions Today: <span className="font-bold">{executions}</span></p>
      <p className="text-xs text-gray-400">Pipeline Throughput: <span className="font-bold">{throughput}</span></p>
      <button
        className="mt-4 text-blue-400 hover:text-blue-300 text-sm font-medium"
        onClick={() => setActiveTab('agent-network')}
      >
        View Agent Health
      </button>
    </div>
  );
};

const RecentActivityFeed = ({ alerts, loading, error }) => {
  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;

  const recentAlerts = alerts?.recent_alerts?.slice(0, 8) || [];

  return (
    <div className="overflow-auto max-h-80">
      <div className="space-y-2">
        {recentAlerts.map(alert => (
          <div key={alert.alert_id} className="flex items-start text-sm border-b border-gray-700 pb-2 last:border-b-0">
            <span className="text-gray-500 w-24 flex-shrink-0">{new Date(alert.timestamp).toLocaleTimeString()}</span>
            <div className="flex-grow ml-2">
              <span className="text-blue-400 font-mono text-xs">{alert.alert_id}</span>
              <span className="text-gray-300 ml-1">: {alert.title}</span>
              {alert.vault_integration && <span className="ml-2 text-green-500 text-xs font-semibold"> (Vault Verified)</span>}
            </div>
            <span className={`text-xs ml-4 flex-shrink-0 ${alert.severity === 'CRITICAL' ? 'text-red-400' : alert.severity === 'HIGH' ? 'text-orange-400' : 'text-yellow-400'}`}>
              {alert.severity}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};

// --- Dashboard Component ---
const Dashboard = ({ setActiveTab }) => {
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

  const widgets = [
    { 
      id: 'alerts', 
      component: <CriticalThreatAlerts 
        alerts={alertsData?.recent_alerts} 
        loading={loading} 
        error={error} 
        onRetry={fetchDashboardData} 
      />, 
      size: 'xl:col-span-2', 
      title: "Critical Threat Alerts" 
    },
    { 
      id: 'map', 
      component: <GlobalThreatMap 
        intelData={intelData} 
        loading={loading} 
        error={error} 
      />, 
      size: 'xl:col-span-3', 
      title: "Global Infrastructure Threat Map" 
    },
    { 
      id: 'kpis', 
      component: (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <KpiCard 
            icon={Shield} 
            title="Active Threats" 
            value={intelData?.total_threats || 0} 
            change={intelData?.critical_threats ? `${intelData.critical_threats} Critical` : ''} 
            changeType="up" 
          />
          <KpiCard 
            icon={Target} 
            title="Active Alerts" 
            value={alertsData?.alert_statistics?.active_alerts || 0} 
            change={alertsData?.alert_statistics?.critical_alerts ? `${alertsData.alert_statistics.critical_alerts} Critical` : ''} 
            changeType="up" 
          />
          <KpiCard 
            icon={Beaker} 
            title="System Health" 
            value={agentsData?.system_health?.overall_status || 'Unknown'} 
            change={agentsData?.system_health?.system_uptime || ''} 
          />
        </div>
      ), 
      size: 'xl:col-span-2', 
      title: "Key Threat Indicators" 
    },
    { 
      id: 'agentPulse', 
      component: <AgentNetworkPulse 
        setActiveTab={setActiveTab} 
        agentsData={agentsData} 
        loading={loading} 
        error={error} 
      />, 
      size: 'md:col-span-1', 
      title: "Agent Network Pulse" 
    },
    { 
      id: 'activityFeed', 
      component: <RecentActivityFeed 
        alerts={alertsData} 
        loading={loading} 
        error={error} 
      />, 
      size: 'md:col-span-2', 
      title: "Recent Activity Feed" 
    },
  ];

  const handleCustomizeClick = () => {
    alert('Dashboard customization is under development! Imagine dragging and dropping widgets here to create your personalized view.');
  };

  return (
    <div className="p-6 grid grid-cols-1 xl:grid-cols-3 gap-6 relative">
      <button
        className="absolute top-4 right-4 bg-gray-700 hover:bg-gray-600 text-white px-3 py-1 rounded-md text-sm flex items-center z-10"
        onClick={handleCustomizeClick}
      >
        <Settings size={16} className="mr-2" /> Customize Layout
      </button>

      {widgets.map(widget => (
        <div key={widget.id} className={`${widget.size} col-span-full`}>
          <Card title={widget.title} className="h-full">
            {widget.component}
          </Card>
        </div>
      ))}
    </div>
  );
};

// --- Placeholder Components (keeping original structure) ---
const AgentNetwork = () => (
  <div className="p-6">
    <SectionTitle>Agent Network</SectionTitle>
    <Card className="p-6 text-center">
      <Users size={48} className="mx-auto mb-4 text-blue-400" />
      <p className="text-lg text-gray-300">Agent Network interface will be integrated with live API data</p>
      <p className="text-sm text-gray-400 mt-2">Coming soon with real-time agent status and performance metrics</p>
    </Card>
  </div>
);

const SimulationLab = () => (
  <div className="p-6">
    <SectionTitle>Simulation Lab</SectionTitle>
    <Card className="p-6 text-center">
      <FlaskConical size={48} className="mx-auto mb-4 text-green-400" />
      <p className="text-lg text-gray-300">Simulation Lab interface will be integrated with live API data</p>
      <p className="text-sm text-gray-400 mt-2">Coming soon with real-time simulation execution and results</p>
    </Card>
  </div>
);

const AuditTrail = () => (
  <div className="p-6">
    <SectionTitle>Audit Trail</SectionTitle>
    <Card className="p-6 text-center">
      <ScrollText size={48} className="mx-auto mb-4 text-purple-400" />
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
        return <Dashboard setActiveTab={setActiveTab} />;
      case 'agent-network':
        return <AgentNetwork />;
      case 'simulation-lab':
        return <SimulationLab />;
      case 'audit-trail':
        return <AuditTrail />;
      default:
        return <Dashboard setActiveTab={setActiveTab} />;
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
          <span className="text-sm text-gray-400 flex items-center">
            <Gem size={16} className="text-yellow-400 mr-1" /> API Status: <span className="font-bold text-white ml-1">Live Data</span>
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
            <li className={`p-3 rounded-lg cursor-pointer flex items-center font-medium ${activeTab === 'dashboard' ? 'bg-blue-700 text-white' : 'text-gray-300 hover:bg-gray-700'}`} onClick={() => setActiveTab('dashboard')}>
              <Grid size={20} className="mr-3" /> Dashboard
            </li>
            <li className={`p-3 rounded-lg cursor-pointer flex items-center font-medium ${activeTab === 'agent-network' ? 'bg-blue-700 text-white' : 'text-gray-300 hover:bg-gray-700'}`} onClick={() => setActiveTab('agent-network')}>
              <Users size={20} className="mr-3" /> Agent Network
            </li>
            <li className={`p-3 rounded-lg cursor-pointer flex items-center font-medium ${activeTab === 'simulation-lab' ? 'bg-blue-700 text-white' : 'text-gray-300 hover:bg-gray-700'}`} onClick={() => setActiveTab('simulation-lab')}>
              <FlaskConical size={20} className="mr-3" /> Simulation Lab
            </li>
            <li className={`p-3 rounded-lg cursor-pointer flex items-center font-medium ${activeTab === 'audit-trail' ? 'bg-blue-700 text-white' : 'text-gray-300 hover:bg-gray-700'}`} onClick={() => setActiveTab('audit-trail')}>
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