# Interface functions for querying or extending Vault capabilities

from datetime import datetime
from config.vault_config import vault_metadata, update_vault_status

def get_vault_capabilities():
    """
    Get the list of current vault capabilities.
    
    Returns:
        list: List of vault capability strings
    """
    from config.vault_config import vault_metadata
    return vault_metadata.get("vault_capabilities", [])

def has_capability(capability: str) -> bool:
    """
    Check if the vault has a specific capability.
    
    Args:
        capability (str): Capability to check for
        
    Returns:
        bool: True if capability exists, False otherwise
    """
    capabilities = get_vault_capabilities()
    return capability in capabilities

def add_vault_capability(capability: str):
    """
    Add a new capability to the vault.
    
    Args:
        capability (str): New capability to add
    """
    capabilities = get_vault_capabilities()
    if capability not in capabilities:
        capabilities.append(capability)
        update_vault_status({
            "vault_capabilities": capabilities,
            "last_capability_update": datetime.utcnow().isoformat()
        })

def remove_vault_capability(capability: str):
    """
    Remove a capability from the vault.
    
    Args:
        capability (str): Capability to remove
    """
    capabilities = get_vault_capabilities()
    if capability in capabilities:
        capabilities.remove(capability)
        update_vault_status({
            "vault_capabilities": capabilities,
            "last_capability_update": datetime.utcnow().isoformat()
        })

def initialize_vault():
    """
    Initialize the vault with current timestamp and perform startup checks.
    
    Returns:
        dict: Initialization status and metadata
    """
    initialization_time = datetime.utcnow().isoformat()
    
    update_vault_status({
        "initialization_timestamp": initialization_time
    })
    
    # Perform startup checks
    startup_status = {
        "initialized_at": initialization_time,
        "vault_id": vault_metadata.get("vault_id"),
        "capabilities_count": len(get_vault_capabilities()),
        "enico_status": vault_metadata.get("ENICO_status"),
        "dev_eon_linked": vault_metadata.get("DEV_EON_linked"),
        "web4_compliance": vault_metadata.get("web4_compliance"),
        "autonomous_mode": vault_metadata.get("autonomous_mode"),
        "security_level": vault_metadata.get("security_level")
    }
    
    return startup_status

def get_vault_context():
    """
    Get vault context object for passing to agents.
    
    Returns:
        dict: Vault context with essential metadata
    """
    return {
        "vault": vault_metadata.copy(),
        "capabilities": get_vault_capabilities(),
        "vault_id": vault_metadata.get("vault_id"),
        "project_token": vault_metadata.get("project_token"),
        "security_level": vault_metadata.get("security_level"),
        "autonomous_mode": vault_metadata.get("autonomous_mode")
    }

def validate_vault_integrity():
    """
    Validate vault configuration and integrity.
    
    Returns:
        dict: Validation results
    """
    validation_results = {
        "valid": True,
        "issues": [],
        "warnings": []
    }
    
    # Check required fields
    required_fields = ["vault_id", "ENICO_status", "DEV_EON_linked", "web4_compliance"]
    for field in required_fields:
        if field not in vault_metadata or vault_metadata[field] is None:
            validation_results["valid"] = False
            validation_results["issues"].append(f"Missing required field: {field}")
    
    # Check capabilities
    if not get_vault_capabilities():
        validation_results["warnings"].append("No vault capabilities defined")
    
    # Check Web4 compliance
    if not vault_metadata.get("web4_compliance"):
        validation_results["warnings"].append("Web4 compliance not enabled")
    
    return validation_results

def get_vault_stats():
    """
    Get comprehensive vault statistics and status.
    
    Returns:
        dict: Vault statistics
    """
    return {
        "vault_id": vault_metadata.get("vault_id"),
        "status": "ACTIVE" if vault_metadata.get("ENICO_status") == "active" else "INACTIVE",
        "capabilities_count": len(get_vault_capabilities()),
        "capabilities": get_vault_capabilities(),
        "web4_compliant": vault_metadata.get("web4_compliance", False),
        "dev_eon_linked": vault_metadata.get("DEV_EON_linked", False),
        "origin_chain": vault_metadata.get("origin_chain"),
        "project_token": vault_metadata.get("project_token"),
        "security_level": vault_metadata.get("security_level"),
        "autonomous_mode": vault_metadata.get("autonomous_mode"),
        "initialization_timestamp": vault_metadata.get("initialization_timestamp"),
        "last_capability_update": vault_metadata.get("last_capability_update")
    } 