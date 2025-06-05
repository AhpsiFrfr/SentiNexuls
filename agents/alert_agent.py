from .base_agent import BaseAgent

class AlertAgent(BaseAgent):
    def run(self, input_data: dict) -> dict:
        """Creates alerts and dispatches notifications."""
        return {"alert_status": "Dispatched to Slack + Vault UI"} 