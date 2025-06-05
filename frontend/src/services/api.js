import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: '/api/v1', // Proxied through Vite to http://localhost:8000/api/v1
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('❌ API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('❌ API Response Error:', error.response?.status, error.response?.data);
    return Promise.reject(error);
  }
);

// API service functions
export const apiService = {
  // Dashboard endpoint
  getDashboard: async () => {
    try {
      const response = await api.get('/dashboard');
      return response.data;
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
      throw error;
    }
  },

  // Intel feed endpoint
  getIntelFeed: async () => {
    try {
      const response = await api.get('/intel-feed');
      return response.data;
    } catch (error) {
      console.error('Failed to fetch intel feed:', error);
      throw error;
    }
  },

  // Agents endpoint
  getAgents: async () => {
    try {
      const response = await api.get('/agents');
      return response.data;
    } catch (error) {
      console.error('Failed to fetch agents data:', error);
      throw error;
    }
  },

  // Alerts endpoint
  getAlerts: async () => {
    try {
      const response = await api.get('/alerts');
      return response.data;
    } catch (error) {
      console.error('Failed to fetch alerts:', error);
      throw error;
    }
  },

  // Vault settings endpoint
  getVaultSettings: async () => {
    try {
      const response = await api.get('/vault-settings');
      return response.data;
    } catch (error) {
      console.error('Failed to fetch vault settings:', error);
      throw error;
    }
  },

  // Simulation endpoint
  runSimulation: async (simulationData) => {
    try {
      const response = await api.post('/simulate', simulationData);
      return response.data;
    } catch (error) {
      console.error('Failed to run simulation:', error);
      throw error;
    }
  },

  // System status endpoint
  getSystemStatus: async () => {
    try {
      const response = await api.get('/system/status');
      return response.data;
    } catch (error) {
      console.error('Failed to fetch system status:', error);
      throw error;
    }
  },

  // Execute pipeline endpoint
  executePipeline: async (inputData) => {
    try {
      const response = await api.post('/pipeline/execute', inputData);
      return response.data;
    } catch (error) {
      console.error('Failed to execute pipeline:', error);
      throw error;
    }
  },
};

// Health check function
export const checkBackendHealth = async () => {
  try {
    const response = await axios.get('http://localhost:8000/health');
    return response.data;
  } catch (error) {
    console.error('Backend health check failed:', error);
    return { status: 'unhealthy', error: error.message };
  }
};

export default api; 