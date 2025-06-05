import React, { useState, useEffect } from 'react';
import {
  Bell, Grid, Globe, Users, FlaskConical, ScrollText, BarChart2, Zap, Target, Shield, HeartPulse, HardHat, Beaker, CheckCircle, Package, Lock, DollarSign, Gem, Code, UserCheck, Network, Store, Settings, PlusCircle, Maximize
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

const SectionTitle = ({ children, className = '' }) => (
  <h2 className={`text-xl font-semibold text-blue-300 mb-4 ${className}`}>{children}</h2>
);

const KpiCard = ({ icon: Icon, title, value, change, changeType }) => {
  const changeColor = changeType === 'up' ? 'text-red-400' : changeType === 'down' ? 'text-green-400' : 'text-gray-400';
  const changeArrow = changeType === 'up' ? '↑' : changeType === 'down' ? '↓' : '';
  return (
    <Card className="flex flex-col items-center justify-center p-6 text-center">
      <div className="text-blue-400 mb-2">{Icon && <Icon size={32} />}</div>
      <p className="text-sm text-gray-300 mb-1">{title}</p>
      <p className="text-2xl font-bold text-white">{value}</p>
      {change && <p className={`text-xs ${changeColor}`}>{changeArrow} {change}</p>}
    </Card>
  );
};

// --- Dummy Data (Updated for more context) ---

const DUMMY_ALERTS = [
  {
    id: 'alert-001',
    type: 'CRITICAL',
    infrastructure: 'Power Grid - Substation Alpha (Energy Sector)',
    threat: 'Zero-Day ICS Exploit (CVE-202X-XXXX)',
    impact: 'Regional Blackout (Est. 72 hrs, $50M economic loss)',
    status: 'Simulation Confirmed - Breach Imminent',
    agents: ['AlertAgent', 'SimAgent'],
    polygonScanLink: 'https://polygonscan.com/tx/0xabc123...',
    ipfsLink: 'https://ipfs.io/ipfs/Qmxyz...',
    new: true,
    description: "Highly sophisticated attack targeting critical industrial control systems within Substation Alpha. SimAgent's deep-dive analysis confirmed a successful breach in live-sim environment, indicating a high probability of real-world impact. Immediate action required to mitigate regional blackout.",
  },
  {
    id: 'alert-002',
    type: 'HIGH',
    infrastructure: 'Water Treatment - Plant Beta (Water Sector)',
    threat: 'Outdated Firmware (CVE-2023-YYYY) in Pump Control Unit',
    impact: 'Water Contamination Risk (High Public Health Impact)',
    status: 'Unpatched Vulnerability Detected',
    agents: ['VulnDetectAgent', 'IntelSweepAgent'],
    polygonScanLink: 'https://polygonscan.com/tx/0xdef456...',
    ipfsLink: 'https://ipfs.io/ipfs/Qmaun...',
    new: true,
    description: "VulnDetectAgent identified a critical vulnerability in the pump control unit's firmware, known to be exploitable. IntelSweepAgent found dark web discussions about this specific CVE being actively exploited. Risk of unauthorized chemical dosage or flow disruption leading to contamination.",
  },
  {
    id: 'alert-003',
    type: 'MEDIUM',
    infrastructure: 'City Hospital Z (Healthcare Sector)',
    threat: 'Phishing Campaign Targeting Administrative Staff',
    impact: 'Patient Data Breach Risk (Moderate), Operational Disruption',
    status: 'Ongoing Investigation - Threat Contained',
    agents: ['IntelSweepAgent', 'AlertAgent'],
    polygonScanLink: 'https://polygonscan.com/tx/0xghi789...',
    ipfsLink: 'https://ipfs.io/ipfs/Qmvbn...',
    new: false,
    description: "IntelSweepAgent detected a widespread phishing campaign targeting the hospital's administrative network. Initial analysis suggests attempts to gain access to patient scheduling and billing systems. AlertAgent contained spread, but ongoing vigilance is required.",
  },
];

const DUMMY_AGENTS = [
  {
    id: 'agent-001',
    name: 'IntelSweepAgent',
    status: 'Online',
    task: 'Monitoring Dark Web Feeds',
    health: 98,
    lastActive: '2 min ago',
    did: 'did:ethr:0x123abc...',
    description: 'Specializes in mapping dark web chatter, OSINT, regulatory drops, and geospatial data via Vertex AI multilingual models and custom transformers.',
    recentDecisions: [
      { id: 'd1', type: 'Data Ingested', desc: 'Processed new dark web forum posts.', tx: '0x1a2b3c...', ipfs: 'Qm123...' },
      { id: 'd2', type: 'Signal Flagged', desc: 'Identified suspicious keyword patterns.', tx: '0x2d3e4f...', ipfs: 'Qm456...' },
    ],
    performance: { latency: '30ms', uptime: '99.9%', taskCompletion: '99%' },
    resources: 'Cloud Run Instances: 5, Vertex AI Endpoints: 2',
    zkpStatus: 'Enabled',
    price: '2.5 EONIC/day',
    reputation: 92
  },
  {
    id: 'agent-002',
    name: 'VulnDetectAgent',
    status: 'Online',
    task: 'Analyzing Firmware Configurations',
    health: 95,
    lastActive: '5 min ago',
    did: 'did:ethr:0x456def...',
    description: 'Uses pre-trained models and few-shot adapters to detect novel infrastructure threats across protocol, firmware, and configuration surfaces.',
    recentDecisions: [
      { id: 'd3', type: 'Vulnerability Detected', desc: 'Flagged CVE-2023-YYYY in Water Plant Beta firmware.', tx: '0x3f4a5b...', ipfs: 'Qm789...' },
      { id: 'd4', type: 'Configuration Audit', desc: 'Completed audit of Substation Alpha configs.', tx: '0x4c5d6e...', ipfs: 'Qm012...' },
    ],
    performance: { latency: '50ms', uptime: '99.8%', taskCompletion: '97%' },
    resources: 'Cloud Run Instances: 3, Vertex AI Endpoints: 1',
    zkpStatus: 'Enabled',
    price: '3.0 EONIC/analysis',
    reputation: 95
  },
  {
    id: 'agent-003',
    name: 'SimAgent',
    status: 'Online',
    task: 'Running Grid Breach 007',
    health: 92,
    lastActive: '10 sec ago',
    did: 'did:ethr:0x789ghi...',
    description: 'Containerizes adversarial breach scenarios via GKE, letting SimAgent validate vulnerabilities in live-sim environments.',
    recentDecisions: [
      { id: 'd5', type: 'Simulation Initiated', desc: 'Started simulation for Substation Alpha.', tx: '0x5e6f7a...', ipfs: 'Qm345...' },
      { id: 'd6', type: 'Simulation Completed', desc: 'Grid Breach 007 simulation finished.', tx: '0x6g7h8i...', ipfs: 'Qm678...' },
    ],
    performance: { latency: '20ms', uptime: '99.7%', taskCompletion: '90%' },
    resources: 'GKE Clusters: 1, Cloud Run Instances: 2',
    zkpStatus: 'Disabled',
    price: '5.0 EONIC/simulation',
    reputation: 90
  },
  {
    id: 'agent-004',
    name: 'AlertAgent',
    status: 'Online',
    task: 'Dispatching Briefs',
    health: 99,
    lastActive: '1 min ago',
    did: 'did:ethr:0xjklmno...',
    description: 'Scores and packages validated simulations into mission-critical briefs, delivering real-time, tamper-proof alerts.',
    recentDecisions: [
      { id: 'd7', type: 'Brief Dispatched', desc: 'Dispatched critical brief for Substation Alpha.', tx: '0x7h8i9j...', ipfs: 'Qm901...' },
      { id: 'd8', type: 'Alert Sent', desc: 'Sent email alert for Water Plant Beta.', tx: '0x8k9l0m...', ipfs: 'Qm234...' },
    ],
    performance: { latency: '15ms', uptime: '100%', taskCompletion: '100%' },
    resources: 'Cloud Run Instances: 2',
    zkpStatus: 'Enabled',
    price: '1.0 EONIC/brief',
    reputation: 98
  },
  {
    id: 'agent-005',
    name: 'ImpactAgent',
    status: 'Online',
    task: 'Updating Risk Projections',
    health: 97,
    lastActive: '3 min ago',
    did: 'did:ethr:0xpqrstu...',
    description: 'Runs chain-of-risk projections with weighted graph modeling, visualizing outcomes in real-time via interactive dashboards.',
    recentDecisions: [
      { id: 'd9', type: 'Risk Projection Updated', desc: 'Updated risk for Port Z due to geopolitical events.', tx: '0x9m0n1o...', ipfs: 'Qm567...' },
      { id: 'd10', type: 'Causal Inference', desc: 'Identified root cause for recent healthcare vulnerability.', tx: '0xabcde1...', ipfs: 'Qm890...' },
    ],
    performance: { latency: '40ms', uptime: '99.9%', taskCompletion: '98%' },
    resources: 'Cloud Run Instances: 3, Vertex AI Endpoints: 1',
    zkpStatus: 'Enabled',
    price: '4.0 EONIC/projection',
    reputation: 94
  },
];

const DUMMY_SIMULATIONS = [
  {
    id: 'sim-001',
    name: 'Grid Breach 007 - Substation Alpha',
    status: 'Completed',
    threat: 'Zero-Day ICS Exploit',
    target: 'Power Grid',
    progress: 100,
    impact: 'High',
    report: 'Detailed report on simulated regional blackout due to ICS exploit. Confirmed vulnerability.',
    logs: 'https://console.cloud.google.com/logs/viewer?resource=container.cluster%2F...',
    mitigation: [
      'Isolate compromised segments.',
      'Patch affected firmware (CVE-202X-XXXX).',
      'Implement stricter access controls on OT networks.',
    ],
  },
  {
    id: 'sim-002',
    name: 'Water Plant Beta - Firmware Exploit',
    status: 'Completed',
    threat: 'Outdated Firmware',
    target: 'Water Treatment',
    progress: 100,
    impact: 'High',
    report: 'Comprehensive analysis of water contamination risk from unpatched firmware. Demonstrated control system override.',
    logs: 'https://console.cloud.google.com/logs/viewer?resource=container.cluster%2F...',
    mitigation: [
      'Immediate firmware upgrade.',
      'Review network segmentation between IT/OT.',
      'Implement multi-factor authentication for remote access.',
    ],
  },
  {
    id: 'sim-003',
    name: 'Port Z - Supply Chain Disruption',
    status: 'Pending',
    threat: 'Geopolitical Sabotage',
    target: 'Transportation',
    progress: 0,
    impact: 'Medium',
    report: null,
    logs: null,
    mitigation: [],
  },
];

const DUMMY_AUDIT_LOGS = [
  { id: 'log-001', timestamp: '2025-06-05 01:55 AM', agentDid: 'did:ethr:0xjklmno...', type: 'Brief Dispatched', description: 'Critical Brief for Substation Alpha.', txHash: '0x7h8i9j...', ipfsHash: 'Qm901...', zkpUsed: true },
  { id: 'log-002', timestamp: '2025-06-05 01:50 AM', agentDid: 'did:ethr:0x789ghi...', type: 'Simulation Completed', description: 'Grid Breach 007 simulation finished.', txHash: '0x6g7h8i...', ipfsHash: 'Qm678...', zkpUsed: false },
  { id: 'log-003', timestamp: '2025-06-05 01:40 AM', agentDid: 'did:ethr:0x456def...', type: 'Vulnerability Detected', description: 'Flagged CVE-2023-YYYY in Water Plant Beta firmware.', txHash: '0x3f4a5b...', ipfsHash: 'Qm789...', zkpUsed: true },
  { id: 'log-004', timestamp: '2025-06-05 01:30 AM', agentDid: 'did:ethr:0x123abc...', type: 'Signal Flagged', description: 'Detected elevated dark web chatter related to power grid exploits.', txHash: '0x2d3e4f...', ipfsHash: 'Qm456...', zkpUsed: true },
  { id: 'log-005', timestamp: '2025-06-05 01:20 AM', agentDid: 'did:ethr:0xpqrstu...', type: 'Risk Projection Updated', description: 'Updated risk for Port Z due to new geopolitical events.', txHash: '0x9m0n1o...', ipfs: 'Qm567...', zkpUsed: true },
  { id: 'log-006', timestamp: '2025-06-05 01:10 AM', agentDid: 'did:ethr:0x123abc...', type: 'Data Ingested', description: 'Processed new regulatory drops from EPA.', txHash: '0xabc123...', ipfs: 'Qmdef...', zkpUsed: false },
];

const DUMMY_TRANSACTIONS = [
  { id: 'tx-001', type: 'Earned', amount: '+0.05 EONIC', agent: 'IntelSweepAgent', reason: 'Data validation' },
  { id: 'tx-002', type: 'Spent', amount: '-0.02 EONIC', agent: 'AlertAgent', reason: 'Report generation' },
  { id: 'tx-003', type: 'Earned', amount: '+0.10 EONIC', agent: 'SimAgent', reason: 'Simulation validation' },
  { id: 'tx-004', type: 'Spent', amount: '-0.01 EONIC', agent: 'VulnDetectAgent', reason: 'Model inference' },
];

// --- Dashboard Components ---

const CriticalThreatAlerts = ({ alerts }) => (
  <Card title="Critical Threat Alerts" className="col-span-full xl:col-span-2">
    <div className="space-y-4">
      {alerts.map(alert => (
        <div key={alert.id} className={`${alert.type === 'CRITICAL' ? 'bg-red-900/40 border-red-700' : alert.type === 'HIGH' ? 'bg-orange-900/40 border-orange-700' : 'bg-yellow-900/40 border-yellow-700'} p-6 rounded-lg relative`}>
          {alert.new && <span className="absolute top-2 right-2 text-xs font-bold bg-blue-500 text-white px-2 py-1 rounded-full">NEW!</span>}
          <div className="flex items-center mb-2">
            <Zap size={24} className={alert.type === 'CRITICAL' ? 'text-red-400' : 'text-orange-400'} />
            <h3 className="text-lg font-semibold text-white ml-2">{alert.infrastructure}</h3>
          </div>
          <p className="text-gray-300 text-sm mb-1">Threat: <span className="font-medium">{alert.threat}</span></p>
          <p className="text-gray-300 text-sm mb-1">Impact: <span className="font-medium">{alert.impact}</span></p>
          <p className="text-gray-300 text-sm mb-2">Status: <span className="font-medium">{alert.status}</span></p>
          <p className="text-gray-400 text-xs mb-3">{alert.description}</p>
          <div className="flex justify-between items-center text-xs text-gray-400">
            <span>Agents: {alert.agents.join(', ')}</span>
            <div className="flex space-x-2">
              <a href={alert.polygonScanLink} target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:text-blue-300 underline">On-Chain Proof</a>
              <a href={alert.ipfsLink} target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:text-blue-300 underline">Archived Report</a>
            </div>
          </div>
          <button
            className={`mt-4 w-full py-2 rounded-md font-semibold ${alert.type === 'CRITICAL' ? 'bg-red-600 hover:bg-red-700' : 'bg-orange-600 hover:bg-orange-700'} text-white`}
            onClick={() => alert(`Action: ${alert.type === 'CRITICAL' ? 'Initiate Emergency Response' : 'Review Mitigation Plan'} for ${alert.infrastructure}`)}
          >
            {alert.type === 'CRITICAL' ? 'INITIATE EMERGENCY RESPONSE' : 'REVIEW MITIGATION PLAN'}
          </button>
        </div>
      ))}
    </div>
  </Card>
);

const GlobalThreatMap = () => (
  <Card title="Global Infrastructure Threat Map" className="col-span-full xl:col-span-3 h-96 flex flex-col items-center justify-center bg-gradient-to-br from-blue-900 to-indigo-900 text-white relative overflow-hidden">
    <div className="absolute inset-0 z-0 opacity-20">
      <div className="w-full h-full bg-[radial-gradient(#00F8FF_1px,transparent_1px)] [background-size:20px_20px] [mask-image:radial-gradient(ellipse_at_center,white,transparent)]"></div>
    </div>
    <div className="relative z-10 text-center">
      <Globe size={64} className="mx-auto mb-4 text-blue-400 animate-pulse" />
      <p className="text-xl font-bold mb-2">Global Infrastructure Threat Map</p>
      <p className="text-sm text-gray-300 text-center px-4">
        Visualizing real-time risk across critical systems. Currently monitoring: **Energy, Water, Healthcare, Transportation, Smart Cities, Telecommunications, Supply Chains.**
      </p>
      <p className="text-xs text-gray-500 mt-2">*(Interactive 3D globe visualization placeholder)*</p>
      <p className="text-xs text-green-400 mt-2 flex items-center justify-center">
        <Network size={16} className="mr-1" /> Decentralized Edge Nodes: <span className="font-bold text-lg">120+ Active</span>
      </p>
    </div>
  </Card>
);

const AgentNetworkPulse = ({ setActiveTab }) => {
  const [activeAgents, setActiveAgents] = useState(23);
  useEffect(() => {
    const interval = setInterval(() => {
      setActiveAgents(prev => (prev === 23 ? 24 : 23));
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <Card title="Agent Network Pulse" className="col-span-full md:col-span-1 p-6 flex flex-col items-center justify-center">
      <Users size={32} className="text-green-400 mb-2" />
      <p className="text-sm text-gray-300 mb-1">Total Active Agents</p>
      <p className="text-2xl font-bold text-white">{activeAgents}/24 Online</p>
      <p className="text-xs text-gray-400 mt-2">Decisions Logged (24hr): <span className="font-bold">12,450</span></p>
      <p className="text-xs text-gray-400">Avg. Orchestration Latency: <span className="font-bold">45ms</span></p>
      <button
        className="mt-4 text-blue-400 hover:text-blue-300 text-sm font-medium"
        onClick={() => setActiveTab('agent-network')}
      >
        View Agent Health
      </button>
    </Card>
  );
};

const RecentActivityFeed = ({ logs }) => (
  <Card title="Recent Activity Feed" className="col-span-full md:col-span-2 overflow-auto max-h-80">
    <div className="space-y-2">
      {logs.map(log => (
        <div key={log.id} className="flex items-start text-sm border-b border-gray-700 pb-2 last:border-b-0">
          <span className="text-gray-500 w-24 flex-shrink-0">{log.timestamp.split(' ')[1]}</span>
          <div className="flex-grow ml-2">
            <span className="text-blue-400 font-mono text-xs">{log.agentDid.substring(0, 8)}...</span>
            <span className="text-gray-300 ml-1">: {log.description}</span>
            {log.zkpUsed && <span className="ml-2 text-green-500 text-xs font-semibold"> (ZKP Verified)</span>}
          </div>
          <a href={log.txHash} target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:text-blue-300 text-xs ml-4 flex-shrink-0">Tx Proof</a>
        </div>
      ))}
    </div>
  </Card>
);

// --- Dashboard Component ---
const Dashboard = ({ setActiveTab }) => {
  const [widgets, setWidgets] = useState([
    { id: 'alerts', component: <CriticalThreatAlerts alerts={DUMMY_ALERTS} />, size: 'xl:col-span-2', title: "Critical Threat Alerts" },
    { id: 'map', component: <GlobalThreatMap />, size: 'xl:col-span-3', title: "Global Infrastructure Threat Map" },
    { id: 'kpis', component: (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <KpiCard icon={Shield} title="Cyber Threat Score" value="7.8/10" change="1.2%" changeType="up" />
          <KpiCard icon={Target} title="Active Vulnerabilities" value="12" change="3 New" changeType="up" />
          <KpiCard icon={Beaker} title="Pending Simulations" value="2" change="High Priority" />
        </div>
      ), size: 'xl:col-span-2', title: "Key Threat Indicators" },
    { id: 'agentPulse', component: <AgentNetworkPulse setActiveTab={setActiveTab} />, size: 'md:col-span-1', title: "Agent Network Pulse" },
    { id: 'activityFeed', component: <RecentActivityFeed logs={DUMMY_AUDIT_LOGS.slice(0, 8)} />, size: 'md:col-span-2', title: "Recent Activity Feed" },
  ]);

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
            {React.isValidElement(widget.component) ? (
              widget.id === 'agentPulse'
                ? React.cloneElement(widget.component, { setActiveTab })
                : widget.component
            ) : null}
          </Card>
        </div>
      ))}
    </div>
  );
};

// --- Main App Component ---
const App = () => {
  const [activeTab, setActiveTab] = useState('dashboard');

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard setActiveTab={setActiveTab} />;
      case 'live-threats':
        return (
          <div className="p-6">
            <SectionTitle>Live Threats Overview</SectionTitle>
            <CriticalThreatAlerts alerts={DUMMY_ALERTS} />
          </div>
        );
      case 'infrastructure-map':
        return (
          <div className="p-6">
            <SectionTitle>Global Infrastructure Mapping</SectionTitle>
            <GlobalThreatMap />
            <Card title="Threat Impact Projections" className="mt-6 h-48 flex items-center justify-center">
              <BarChart2 size={48} className="text-yellow-400 mr-4" />
              <p className="text-lg text-gray-300">ImpactAgent's real-time chain-of-risk projections will be visualized here.</p>
            </Card>
          </div>
        );
      case 'agent-network':
        return (
          <div className="p-6">
            <SectionTitle>Agent Network</SectionTitle>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {DUMMY_AGENTS.map(agent => (
                <Card key={agent.id} className="p-6">
                  <div className="flex items-center mb-3">
                    <div className={`w-3 h-3 rounded-full mr-3 ${agent.status === 'Online' ? 'bg-green-500' : 'bg-red-500'}`}></div>
                    <h3 className="text-lg font-semibold text-white">{agent.name}</h3>
                  </div>
                  <p className="text-gray-400 text-sm mb-2">{agent.task}</p>
                  <p className="text-gray-300 text-sm">Health: {agent.health}%</p>
                  <p className="text-gray-300 text-sm">Last Active: {agent.lastActive}</p>
                  <p className="text-gray-400 text-xs mt-2">{agent.description}</p>
                </Card>
              ))}
            </div>
          </div>
        );
      case 'simulation-lab':
        return (
          <div className="p-6">
            <SectionTitle>Simulation Lab</SectionTitle>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {DUMMY_SIMULATIONS.map(sim => (
                <Card key={sim.id} className="p-6">
                  <h3 className="text-lg font-semibold text-white mb-2">{sim.name}</h3>
                  <p className="text-gray-400 text-sm">Threat: {sim.threat}</p>
                  <p className="text-gray-400 text-sm">Target: {sim.target}</p>
                  <p className="text-gray-400 text-sm">Status: {sim.status}</p>
                  <div className="w-full bg-gray-700 rounded-full h-2.5 mt-2">
                    <div className="bg-blue-600 h-2.5 rounded-full" style={{ width: `${sim.progress}%` }}></div>
                  </div>
                </Card>
              ))}
            </div>
          </div>
        );
      case 'audit-trail':
        return (
          <div className="p-6">
            <SectionTitle>Agent Audit Trail (On-Chain Transparency)</SectionTitle>
            <Card className="p-6">
              <div className="overflow-x-auto">
                <table className="min-w-full text-left text-sm text-gray-300">
                  <thead>
                    <tr className="border-b border-gray-700 text-gray-400 uppercase text-xs">
                      <th className="py-2 px-4">Timestamp</th>
                      <th className="py-2 px-4">Agent DID</th>
                      <th className="py-2 px-4">Decision Type</th>
                      <th className="py-2 px-4">Description</th>
                      <th className="py-2 px-4">Tx Hash</th>
                      <th className="py-2 px-4">ZKP</th>
                    </tr>
                  </thead>
                  <tbody>
                    {DUMMY_AUDIT_LOGS.map(log => (
                      <tr key={log.id} className="border-b border-gray-800 hover:bg-gray-700">
                        <td className="py-2 px-4">{log.timestamp}</td>
                        <td className="py-2 px-4 font-mono">{log.agentDid.substring(0, 10)}...</td>
                        <td className="py-2 px-4">{log.type}</td>
                        <td className="py-2 px-4">{log.description}</td>
                        <td className="py-2 px-4">
                          <a href={log.txHash} target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:text-blue-300 underline">
                            {log.txHash.substring(0, 10)}...
                          </a>
                        </td>
                        <td className="py-2 px-4">
                          {log.zkpUsed ? <CheckCircle size={18} className="text-green-500" /> : <span className="text-red-500">N/A</span>}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </Card>
          </div>
        );
      case 'eonic-pylon':
        return (
          <div className="p-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <SectionTitle className="col-span-full">Your EONIC Pylon Hub</SectionTitle>
            <KpiCard icon={Gem} title="My XP Score" value="2,500 XP" change="Next Tier: 5,000 XP" />
            <KpiCard icon={Zap} title="My Impact Score" value="+150" change="3 Critical Mitigations" changeType="up" />
            <KpiCard icon={Lock} title="Vault Access" value="Tier 1" change="Active" changeType="up" />

            <Card title="Agent Economy (Fully On-Chain Micropayments Prototype)" className="col-span-full md:col-span-2 lg:col-span-3 p-6">
              <p className="text-gray-300 text-md mb-4 flex items-center"><DollarSign size={20} className="mr-2 text-green-500"/> My EONIC Balance: <span className="text-white font-bold text-xl ml-2">5.00 EONIC</span></p>

              <h4 className="text-md font-semibold text-gray-300 mb-2">Recent Transactions</h4>
              <div className="space-y-2 text-sm">
                {DUMMY_TRANSACTIONS.map(tx => (
                  <div key={tx.id} className="flex justify-between items-center text-gray-400">
                    <span className={tx.type === 'Earned' ? 'text-green-400' : 'text-red-400'}>{tx.amount}</span>
                    <span>{tx.type === 'Earned' ? 'From' : 'To'} {tx.agent}</span>
                    <span>Reason: {tx.reason}</span>
                  </div>
                ))}
              </div>
              <p className="text-gray-500 text-xs mt-4">Note: Agent-to-agent transactions are logged on-chain for full auditability.</p>
            </Card>
          </div>
        );
      case 'did-marketplace':
        return (
          <div className="p-6">
            <SectionTitle>DID Marketplace: Discover & Deploy Agents</SectionTitle>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {DUMMY_AGENTS.map(agent => (
                <Card key={agent.id} className="relative p-6 group">
                  <div className="flex items-center mb-3">
                    <Users size={32} className="text-purple-400 mr-3" />
                    <h3 className="text-xl font-bold text-white">{agent.name}</h3>
                  </div>
                  <p className="text-gray-400 text-sm mb-2">{agent.description}</p>
                  <div className="text-sm space-y-1 mb-4">
                    <p className="text-gray-300">DID: <span className="font-mono text-xs">{agent.did.substring(0, 15)}...</span></p>
                    <p className="text-gray-300">Reputation: <span className="font-bold text-green-400">{agent.reputation}%</span></p>
                    <p className="text-gray-300">Status: <span className={`${agent.status === 'Online' ? 'text-green-500' : 'text-red-500'} font-medium`}>{agent.status}</span></p>
                    <p className="text-gray-300">ZKP: {agent.zkpStatus === 'Enabled' ? <CheckCircle size={14} className="inline text-green-500" /> : <span className="text-red-500">No</span>}</p>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-2xl font-bold text-yellow-300 flex items-center">
                      <DollarSign size={20} className="mr-1" /> {agent.price}
                    </span>
                    <button
                      className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md font-semibold"
                      onClick={() => alert(`Deploying ${agent.name} for ${agent.price}!`)}
                    >
                      Deploy Agent
                    </button>
                  </div>
                </Card>
              ))}
            </div>
          </div>
        );
      case 'dao-governance':
        return (
          <div className="p-6">
            <SectionTitle>Community-Governed Threat Governance (DAO)</SectionTitle>
            <Card className="p-6 flex flex-col items-center justify-center text-center h-80">
              <UserCheck size={64} className="text-purple-400 mb-4" />
              <p className="text-lg font-semibold text-white mb-2">Participate in SentiNexuls Governance</p>
              <p className="text-gray-300 text-sm mb-4">
                Influence agent behavior updates, response thresholds, and model transparency via token-based voting.
              </p>
              <button
                className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-2 rounded-md font-semibold"
                onClick={() => alert('Navigating to Active DAO Proposals!')}
              >
                View Active Proposals
              </button>
            </Card>
          </div>
        );
      case 'developer-api':
        return (
          <div className="p-6">
            <SectionTitle>Developer API Suite</SectionTitle>
            <Card className="p-6 flex flex-col items-center justify-center text-center h-80">
              <Code size={64} className="text-cyan-400 mb-4" />
              <p className="text-lg font-semibold text-white mb-2">Integrate SentiNexuls Intelligence</p>
              <p className="text-gray-300 text-sm mb-4">
                Embed proactive threat detection and vulnerability insights into your security stacks.
              </p>
              <button
                className="bg-cyan-600 hover:bg-cyan-700 text-white px-6 py-2 rounded-md font-semibold"
                onClick={() => alert('Opening Developer API Documentation!')}
              >
                Access API Documentation
              </button>
            </Card>
          </div>
        );
      default:
        return <Dashboard setActiveTab={setActiveTab} />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white font-inter">
      <script src="https://cdn.tailwindcss.com"></script>
      <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
      
      {/* Top Navigation Bar */}
      <header className="flex items-center justify-between p-4 bg-gray-800 border-b border-gray-700 shadow-xl">
        <div className="flex items-center">
          <h1 className="text-2xl font-bold text-blue-400 mr-8 flex items-center">
            <Zap size={28} className="mr-2 animate-pulse" /> SentiNexuls Vault
          </h1>
          <span className="text-sm text-gray-400 mr-4">Connected: <span className="font-mono text-white">eonic_user_001.eth</span></span>
          <span className="text-sm text-gray-400 flex items-center">
            <Gem size={16} className="text-yellow-400 mr-1" /> EONIC Pylon: <span className="font-bold text-white ml-1">5.00 EONIC</span> (<span className="font-bold text-yellow-300 ml-1">2,500 XP</span>)
          </span>
        </div>
        <div className="flex items-center space-x-6">
          <span className="text-lg font-bold px-4 py-2 rounded-full bg-red-600 text-white animate-pulse">
            ORANGE - ELEVATED RISK
          </span>
          <Bell
            size={24}
            className="text-red-400 cursor-pointer animate-bounce"
            onClick={() => alert('Notifications Panel: Displaying 3 unread critical alerts.')}
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
            <li className={`p-3 rounded-lg cursor-pointer flex items-center font-medium ${activeTab === 'live-threats' ? 'bg-blue-700 text-white' : 'text-gray-300 hover:bg-gray-700'}`} onClick={() => setActiveTab('live-threats')}>
              <Target size={20} className="mr-3" /> Live Threats
            </li>
            <li className={`p-3 rounded-lg cursor-pointer flex items-center font-medium ${activeTab === 'infrastructure-map' ? 'bg-blue-700 text-white' : 'text-gray-300 hover:bg-gray-700'}`} onClick={() => setActiveTab('infrastructure-map')}>
              <Globe size={20} className="mr-3" /> Infrastructure Map
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
            <li className={`p-3 rounded-lg cursor-pointer flex items-center font-medium ${activeTab === 'eonic-pylon' ? 'bg-blue-700 text-white' : 'text-gray-300 hover:bg-gray-700'}`} onClick={() => setActiveTab('eonic-pylon')}>
              <Gem size={20} className="mr-3" /> EONIC Pylon
            </li>
            <li className={`p-3 rounded-lg cursor-pointer flex items-center font-medium ${activeTab === 'did-marketplace' ? 'bg-blue-700 text-white' : 'text-gray-300 hover:bg-gray-700'}`} onClick={() => setActiveTab('did-marketplace')}>
              <Store size={20} className="mr-3" /> DID Marketplace
            </li>
            <li className={`p-3 rounded-lg cursor-pointer flex items-center font-medium ${activeTab === 'dao-governance' ? 'bg-blue-700 text-white' : 'text-gray-300 hover:bg-gray-700'}`} onClick={() => setActiveTab('dao-governance')}>
              <UserCheck size={20} className="mr-3" /> DAO Governance
            </li>
            <li className={`p-3 rounded-lg cursor-pointer flex items-center font-medium ${activeTab === 'developer-api' ? 'bg-blue-700 text-white' : 'text-gray-300 hover:bg-gray-700'}`} onClick={() => setActiveTab('developer-api')}>
              <Code size={20} className="mr-3" /> Developer API
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