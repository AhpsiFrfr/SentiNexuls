from .base_agent import BaseAgent

class IntelSweepAgent(BaseAgent):
    def run(self, input_data: dict, context: dict = None) -> dict:
        """Scans dark web, news, OSINT feeds."""
        # Access vault context if provided
        vault_info = context.get("vault", {}) if context else {}
        vault_id = vault_info.get("vault_id", "UNKNOWN")
        
        # Access DID context for authentication and audit trails
        did_doc = context.get("DID_doc", {}) if context else {}
        did_info = context.get("did_info", {}) if context else {}
        
        result = {
            "intel": "Sample threat intel extracted.",
            "vault_context": vault_id,
            "capabilities_used": vault_info.get("vault_capabilities", [])[:2] if vault_info else []
        }
        
        # Add DID authentication information if available
        if did_doc and "id" in did_doc:
            result["did_authenticated"] = True
            result["vault_did"] = did_doc["id"]
            result["audit_endpoint"] = did_info.get("audit_endpoint")
            
            # Create audit entry for this intelligence gathering
            if "DID-authenticated audits" in vault_info.get("vault_capabilities", []):
                result["audit_entry"] = {
                    "action": "intel_sweep_completed",
                    "did": did_doc["id"],
                    "timestamp": did_doc.get("created"),
                    "authenticated": True
                }
        
        return result 