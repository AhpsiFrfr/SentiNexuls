"""
SentiNexuls API Router
Modular API endpoints for the SentiNexuls platform with comprehensive data endpoints.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json
import sys
import os
import asyncio

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orchestrator.agent_router import run_agent_pipeline
from simulation.scenario_runner import simulate_breach, run_advanced_simulation, run_scenario_suite
from config.vault_config import vault_metadata, get_vault_metadata, is_vault_active
from logging.agent_logger import log_event

# Initialize router
router = APIRouter()

# Pydantic models for request/response validation
class SimulationRequest(BaseModel):
    vuln_data: Dict[str, Any]
    target_metadata: Dict[str, Any]
    scenario_type: Optional[str] = "standard"
    run_full_suite: Optional[bool] = False

class SimulationResponse(BaseModel):
    status: str
    simulation_id: str
    results: Dict[str, Any]
    timestamp: str

# Mock data generators for realistic responses
def generate_mock_intel_feed():
    """Generate realistic mock intelligence feed data."""
    return {
        "dark_web_chatter": [
            {
                "id": "dw_001",
                "source": "ExploitForum123",
                "post_title": "New SCADA zero-day - affecting regional grids",
                "content_snippet": "Confirmed working payload for firmware v2.18 on Siemens substations. DM for sample.",
                "threat_level": "HIGH",
                "timestamp": "2025-06-05T08:30:00Z",
                "confidence": 0.87,
                "tags": ["SCADA", "zero-day", "Siemens", "firmware"]
            },
            {
                "id": "dw_002", 
                "source": "ZeroLeakz",
                "post_title": "Selling access to energy control panels (East Coast)",
                "content_snippet": "Got creds for legacy HMIs in Florida. $500 per login.",
                "threat_level": "CRITICAL",
                "timestamp": "2025-06-05T07:15:00Z",
                "confidence": 0.92,
                "tags": ["HMI", "credentials", "Florida", "energy"]
            },
            {
                "id": "dw_003",
                "source": "CyberUnderground",
                "post_title": "Grid vulnerability scanner - automated tool",
                "content_snippet": "New tool for scanning power grid vulnerabilities. Works on most legacy systems.",
                "threat_level": "MEDIUM",
                "timestamp": "2025-06-05T06:45:00Z",
                "confidence": 0.73,
                "tags": ["scanner", "grid", "automation", "legacy"]
            }
        ],
        "osint_articles": [
            {
                "id": "osint_001",
                "headline": "Outdated control firmware still used in 30% of US substations",
                "source": "TechSec Weekly",
                "published": "2025-05-28T00:00:00Z",
                "summary": "Security researchers find widespread use of vulnerable firmware versions across critical infrastructure.",
                "url": "https://techsec.example.com/articles/firmware-vulnerabilities",
                "relevance_score": 0.94,
                "impact_assessment": "HIGH"
            },
            {
                "id": "osint_002",
                "headline": "New cybersecurity framework for energy sector released",
                "source": "Energy Security Today",
                "published": "2025-06-01T00:00:00Z",
                "summary": "Department of Energy releases updated cybersecurity guidelines for critical infrastructure protection.",
                "url": "https://energysec.example.com/framework-2025",
                "relevance_score": 0.81,
                "impact_assessment": "MEDIUM"
            }
        ],
        "cve_alerts": [
            {
                "cve_id": "CVE-2025-19304",
                "title": "Siemens SCADA Firmware Remote Code Execution",
                "severity": "CRITICAL",
                "cvss_score": 9.8,
                "published": "2025-06-01T00:00:00Z",
                "description": "Remote code execution vulnerability in Siemens SCADA firmware versions 2.18 and earlier.",
                "affected_products": ["Siemens SCADA v2.18", "Siemens SCADA v2.17"],
                "mitigation": "Upgrade to firmware version 2.19 or later",
                "exploit_available": True,
                "in_the_wild": True
            },
            {
                "cve_id": "CVE-2025-19305",
                "title": "Industrial HMI Authentication Bypass",
                "severity": "HIGH",
                "cvss_score": 8.1,
                "published": "2025-05-30T00:00:00Z",
                "description": "Authentication bypass vulnerability in industrial HMI systems.",
                "affected_products": ["Generic HMI Systems", "Legacy Control Panels"],
                "mitigation": "Implement additional authentication layers",
                "exploit_available": False,
                "in_the_wild": False
            }
        ],
        "regulatory_alerts": [
            {
                "id": "reg_001",
                "title": "NERC Critical Update",
                "summary": "All regional energy providers must patch CVE-2025-19304 within 30 days or risk compliance fines.",
                "published": "2025-06-01T00:00:00Z",
                "deadline": "2025-07-01T00:00:00Z",
                "compliance_level": "MANDATORY",
                "fine_amount": "$50,000 - $500,000"
            }
        ],
        "last_updated": datetime.utcnow().isoformat(),
        "total_threats": 7,
        "critical_threats": 2,
        "high_threats": 2,
        "medium_threats": 3
    }

def generate_mock_agent_status():
    """Generate realistic mock agent health and status data."""
    return {
        "agents": [
            {
                "agent_id": "intel_sweep",
                "name": "IntelSweepAgent",
                "status": "ACTIVE",
                "health": "HEALTHY",
                "last_execution": "2025-06-05T09:15:00Z",
                "execution_count": 1247,
                "success_rate": 0.987,
                "average_runtime": 2.3,
                "current_task": "Scanning dark web forums",
                "vault_enhanced": True,
                "capabilities_used": ["sentient_agents", "self-evolving defenses"],
                "retraining_status": {
                    "last_retrain": "2025-06-04T12:00:00Z",
                    "next_scheduled": "2025-06-06T12:00:00Z",
                    "model_version": "v2.1.3",
                    "accuracy_improvement": 0.023
                }
            },
            {
                "agent_id": "vuln_detect",
                "name": "VulnDetectAgent", 
                "status": "ACTIVE",
                "health": "HEALTHY",
                "last_execution": "2025-06-05T09:14:30Z",
                "execution_count": 892,
                "success_rate": 0.994,
                "average_runtime": 1.8,
                "current_task": "CVE correlation analysis",
                "vault_enhanced": True,
                "capabilities_used": ["token-auth infrastructure"],
                "retraining_status": {
                    "last_retrain": "2025-06-03T18:00:00Z",
                    "next_scheduled": "2025-06-07T18:00:00Z",
                    "model_version": "v1.9.7",
                    "accuracy_improvement": 0.031
                }
            },
            {
                "agent_id": "impact_assess",
                "name": "ImpactAgent",
                "status": "ACTIVE", 
                "health": "HEALTHY",
                "last_execution": "2025-06-05T09:14:45Z",
                "execution_count": 634,
                "success_rate": 0.991,
                "average_runtime": 3.1,
                "current_task": "Infrastructure impact modeling",
                "vault_enhanced": True,
                "capabilities_used": ["self-evolving defenses", "DID-authenticated audits"],
                "retraining_status": {
                    "last_retrain": "2025-06-04T06:00:00Z",
                    "next_scheduled": "2025-06-08T06:00:00Z",
                    "model_version": "v1.7.2",
                    "accuracy_improvement": 0.018
                }
            },
            {
                "agent_id": "sim_agent",
                "name": "SimAgent",
                "status": "ACTIVE",
                "health": "HEALTHY", 
                "last_execution": "2025-06-05T09:13:20Z",
                "execution_count": 423,
                "success_rate": 0.989,
                "average_runtime": 4.7,
                "current_task": "Breach scenario simulation",
                "vault_enhanced": False,
                "capabilities_used": ["custom breach rituals"],
                "retraining_status": {
                    "last_retrain": "2025-06-02T14:00:00Z",
                    "next_scheduled": "2025-06-09T14:00:00Z",
                    "model_version": "v1.5.1",
                    "accuracy_improvement": 0.027
                }
            },
            {
                "agent_id": "alert_dispatch",
                "name": "AlertAgent",
                "status": "ACTIVE",
                "health": "HEALTHY",
                "last_execution": "2025-06-05T09:15:10Z",
                "execution_count": 1156,
                "success_rate": 0.998,
                "average_runtime": 0.9,
                "current_task": "Alert distribution",
                "vault_enhanced": True,
                "capabilities_used": ["token-auth infrastructure", "DID-authenticated audits"],
                "retraining_status": {
                    "last_retrain": "2025-06-05T02:00:00Z",
                    "next_scheduled": "2025-06-10T02:00:00Z",
                    "model_version": "v2.0.1",
                    "accuracy_improvement": 0.012
                }
            }
        ],
        "system_health": {
            "overall_status": "OPERATIONAL",
            "active_agents": 5,
            "total_agents": 5,
            "system_uptime": "99.97%",
            "last_system_restart": "2025-06-01T00:00:00Z",
            "vault_integration": "ACTIVE",
            "pipeline_throughput": "847 ops/hour"
        },
        "performance_metrics": {
            "total_executions_today": 3352,
            "average_pipeline_time": 12.8,
            "success_rate_overall": 0.992,
            "threats_detected_today": 23,
            "simulations_run_today": 8
        }
    }

def generate_mock_alerts():
    """Generate realistic mock alert and impact assessment data."""
    return {
        "recent_alerts": [
            {
                "alert_id": "ALT-2025-001247",
                "timestamp": "2025-06-05T09:15:00Z",
                "severity": "CRITICAL",
                "title": "Active Exploit Detected - CVE-2025-19304",
                "description": "Confirmed exploitation attempt targeting Siemens SCADA firmware v2.18 in Florida-East region",
                "affected_systems": ["FL-GRID-204", "FL-GRID-207"],
                "impact_score": 92.5,
                "status": "ACTIVE",
                "response_actions": [
                    "Automated isolation of affected substations",
                    "Emergency patch deployment initiated",
                    "Incident response team notified"
                ],
                "vault_integration": True,
                "enico_status": "ESCALATED",
                "dispatched_to": ["Slack", "Vault UI", "DEV-EON Network", "Web4 Dashboard"]
            },
            {
                "alert_id": "ALT-2025-001246",
                "timestamp": "2025-06-05T08:45:00Z",
                "severity": "HIGH",
                "title": "Suspicious Dark Web Activity",
                "description": "Increased chatter about energy sector vulnerabilities on monitored forums",
                "affected_systems": ["Monitoring Systems"],
                "impact_score": 67.3,
                "status": "MONITORING",
                "response_actions": [
                    "Enhanced monitoring activated",
                    "Threat intelligence correlation in progress"
                ],
                "vault_integration": True,
                "enico_status": "ACTIVE",
                "dispatched_to": ["Slack", "Vault UI"]
            },
            {
                "alert_id": "ALT-2025-001245",
                "timestamp": "2025-06-05T07:30:00Z",
                "severity": "MEDIUM",
                "title": "Firmware Version Mismatch Detected",
                "description": "Legacy firmware versions detected in 3 substations",
                "affected_systems": ["FL-GRID-201", "FL-GRID-203", "FL-GRID-209"],
                "impact_score": 45.8,
                "status": "RESOLVED",
                "response_actions": [
                    "Maintenance window scheduled",
                    "Firmware update packages prepared"
                ],
                "vault_integration": True,
                "enico_status": "COMPLETED",
                "dispatched_to": ["Vault UI", "Web4 Dashboard"]
            }
        ],
        "impact_assessments": [
            {
                "assessment_id": "IMP-2025-0089",
                "timestamp": "2025-06-05T09:10:00Z",
                "threat_source": "CVE-2025-19304",
                "overall_impact_score": 92.5,
                "affected_zones": ["Grid A", "Grid B"],
                "potential_outage_duration": "2-4 hours",
                "estimated_affected_customers": 125000,
                "financial_impact": "$2.3M - $4.7M",
                "mitigation_effectiveness": 0.87,
                "vault_mitigation": True,
                "recommendations": [
                    "Immediate firmware patching required",
                    "Implement network segmentation",
                    "Enhance monitoring on legacy systems"
                ]
            },
            {
                "assessment_id": "IMP-2025-0088",
                "timestamp": "2025-06-05T06:15:00Z",
                "threat_source": "Dark Web Intelligence",
                "overall_impact_score": 67.3,
                "affected_zones": ["Grid C"],
                "potential_outage_duration": "30 minutes - 1 hour",
                "estimated_affected_customers": 45000,
                "financial_impact": "$500K - $1.2M",
                "mitigation_effectiveness": 0.94,
                "vault_mitigation": True,
                "recommendations": [
                    "Increase security monitoring",
                    "Review access controls",
                    "Update incident response procedures"
                ]
            }
        ],
        "alert_statistics": {
            "total_alerts_today": 23,
            "critical_alerts": 3,
            "high_alerts": 7,
            "medium_alerts": 9,
            "low_alerts": 4,
            "resolved_alerts": 18,
            "active_alerts": 5,
            "average_response_time": "4.2 minutes",
            "vault_integration_rate": 1.0
        }
    }

# API Endpoints

@router.get("/dashboard")
async def get_dashboard():
    """
    Returns live ENICO status and agent overview for the main dashboard.
    """
    try:
        vault_data = get_vault_metadata()
        agent_data = generate_mock_agent_status()
        
        dashboard_data = {
            "enico_status": {
                "status": vault_data.get("ENICO_status", "active"),
                "vault_id": vault_data.get("vault_id"),
                "dev_eon_linked": vault_data.get("DEV_EON_linked", True),
                "web4_compliance": vault_data.get("web4_compliance", True),
                "last_update": datetime.utcnow().isoformat(),
                "autonomous_mode": vault_data.get("autonomous_mode", True)
            },
            "agent_overview": {
                "total_agents": len(agent_data["agents"]),
                "active_agents": len([a for a in agent_data["agents"] if a["status"] == "ACTIVE"]),
                "system_health": agent_data["system_health"]["overall_status"],
                "vault_enhanced_agents": len([a for a in agent_data["agents"] if a["vault_enhanced"]]),
                "pipeline_throughput": agent_data["system_health"]["pipeline_throughput"]
            },
            "threat_summary": {
                "active_threats": 5,
                "critical_alerts": 3,
                "simulations_today": 8,
                "last_breach_simulation": "2025-06-05T09:13:20Z"
            },
            "system_metrics": {
                "uptime": agent_data["system_health"]["system_uptime"],
                "success_rate": agent_data["performance_metrics"]["success_rate_overall"],
                "executions_today": agent_data["performance_metrics"]["total_executions_today"],
                "average_response_time": "4.2 seconds"
            }
        }
        
        log_event("API", "Dashboard data requested", data={"endpoint": "/dashboard"})
        return dashboard_data
        
    except Exception as e:
        log_event("API", "Dashboard error", data={"error": str(e)})
        raise HTTPException(status_code=500, detail=f"Dashboard error: {str(e)}")

@router.get("/intel-feed")
async def get_intel_feed():
    """
    Returns parsed dark web, OSINT, and CVE alerts for the intelligence feed.
    """
    try:
        intel_data = generate_mock_intel_feed()
        
        log_event("API", "Intel feed requested", data={
            "endpoint": "/intel-feed",
            "total_threats": intel_data["total_threats"]
        })
        
        return intel_data
        
    except Exception as e:
        log_event("API", "Intel feed error", data={"error": str(e)})
        raise HTTPException(status_code=500, detail=f"Intel feed error: {str(e)}")

@router.post("/simulate")
async def run_simulation(request: SimulationRequest, background_tasks: BackgroundTasks):
    """
    Accepts POST with payload and runs simulation via scenario_runner.py.
    """
    try:
        simulation_id = f"SIM-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"
        
        log_event("API", "Simulation requested", data={
            "simulation_id": simulation_id,
            "scenario_type": request.scenario_type,
            "full_suite": request.run_full_suite
        })
        
        # Run simulation based on request parameters
        if request.run_full_suite:
            # Run comprehensive scenario suite
            results = run_scenario_suite(request.vuln_data, request.target_metadata)
            simulation_type = "comprehensive_suite"
        elif request.scenario_type in ["standard", "advanced", "stress_test"]:
            # Run advanced simulation with specific scenario
            results = run_advanced_simulation(
                request.vuln_data, 
                request.target_metadata, 
                request.scenario_type
            )
            simulation_type = f"advanced_{request.scenario_type}"
        else:
            # Run basic simulation
            results = simulate_breach(request.vuln_data, request.target_metadata)
            simulation_type = "basic"
        
        response_data = {
            "status": "SUCCESS",
            "simulation_id": simulation_id,
            "simulation_type": simulation_type,
            "results": results,
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": {
                "vuln_count": len(request.vuln_data.get("vulnerabilities", [])) if isinstance(request.vuln_data.get("vulnerabilities"), list) else 1,
                "target_region": request.target_metadata.get("region", "Unknown"),
                "execution_time": results.get("simulation_duration_sec", 0)
            }
        }
        
        log_event("API", "Simulation completed", data={
            "simulation_id": simulation_id,
            "status": results.get("status", "UNKNOWN"),
            "duration": results.get("simulation_duration_sec", 0)
        })
        
        return response_data
        
    except Exception as e:
        log_event("API", "Simulation error", data={"error": str(e)})
        raise HTTPException(status_code=500, detail=f"Simulation error: {str(e)}")

@router.get("/agents")
async def get_agents():
    """
    Returns agent health, retraining status, and performance metrics.
    """
    try:
        agent_data = generate_mock_agent_status()
        
        log_event("API", "Agent status requested", data={
            "endpoint": "/agents",
            "active_agents": agent_data["system_health"]["active_agents"]
        })
        
        return agent_data
        
    except Exception as e:
        log_event("API", "Agent status error", data={"error": str(e)})
        raise HTTPException(status_code=500, detail=f"Agent status error: {str(e)}")

@router.get("/alerts")
async def get_alerts():
    """
    Returns recent impact assessments and alert logs.
    """
    try:
        alert_data = generate_mock_alerts()
        
        log_event("API", "Alerts requested", data={
            "endpoint": "/alerts",
            "total_alerts": alert_data["alert_statistics"]["total_alerts_today"],
            "active_alerts": alert_data["alert_statistics"]["active_alerts"]
        })
        
        return alert_data
        
    except Exception as e:
        log_event("API", "Alerts error", data={"error": str(e)})
        raise HTTPException(status_code=500, detail=f"Alerts error: {str(e)}")

@router.get("/vault-settings")
async def get_vault_settings():
    """
    Returns current Vault ID, DID, token status, and evolution stage.
    """
    try:
        vault_data = get_vault_metadata()
        vault_active = is_vault_active()
        
        vault_settings = {
            "vault_info": {
                "vault_id": vault_data.get("vault_id"),
                "vault_did": vault_data.get("vault_DID"),
                "project_token": vault_data.get("project_token"),
                "vault_version": vault_data.get("vault_version"),
                "origin_chain": vault_data.get("origin_chain")
            },
            "status": {
                "enico_status": vault_data.get("ENICO_status"),
                "dev_eon_linked": vault_data.get("DEV_EON_linked"),
                "web4_compliance": vault_data.get("web4_compliance"),
                "vault_active": vault_active,
                "autonomous_mode": vault_data.get("autonomous_mode"),
                "security_level": vault_data.get("security_level")
            },
            "capabilities": {
                "available_capabilities": vault_data.get("vault_capabilities", []),
                "total_capabilities": len(vault_data.get("vault_capabilities", [])),
                "last_capability_update": vault_data.get("last_capability_update"),
                "evolution_stage": "ADVANCED" if len(vault_data.get("vault_capabilities", [])) >= 5 else "BASIC"
            },
            "token_status": {
                "token_symbol": vault_data.get("project_token"),
                "auth_infrastructure": "token-auth infrastructure" in vault_data.get("vault_capabilities", []),
                "did_authenticated_audits": "DID-authenticated audits" in vault_data.get("vault_capabilities", []),
                "last_auth_check": datetime.utcnow().isoformat()
            },
            "integration_status": {
                "vault_initialization": vault_data.get("initialization_timestamp"),
                "services_connected": [
                    "SentiNexuls Platform",
                    "EONIC Vault",
                    "DEV-EON Network",
                    "Web4 Dashboard"
                ],
                "api_endpoints_active": 6,
                "last_health_check": datetime.utcnow().isoformat()
            }
        }
        
        log_event("API", "Vault settings requested", data={
            "endpoint": "/vault-settings",
            "vault_id": vault_data.get("vault_id"),
            "vault_active": vault_active
        })
        
        return vault_settings
        
    except Exception as e:
        log_event("API", "Vault settings error", data={"error": str(e)})
        raise HTTPException(status_code=500, detail=f"Vault settings error: {str(e)}")

# Additional utility endpoints

@router.get("/system/status")
async def get_system_status():
    """
    Returns comprehensive system status for monitoring and debugging.
    """
    try:
        vault_data = get_vault_metadata()
        
        system_status = {
            "api_version": "1.0.0",
            "system_time": datetime.utcnow().isoformat(),
            "vault_integration": is_vault_active(),
            "available_endpoints": [
                "/dashboard",
                "/intel-feed", 
                "/simulate",
                "/agents",
                "/alerts",
                "/vault-settings"
            ],
            "system_health": "OPERATIONAL",
            "last_restart": "2025-06-05T00:00:00Z"
        }
        
        return system_status
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"System status error: {str(e)}")

@router.post("/pipeline/execute")
async def execute_pipeline(input_data: Dict[str, Any]):
    """
    Execute the full agent pipeline with custom input data.
    """
    try:
        log_event("API", "Pipeline execution requested", data={"endpoint": "/pipeline/execute"})
        
        # Execute the agent pipeline
        results = run_agent_pipeline(input_data)
        
        response = {
            "status": "SUCCESS" if "error" not in results else "ERROR",
            "execution_id": f"PIPE-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}",
            "results": results,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        log_event("API", "Pipeline execution completed", data={
            "status": response["status"],
            "execution_id": response["execution_id"]
        })
        
        return response
        
    except Exception as e:
        log_event("API", "Pipeline execution error", data={"error": str(e)})
        raise HTTPException(status_code=500, detail=f"Pipeline execution error: {str(e)}") 