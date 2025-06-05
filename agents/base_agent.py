class BaseAgent:
    def __init__(self, agent_id: str):
        self.agent_id = agent_id

    def run(self, input_data: dict, context: dict = None) -> dict:
        """Run the agent with given input and return output."""
        # Enhance context with DID document if vault context is provided
        if context and "vault" in context:
            try:
                from utils.did_resolver import resolve_did
                vault_did = context["vault"].get("vault_DID")
                if vault_did:
                    context["DID_doc"] = resolve_did(vault_did)
            except ImportError:
                # DID resolver not available, continue without DID context
                pass
        
        raise NotImplementedError("Subclasses must implement this method.") 