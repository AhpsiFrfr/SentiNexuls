# Main orchestration entrypoint

import json
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from orchestrator.agent_router import run_agent_pipeline
from sentinexuls_logging.agent_logger import log_event

def load_input(file_path: str = "data/example_input.json") -> dict:
    """
    Load input data from JSON file.
    
    Args:
        file_path (str): Path to the input JSON file
        
    Returns:
        dict: Loaded input data
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            log_event("Main", f"Input data loaded from {file_path}", {"data": data})
            return data
    except Exception as e:
        log_event("Main", f"Failed to load input data from {file_path}", {"error": str(e)})
        return {}

def save_output(report: dict, file_path: str = "outputs/generated_report.md"):
    """
    Save the agent pipeline results to a formatted markdown report.
    
    Args:
        report (dict): Results from the agent pipeline
        file_path (str): Path to save the report
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("# SentiNexuls Agent Report\n\n")
            f.write(f"Generated at: {json.dumps({'timestamp': str(__import__('datetime').datetime.utcnow())})}\n\n")
            
            if "error" in report:
                f.write("## ⚠️ Pipeline Error\n")
                f.write(f"```\n{report['error']}\n```\n\n")
            else:
                for key, value in report.items():
                    if key != "error":
                        f.write(f"## {key.title()} Agent Results\n")
                        f.write("```json\n")
                        f.write(json.dumps(value, indent=2))
                        f.write("\n```\n\n")
        
        log_event("Main", f"Report saved to {file_path}")
        
    except Exception as e:
        log_event("Main", f"Failed to save report to {file_path}", {"error": str(e)})

def main():
    """Main execution function."""
    print("🚀 Starting SentiNexuls Agent Pipeline...")
    
    # 1. Load input data
    log_event("Main", "Starting pipeline execution")
    input_data = load_input()
    
    if not input_data:
        log_event("Main", "No input data available, using default")
        input_data = {"default": True, "message": "No input file found"}
    
    # 2. Execute agent pipeline
    log_event("Main", "Executing agent pipeline", {"input": input_data})
    results = run_agent_pipeline(input_data)
    
    # 3. Log individual agent outputs
    if "error" in results:
        log_event("Main", "Pipeline failed", {"error": results["error"]})
    else:
        for agent, output in results.items():
            if agent != "error":
                log_event(f"{agent.title()}Agent", "Execution complete", data=output)
    
    # 4. Generate and save report
    save_output(results)
    
    if "error" not in results:
        log_event("Main", "Pipeline completed successfully and report generated")
        print("✅ Pipeline execution completed successfully!")
        print(f"📄 Report generated: outputs/generated_report.md")
    else:
        log_event("Main", "Pipeline completed with errors")
        print("❌ Pipeline execution completed with errors!")
        print(f"📄 Error report generated: outputs/generated_report.md")

if __name__ == "__main__":
    main() 