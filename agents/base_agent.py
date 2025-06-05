class BaseAgent:
    def __init__(self, agent_id: str):
        self.agent_id = agent_id

    def run(self, input_data: dict) -> dict:
        """Run the agent with given input and return output."""
        raise NotImplementedError("Subclasses must implement this method.") 