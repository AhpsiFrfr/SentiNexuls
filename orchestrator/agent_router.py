# Routes outputs between agents
# SentiNexuls Platform: Integrated Agent Pipeline with Simulation
# -------------------------------------------------------------------
# This file implements the full orchestration layer for the SentiNexuls
# project, including breach simulation as part of the end-to-end pipeline.

import json
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ✅ Imports
from agents.intel_sweep_agent import IntelSweepAgent
from agents.vuln_detect_agent import VulnDetectAgent
from agents.impact_agent import ImpactAgent
from agents.alert_agent import AlertAgent
from simulation.scenario_runner import simulate_breach
from logging.agent_logger import log_event
from config.vault_config import vault_metadata
from utils.vault_interface import initialize_vault, get_vault_context
from utils.did_resolver import resolve_did, create_did_context

def run_agent_pipeline(initial_input: dict) -> dict:
    """
    Runs agents sequentially in a pipeline, passing output from one agent as input to the next.
    Now includes breach simulation as part of the comprehensive analysis.
    
    Args:
        initial_input (dict): Initial data to start the pipeline
        
    Returns:
        dict: Aggregated output from all agents including simulation results
    """
    intel_agent = IntelSweepAgent(agent_id="intel")
    vuln_agent = VulnDetectAgent(agent_id="vuln")
    impact_agent = ImpactAgent(agent_id="impact")
    alert_agent = AlertAgent(agent_id="alert")

    try:
        print("Starting enhanced agent pipeline with simulation...")
        
        # 🏛️ Initialize Vault and log metadata
        vault_init_status = initialize_vault()
        log_event("VaultInit", "Loaded Vault metadata for SentiNexuls", data=vault_metadata)
        print(f"[Vault] Initialized {vault_metadata['vault_id']} with {len(vault_metadata['vault_capabilities'])} capabilities")
        
        # 🆔 Resolve and log DID context
        vault_did = vault_metadata.get("vault_DID")
        if vault_did:
            resolved_did = resolve_did(vault_did)
            log_event("DID", "Resolved Vault DID document", data=resolved_did)
            print(f"[DID] Resolved {vault_did} with {len(resolved_did.get('service', []))} service endpoints")
        
        # Get enhanced vault context with DID information
        vault_context = get_vault_context()
        did_context = create_did_context(vault_metadata)
        if "error" not in did_context:
            vault_context["did_info"] = did_context
        
        # ✅ Step 1: IntelSweepAgent
        print("[Pipeline] Running IntelSweepAgent...")
        log_event("Pipeline", "Starting IntelSweepAgent")
        intel_output = intel_agent.run(initial_input, context=vault_context)
        print(f"Intel Agent completed: {intel_output}")
        
        # ✅ Step 2: VulnDetectAgent
        print("[Pipeline] Running VulnDetectAgent...")
        log_event("Pipeline", "Starting VulnDetectAgent")
        vuln_output = vuln_agent.run(intel_output, context=vault_context)
        print(f"Vuln Agent completed: {vuln_output}")
        
        # ✅ Step 3: ImpactAgent
        print("[Pipeline] Running ImpactAgent...")
        log_event("Pipeline", "Starting ImpactAgent")
        impact_output = impact_agent.run(vuln_output, context=vault_context)
        print(f"Impact Agent completed: {impact_output}")
        
        # 🧪 Step 4: SimAgent (Breach Simulation)
        print("[Pipeline] Running SimAgent for breach simulation...")
        log_event("Pipeline", "Starting breach simulation")
        simulation_output = simulate_breach(
            vuln_data=vuln_output, 
            metadata=initial_input.get("target_metadata", {})
        )
        print(f"Simulation completed: {simulation_output.get('status', 'UNKNOWN')}")
        
        # ✅ Step 5: AlertAgent
        print("[Pipeline] Running AlertAgent...")
        log_event("Pipeline", "Starting AlertAgent")
        alert_output = alert_agent.run(impact_output, context=vault_context)
        print(f"Alert Agent completed: {alert_output}")
        
        print("Enhanced pipeline completed successfully!")
        
        # Return comprehensive results including simulation
        results = {
            "intel": intel_output,
            "vulnerabilities": vuln_output,
            "impact": impact_output,
            "simulation": simulation_output,
            "alert": alert_output
        }
        
        log_event("Pipeline", "Pipeline completed successfully", data={
            "agents_executed": 5,
            "simulation_included": True,
            "simulation_status": simulation_output.get("status", "UNKNOWN")
        })
        
        return results
        
    except Exception as e:
        error_msg = f"Pipeline error: {e}"
        print(error_msg)
        log_event("Pipeline", "Pipeline execution failed", data={"error": str(e)})
        return {"error": str(e)}

def run_pipeline(input_data: dict) -> dict:
    """
    Alias for run_agent_pipeline to maintain compatibility with different naming conventions.
    
    Args:
        input_data (dict): Initial data to start the pipeline
        
    Returns:
        dict: Aggregated output from all agents including simulation results
    """
    return run_agent_pipeline(input_data)

# 🔄 Future Extensions (Next Steps)
# ----------------------------------
# 1. Enhance simulation runner with scenario type selector (stress, advanced, etc.)
# 2. Export full results to outputs/generated_report.md with simulation details
# 3. Integrate alert output into EONIC Vault UI via vault_pylon_api
# 4. Add --simulate CLI flag to optionally trigger simulation
# 5. Build gke_launcher.py to run SimAgent in a real containerized environment
# 6. Expand scenario_runner.py with multiple breach templates
# 7. Add IPFS export or Arweave timestamping for generated reports
# 8. Token-gate access to simulation results in production environment

# 📦 CLI usage (from main.py):
# from orchestrator.agent_router import run_pipeline
# results = run_pipeline(input_data)
# print(json.dumps(results, indent=2)) 