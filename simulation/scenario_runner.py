# Runs simulated breach scenarios in GKE

import time
import random
from datetime import datetime
from agents.sim_agent import SimAgent
from logging.agent_logger import log_event

def simulate_breach(vuln_data: dict, metadata: dict) -> dict:
    """
    Simulate a breach scenario using vulnerability data and infrastructure metadata.
    
    Args:
        vuln_data (dict): Vulnerability information from VulnDetectAgent
        metadata (dict): Infrastructure metadata (regions, assets, etc.)
        
    Returns:
        dict: Structured simulation results with timing and status
    """
    sim_agent = SimAgent(agent_id="sim")
    input_payload = {
        "vulnerabilities": vuln_data,
        "target_metadata": metadata
    }

    log_event("SimAgent", "Starting breach simulation", data={
        "target_region": metadata.get("region", "Unknown"),
        "vulnerability_count": len(vuln_data.get("vulnerabilities", [])) if isinstance(vuln_data.get("vulnerabilities"), list) else 1
    })
    
    start_time = time.time()

    # Run the simulation
    result = sim_agent.run(input_payload)

    # Calculate timing metrics
    duration = round(time.time() - start_time, 2)
    
    # Enhance results with simulation metadata
    enhanced_result = {
        **result,
        "simulation_duration_sec": duration,
        "simulation_timestamp": datetime.utcnow().isoformat(),
        "status": "SUCCESS" if result.get("simulation_result") else "INCONCLUSIVE",
        "input_summary": {
            "vulnerabilities_tested": vuln_data,
            "target_infrastructure": metadata
        }
    }

    log_event("SimAgent", "Simulation completed", data=enhanced_result)
    return enhanced_result

def run_advanced_simulation(vuln_data: dict, metadata: dict, scenario_type: str = "standard") -> dict:
    """
    Run an advanced simulation with different scenario types and enhanced metrics.
    
    Args:
        vuln_data (dict): Vulnerability information
        metadata (dict): Infrastructure metadata
        scenario_type (str): Type of simulation (standard, advanced, stress_test)
        
    Returns:
        dict: Comprehensive simulation results
    """
    log_event("SimAgent", f"Starting {scenario_type} simulation scenario")
    
    start_time = time.time()
    
    # Simulate different scenario complexities
    scenario_configs = {
        "standard": {"complexity": 1.0, "detection_delay": 2.0},
        "advanced": {"complexity": 1.5, "detection_delay": 4.0},
        "stress_test": {"complexity": 2.0, "detection_delay": 8.0}
    }
    
    config = scenario_configs.get(scenario_type, scenario_configs["standard"])
    
    # Simulate detection timing based on scenario complexity
    detection_time = random.uniform(1.0, config["detection_delay"])
    time.sleep(min(detection_time, 0.5))  # Simulate processing time (capped for demo)
    
    # Generate realistic simulation metrics
    simulation_metrics = {
        "time_to_detection_sec": round(detection_time, 2),
        "attack_vectors_tested": len(vuln_data.get("vulnerabilities", [])) if isinstance(vuln_data.get("vulnerabilities"), list) else 1,
        "systems_compromised": random.randint(1, len(metadata.get("substation_ids", ["default"]))),
        "mitigation_effectiveness": round(random.uniform(0.7, 0.95), 2),
        "scenario_complexity": config["complexity"]
    }
    
    # Run base simulation
    base_result = simulate_breach(vuln_data, metadata)
    
    # Enhance with advanced metrics
    advanced_result = {
        **base_result,
        "scenario_type": scenario_type,
        "simulation_metrics": simulation_metrics,
        "recommendations": generate_recommendations(simulation_metrics, vuln_data, metadata)
    }
    
    total_duration = round(time.time() - start_time, 2)
    advanced_result["total_simulation_duration_sec"] = total_duration
    
    log_event("SimAgent", f"Advanced {scenario_type} simulation completed", data={
        "duration": total_duration,
        "metrics": simulation_metrics
    })
    
    return advanced_result

def generate_recommendations(metrics: dict, vuln_data: dict, metadata: dict) -> list:
    """
    Generate actionable recommendations based on simulation results.
    
    Args:
        metrics (dict): Simulation metrics
        vuln_data (dict): Vulnerability data
        metadata (dict): Infrastructure metadata
        
    Returns:
        list: List of recommendation strings
    """
    recommendations = []
    
    # Time-based recommendations
    if metrics["time_to_detection_sec"] > 5.0:
        recommendations.append("⚠️ Consider implementing real-time monitoring for faster threat detection")
    
    # Mitigation effectiveness recommendations
    if metrics["mitigation_effectiveness"] < 0.8:
        recommendations.append("🔧 Review and strengthen incident response procedures")
    
    # Infrastructure-specific recommendations
    if metadata.get("region") and "Florida" in metadata.get("region", ""):
        recommendations.append("🌊 Implement hurricane-resilient backup systems for critical infrastructure")
    
    # Vulnerability-specific recommendations
    if "firmware" in str(vuln_data).lower():
        recommendations.append("🔄 Establish automated firmware update procedures")
    
    if not recommendations:
        recommendations.append("✅ Current security posture appears adequate based on simulation")
    
    return recommendations

def run_scenario_suite(vuln_data: dict, metadata: dict) -> dict:
    """
    Run a comprehensive suite of simulation scenarios.
    
    Args:
        vuln_data (dict): Vulnerability information
        metadata (dict): Infrastructure metadata
        
    Returns:
        dict: Results from all simulation scenarios
    """
    log_event("SimAgent", "Starting comprehensive scenario suite")
    
    scenarios = ["standard", "advanced", "stress_test"]
    results = {}
    
    for scenario in scenarios:
        print(f"🔄 Running {scenario} simulation...")
        results[scenario] = run_advanced_simulation(vuln_data, metadata, scenario)
    
    # Generate suite summary
    suite_summary = {
        "scenarios_executed": len(scenarios),
        "total_duration": sum(r["total_simulation_duration_sec"] for r in results.values()),
        "average_detection_time": round(
            sum(r["simulation_metrics"]["time_to_detection_sec"] for r in results.values()) / len(scenarios), 2
        ),
        "overall_status": "COMPREHENSIVE_ANALYSIS_COMPLETE"
    }
    
    final_result = {
        "suite_summary": suite_summary,
        "scenario_results": results,
        "consolidated_recommendations": list(set(
            rec for result in results.values() 
            for rec in result.get("recommendations", [])
        ))
    }
    
    log_event("SimAgent", "Scenario suite completed", data=suite_summary)
    return final_result

# Example direct usage for testing
if __name__ == "__main__":
    print("🚀 Starting SentiNexuls Breach Simulation...")
    
    # Sample data for testing
    dummy_vuln_data = {
        "vulnerabilities": ["CVE-2025-19304"],
        "matched_cve": "CVE-2025-19304", 
        "firmware_affected": "v2.18",
        "severity": "HIGH"
    }
    
    dummy_metadata = {
        "region": "Florida-East", 
        "substation_ids": ["FL-GRID-204", "FL-GRID-207"],
        "firmware_versions": {
            "FL-GRID-204": "v2.18",
            "FL-GRID-207": "v2.19"
        }
    }
    
    # Run single simulation
    print("\n📊 Running single breach simulation...")
    single_result = simulate_breach(dummy_vuln_data, dummy_metadata)
    print(f"Single simulation result: {single_result}")
    
    # Run advanced simulation
    print("\n🔬 Running advanced simulation...")
    advanced_result = run_advanced_simulation(dummy_vuln_data, dummy_metadata, "advanced")
    print(f"Advanced simulation completed in {advanced_result['total_simulation_duration_sec']}s")
    
    # Run full scenario suite
    print("\n🎯 Running comprehensive scenario suite...")
    suite_result = run_scenario_suite(dummy_vuln_data, dummy_metadata)
    print(f"Suite completed: {suite_result['suite_summary']}")
    
    print("\n✅ All simulations completed successfully!") 