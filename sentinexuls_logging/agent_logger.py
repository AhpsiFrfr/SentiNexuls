# Handles smart-contract-compatible logging

import os
import json
from datetime import datetime
from pathlib import Path

LOG_FILE_PATH = Path("logs/agent_log.jsonl")
LOG_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)

def log_event(agent_name: str, event: str, data: dict = None, on_chain: bool = False):
    """
    Log agent events to multiple destinations: console, local file, and optionally blockchain.
    
    Args:
        agent_name (str): Name of the agent generating the log
        event (str): Description of the event being logged
        data (dict, optional): Additional data to include with the log entry
        on_chain (bool, optional): Whether to also log to blockchain smart contract
    """
    timestamp = datetime.utcnow().isoformat()
    log_entry = {
        "timestamp": timestamp,
        "agent": agent_name,
        "event": event,
        "data": data or {}
    }

    # 1. Console logging
    print(f"[{timestamp}] {agent_name} :: {event}")
    if data:
        print(f"    Data: {json.dumps(data, indent=2)}")

    # 2. Local file logging (JSONL format)
    try:
        with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        print(f"⚠️ Failed to write to log file: {e}")

    # 3. Blockchain log (optional)
    if on_chain:
        try:
            from services.smart_contract import publish_log
            publish_log(log_entry)
            print(f"✅ Log entry published to blockchain")
        except ImportError:
            print("⚠️ smart_contract module not found. Skipping on-chain logging.")
        except Exception as e:
            print(f"⚠️ Failed to publish to blockchain: {e}")

def log_agent_start(agent_name: str, input_data: dict = None):
    """Log when an agent starts processing."""
    log_event(agent_name, "Agent started", {"input": input_data})

def log_agent_complete(agent_name: str, output_data: dict = None, execution_time: float = None):
    """Log when an agent completes processing."""
    data = {"output": output_data}
    if execution_time:
        data["execution_time_seconds"] = execution_time
    log_event(agent_name, "Agent completed", data)

def log_agent_error(agent_name: str, error: str, input_data: dict = None):
    """Log when an agent encounters an error."""
    log_event(agent_name, "Agent error", {"error": error, "input": input_data}, on_chain=True)

def log_pipeline_event(event: str, data: dict = None, on_chain: bool = False):
    """Log pipeline-level events."""
    log_event("Pipeline", event, data, on_chain)

# Usage Examples:
# log_event("IntelSweepAgent", "Scan complete", {"threats_found": 3}, on_chain=True)
# log_agent_start("VulnDetectAgent", {"intel_data": "..."})
# log_agent_complete("ImpactAgent", {"impact_score": 92.5}, 2.3)
# log_agent_error("AlertAgent", "Failed to send notification", {"alert_data": "..."}) 