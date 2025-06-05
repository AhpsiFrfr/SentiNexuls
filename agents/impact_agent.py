from .base_agent import BaseAgent

class ImpactAgent(BaseAgent):
    def run(self, input_data: dict, context: dict = None) -> dict:
        """Estimates the potential impact of a detected threat."""
        # Access vault context if provided
        vault_info = context.get("vault", {}) if context else {}
        
        # Enhance impact assessment with vault capabilities
        base_score = 92.5
        if vault_info.get("autonomous_mode"):
            base_score *= 0.85  # Autonomous mode reduces impact through faster response
            
        return {
            "impact_score": base_score,
            "affected_zones": ["Grid A", "Grid B"],
            "vault_mitigation": vault_info.get("autonomous_mode", False),
            "project_token": vault_info.get("project_token", "N/A")
        } 