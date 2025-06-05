from .base_agent import BaseAgent

class VulnDetectAgent(BaseAgent):
    def run(self, input_data: dict) -> dict:
        """Uses ML to detect vulnerabilities in system design."""
        return {"vulnerabilities": ["Example vulnerability #1"]} 