# DID resolver for lookups, verifications, and audit trail integrations

import json
from datetime import datetime
from typing import Dict, Optional

def resolve_did(did: str) -> dict:
    """
    Resolve a DID document (simulated for now, in production would query blockchain/DID registry).
    
    Args:
        did (str): The DID to resolve
        
    Returns:
        dict: DID document with authentication and service endpoints
    """
    if not did or not did.startswith("did:"):
        return {"error": "Invalid DID format"}
    
    # Simulate resolving a DID document
    did_document = {
        "@context": [
            "https://w3id.org/did/v1",
            "https://w3id.org/security/v2"
        ],
        "id": did,
        "created": datetime.utcnow().isoformat(),
        "updated": datetime.utcnow().isoformat(),
        "authentication": [
            {
                "id": f"{did}#key-1",
                "type": "Ed25519VerificationKey2020",
                "controller": did,
                "publicKeyBase58": "Fj4A9f8ZmN7K3pQ2vR8sT1uW6xY9zA2bC4dE5fG7hI8jK9lM0nO1pQ2rS3tU4vW5x"
            }
        ],
        "assertionMethod": [
            f"{did}#key-1"
        ],
        "service": [
            {
                "id": f"{did}#audit",
                "type": "AuditTrail",
                "serviceEndpoint": "https://audit.eonicvault.net",
                "description": "SentiNexuls audit trail service"
            },
            {
                "id": f"{did}#vault",
                "type": "VaultService",
                "serviceEndpoint": "https://vault.eonicvault.net",
                "description": "EONIC Vault integration endpoint"
            },
            {
                "id": f"{did}#web4",
                "type": "Web4Dashboard",
                "serviceEndpoint": "https://web4.eonicvault.net",
                "description": "Web4 compliance dashboard"
            }
        ],
        "verificationMethod": [
            {
                "id": f"{did}#key-1",
                "type": "Ed25519VerificationKey2020",
                "controller": did,
                "publicKeyBase58": "Fj4A9f8ZmN7K3pQ2vR8sT1uW6xY9zA2bC4dE5fG7hI8jK9lM0nO1pQ2rS3tU4vW5x"
            }
        ]
    }
    
    return did_document

def verify_did_signature(did: str, message: str, signature: str) -> bool:
    """
    Verify a signature against a DID's public key (simulated).
    
    Args:
        did (str): The DID of the signer
        message (str): The original message
        signature (str): The signature to verify
        
    Returns:
        bool: True if signature is valid, False otherwise
    """
    # In production, this would:
    # 1. Resolve the DID document
    # 2. Extract the public key
    # 3. Verify the signature cryptographically
    
    did_doc = resolve_did(did)
    if "error" in did_doc:
        return False
    
    # Simulate signature verification
    return len(signature) > 10 and signature.startswith("sig_")

def create_audit_entry(did: str, action: str, data: dict) -> dict:
    """
    Create a DID-authenticated audit entry.
    
    Args:
        did (str): The DID performing the action
        action (str): Description of the action
        data (dict): Additional audit data
        
    Returns:
        dict: Audit entry with DID authentication
    """
    audit_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "did": did,
        "action": action,
        "data": data,
        "audit_id": f"audit_{int(datetime.utcnow().timestamp())}",
        "signature": f"sig_{hash(str(data))}"  # Simulated signature
    }
    
    return audit_entry

def get_did_services(did: str, service_type: str = None) -> list:
    """
    Get service endpoints from a DID document.
    
    Args:
        did (str): The DID to query
        service_type (str, optional): Filter by service type
        
    Returns:
        list: List of matching service endpoints
    """
    did_doc = resolve_did(did)
    if "error" in did_doc:
        return []
    
    services = did_doc.get("service", [])
    
    if service_type:
        services = [s for s in services if s.get("type") == service_type]
    
    return services

def validate_did_context(context: dict) -> dict:
    """
    Validate and enhance context with DID information.
    
    Args:
        context (dict): Agent context containing vault information
        
    Returns:
        dict: Enhanced context with DID validation results
    """
    if not context or "vault" not in context:
        return {"valid": False, "error": "No vault context provided"}
    
    vault_did = context["vault"].get("vault_DID")
    if not vault_did:
        return {"valid": False, "error": "No vault DID found"}
    
    did_doc = resolve_did(vault_did)
    if "error" in did_doc:
        return {"valid": False, "error": f"Failed to resolve DID: {did_doc['error']}"}
    
    return {
        "valid": True,
        "did": vault_did,
        "did_document": did_doc,
        "services": get_did_services(vault_did),
        "authentication_methods": len(did_doc.get("authentication", [])),
        "verification_methods": len(did_doc.get("verificationMethod", []))
    }

def get_audit_endpoint(did: str) -> Optional[str]:
    """
    Get the audit trail endpoint for a DID.
    
    Args:
        did (str): The DID to query
        
    Returns:
        str or None: Audit endpoint URL if found
    """
    audit_services = get_did_services(did, "AuditTrail")
    if audit_services:
        return audit_services[0].get("serviceEndpoint")
    return None

def create_did_context(vault_metadata: dict) -> dict:
    """
    Create a comprehensive DID context for agents.
    
    Args:
        vault_metadata (dict): Vault configuration
        
    Returns:
        dict: DID context with resolved document and services
    """
    vault_did = vault_metadata.get("vault_DID")
    if not vault_did:
        return {"error": "No vault DID configured"}
    
    did_doc = resolve_did(vault_did)
    if "error" in did_doc:
        return {"error": f"Failed to resolve vault DID: {did_doc['error']}"}
    
    return {
        "vault_did": vault_did,
        "did_document": did_doc,
        "audit_endpoint": get_audit_endpoint(vault_did),
        "services": get_did_services(vault_did),
        "authentication_ready": len(did_doc.get("authentication", [])) > 0,
        "web4_compliant": any(s.get("type") == "Web4Dashboard" for s in did_doc.get("service", []))
    } 