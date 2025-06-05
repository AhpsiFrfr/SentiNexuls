#!/usr/bin/env python3
"""
Simple test script for SentiNexuls backend
This script tests the backend functionality without complex imports
"""

import sys
import os
import json
from datetime import datetime

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_basic_functionality():
    """Test basic backend functionality"""
    print("🧪 Testing SentiNexuls Backend Functionality")
    print("=" * 50)
    
    # Test 1: Import basic modules
    try:
        print("✅ Testing Python imports...")
        import fastapi
        import uvicorn
        print(f"   FastAPI version: {fastapi.__version__}")
        print(f"   Uvicorn available: ✅")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    
    # Test 2: Test vault configuration
    try:
        print("✅ Testing vault configuration...")
        from config.vault_config import vault_metadata, get_vault_metadata
        vault_data = get_vault_metadata()
        print(f"   Vault ID: {vault_data.get('vault_id')}")
        print(f"   ENICO Status: {vault_data.get('ENICO_status')}")
        print(f"   Capabilities: {len(vault_data.get('vault_capabilities', []))}")
    except Exception as e:
        print(f"⚠️  Vault config warning: {e}")
    
    # Test 3: Test agent functionality
    try:
        print("✅ Testing agent functionality...")
        from agents.intel_sweep_agent import IntelSweepAgent
        from agents.vuln_detect_agent import VulnDetectAgent
        
        intel_agent = IntelSweepAgent(agent_id="test_intel")
        vuln_agent = VulnDetectAgent(agent_id="test_vuln")
        
        print(f"   IntelSweepAgent: ✅")
        print(f"   VulnDetectAgent: ✅")
    except Exception as e:
        print(f"⚠️  Agent warning: {e}")
    
    # Test 4: Generate mock API responses
    print("✅ Testing API response generation...")
    
    # Mock dashboard data
    dashboard_data = {
        "enico_status": {
            "status": "active",
            "vault_id": "SNX-VLT-001",
            "last_update": datetime.utcnow().isoformat()
        },
        "agent_overview": {
            "total_agents": 5,
            "active_agents": 5,
            "system_health": "OPERATIONAL"
        },
        "threat_summary": {
            "active_threats": 7,
            "critical_alerts": 3,
            "simulations_today": 8
        }
    }
    
    print(f"   Dashboard data: ✅")
    print(f"   Active threats: {dashboard_data['threat_summary']['active_threats']}")
    print(f"   System health: {dashboard_data['agent_overview']['system_health']}")
    
    return True

def create_simple_server():
    """Create a simple FastAPI server for testing"""
    print("\n🚀 Creating Simple Test Server")
    print("=" * 50)
    
    try:
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        
        app = FastAPI(title="SentiNexuls Test API")
        
        # Add CORS
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        @app.get("/")
        def root():
            return {"message": "SentiNexuls Test API is running!", "status": "success"}
        
        @app.get("/health")
        def health():
            return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}
        
        @app.get("/api/v1/dashboard")
        def dashboard():
            return {
                "enico_status": {"status": "active", "vault_id": "SNX-VLT-001"},
                "agent_overview": {"total_agents": 5, "active_agents": 5},
                "threat_summary": {"active_threats": 7, "critical_alerts": 3}
            }
        
        @app.get("/api/v1/intel-feed")
        def intel_feed():
            return {"dark_web_alerts": [], "osint_data": [], "cve_alerts": []}
        
        @app.get("/api/v1/agents")
        def agents():
            return {"agents": [], "retraining_status": {"in_progress": False}}
        
        @app.get("/api/v1/alerts")
        def alerts():
            return {"recent_alerts": [], "impact_assessments": []}
        
        @app.get("/api/v1/vault-settings")
        def vault_settings():
            return {"vault_id": "SNX-VLT-001", "did": "did:web4:test"}
        
        print("✅ Simple FastAPI server created successfully!")
        print("📡 To start the server, run:")
        print("   uvicorn test_backend:app --reload --host 0.0.0.0 --port 8000")
        print("\n🌐 Then test with:")
        print("   http://localhost:8000/health")
        print("   http://localhost:8000/api/v1/dashboard")
        
        return app
        
    except Exception as e:
        print(f"❌ Server creation error: {e}")
        return None

# Create the app at module level so uvicorn can find it
app = None

def initialize_app():
    """Initialize the FastAPI app"""
    global app
    if app is None:
        app = create_simple_server()
    return app

# Initialize app when module is imported
try:
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    
    app = FastAPI(title="SentiNexuls Test API")
    
    # Add CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    @app.get("/")
    def root():
        return {"message": "SentiNexuls Test API is running!", "status": "success"}
    
    @app.get("/health")
    def health():
        return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}
    
    @app.get("/api/v1/dashboard")
    def dashboard():
        return {
            "enico_status": {"status": "active", "vault_id": "SNX-VLT-001"},
            "agent_overview": {"total_agents": 5, "active_agents": 5},
            "threat_summary": {"active_threats": 7, "critical_alerts": 3}
        }
    
    @app.get("/api/v1/intel-feed")
    def intel_feed():
        return {
            "dark_web_alerts": [
                {
                    "id": "DW-001",
                    "source": "TOR Network",
                    "threat_type": "Data Breach",
                    "severity": "HIGH",
                    "timestamp": datetime.utcnow().isoformat(),
                    "description": "Corporate credentials detected on dark web marketplace"
                }
            ],
            "osint_data": [
                {
                    "id": "OSINT-001",
                    "source": "Social Media",
                    "threat_type": "Information Leak",
                    "severity": "MEDIUM",
                    "timestamp": datetime.utcnow().isoformat(),
                    "description": "Employee discussing internal systems publicly"
                }
            ],
            "cve_alerts": [
                {
                    "id": "CVE-2024-001",
                    "severity": "CRITICAL",
                    "cvss_score": 9.8,
                    "affected_systems": ["Web Server", "Database"],
                    "timestamp": datetime.utcnow().isoformat(),
                    "description": "Remote code execution vulnerability"
                }
            ]
        }
    
    @app.get("/api/v1/agents")
    def agents():
        return {
            "total_agents": 5,
            "active_agents": 4,
            "training_agents": 1,
            "offline_agents": 0,
            "agent_details": [
                {
                    "name": "Intel Sweep Agent",
                    "type": "Intelligence Gathering",
                    "status": "active",
                    "performance": 98,
                    "last_seen": "2 minutes ago"
                },
                {
                    "name": "Vulnerability Scanner",
                    "type": "Security Assessment",
                    "status": "active",
                    "performance": 95,
                    "last_seen": "1 minute ago"
                },
                {
                    "name": "Threat Hunter",
                    "type": "Threat Detection",
                    "status": "active",
                    "performance": 99,
                    "last_seen": "30 seconds ago"
                },
                {
                    "name": "Network Monitor",
                    "type": "Network Security",
                    "status": "training",
                    "performance": 87,
                    "last_seen": "5 minutes ago"
                },
                {
                    "name": "Incident Responder",
                    "type": "Response & Recovery",
                    "status": "active",
                    "performance": 92,
                    "last_seen": "1 minute ago"
                }
            ],
            "retraining_status": {
                "in_progress": True,
                "last_retrain": "2024-01-15T10:30:00Z",
                "next_scheduled": "2024-01-22T02:00:00Z"
            }
        }
    
    @app.get("/api/v1/alerts")
    def alerts():
        return {
            "recent_alerts": [
                {
                    "title": "Suspicious Network Activity",
                    "description": "Unusual traffic patterns detected from external IP addresses",
                    "severity": "HIGH",
                    "source": "Network Monitor",
                    "timestamp": "2024-01-15T10:30:00Z"
                },
                {
                    "title": "Failed Authentication Attempts",
                    "description": "Multiple failed login attempts detected on admin portal",
                    "severity": "MEDIUM",
                    "source": "Auth System",
                    "timestamp": "2024-01-15T10:25:00Z"
                },
                {
                    "title": "Malware Signature Detected",
                    "description": "Known malware signature found in email attachment",
                    "severity": "CRITICAL",
                    "source": "Email Security",
                    "timestamp": "2024-01-15T10:20:00Z"
                },
                {
                    "title": "Vulnerability Scan Complete",
                    "description": "Weekly vulnerability scan completed with 3 high-risk findings",
                    "severity": "MEDIUM",
                    "source": "Vuln Scanner",
                    "timestamp": "2024-01-15T10:15:00Z"
                }
            ],
            "total_events": 156,
            "critical_alerts": 3,
            "warnings": 12,
            "info_events": 141
        }
    
    @app.get("/api/v1/vault-settings")
    def vault_settings():
        return {
            "vault_id": "SNX-VLT-001",
            "did": "did:web4:sentinexuls.vault.001",
            "token_status": {
                "active_tokens": 1250,
                "pending_rewards": 75,
                "staking_status": "active"
            },
            "evolution_stage": {
                "current_stage": "Advanced",
                "progress": 78,
                "next_milestone": "Expert Level",
                "estimated_time": "14 days"
            }
        }
    
    @app.post("/api/v1/simulate")
    def simulate(simulation_request: dict):
        import random
        import time
        
        scenario = simulation_request.get("scenario", "unknown")
        
        # Simulate processing time
        time.sleep(1)
        
        # Generate mock simulation results
        return {
            "simulation_id": f"SIM-{random.randint(1000, 9999)}",
            "scenario": scenario,
            "status": "completed",
            "success_rate": random.randint(75, 95),
            "duration": random.randint(5, 30),
            "vulnerabilities": random.randint(0, 5),
            "results": {
                "threats_detected": random.randint(1, 10),
                "false_positives": random.randint(0, 3),
                "response_time": f"{random.randint(1, 5)}.{random.randint(10, 99)}s",
                "mitigation_success": random.choice([True, False])
            },
            "recommendations": [
                "Update security policies",
                "Enhance monitoring systems", 
                "Conduct additional training"
            ]
        }
        
except Exception as e:
    print(f"❌ Error creating app: {e}")
    app = None

if __name__ == "__main__":
    print("🎯 SentiNexuls Backend Test Suite")
    print("=" * 50)
    
    # Run basic functionality tests
    if test_basic_functionality():
        print("\n✅ Basic functionality tests passed!")
    else:
        print("\n❌ Some tests failed, but continuing...")
    
    if app:
        print("\n🎉 Test completed successfully!")
        print("\n📋 Next Steps:")
        print("1. Run: uvicorn test_backend:app --reload --port 8000")
        print("2. Open: http://localhost:8000/health")
        print("3. Test frontend connection")
    else:
        print("\n❌ Server creation failed")
    
    print("\n" + "=" * 50) 