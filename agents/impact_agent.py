from .base_agent import BaseAgent

class ImpactAgent(BaseAgent):
    def run(self, input_data: dict) -> dict:
        """Estimates the potential impact of a detected threat."""
        return {"impact_score": 92.5, "affected_zones": ["Grid A", "Grid B"]} 