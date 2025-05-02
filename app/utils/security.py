import hashlib
from typing import Dict, Any

def encrypt_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Securely hash sensitive data (mock encryption for hackathon)"""
    encrypted = data.copy()
    if "account_number" in encrypted:
        encrypted["account_number"] = hashlib.sha256(
            str(encrypted["account_number"]).encode()
        ).hexdigest()
    return encrypted