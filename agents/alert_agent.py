from .base_agent import BaseAgent

class AlertAgent(BaseAgent):
    def run(self, input_data: dict, context: dict = None) -> dict:
        """Creates alerts and dispatches notifications."""
        # Access vault context if provided
        vault_info = context.get("vault", {}) if context else {}
        
        alert_channels = ["Slack", "Vault UI"]
        if vault_info.get("DEV_EON_linked"):
            alert_channels.append("DEV-EON Network")
        if vault_info.get("web4_compliance"):
            alert_channels.append("Web4 Dashboard")
            
        return {
            "alert_status": f"Dispatched to {', '.join(alert_channels)}",
            "vault_integration": True,
            "enico_status": vault_info.get("ENICO_status", "unknown"),
            "token_auth": "token-auth infrastructure" in vault_info.get("vault_capabilities", [])
        } 