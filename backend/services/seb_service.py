import hashlib
from fastapi import Request, HTTPException, WebSocket, status

# In a real scenario, this would be loaded from environment variables
EXPECTED_SEB_CONFIG_KEY = "shield-seb-secure-config-key-2026"
EXPECTED_SEB_CONFIG_KEY_HASH = "mock-config-key-hash" # Usually a static hash of the .seb file

class SEBVerificationError(Exception):
    pass

def verify_seb_request_hash(url: str, request_hash: str) -> bool:
    """
    Verifies the Safe Exam Browser RequestHash.
    The RequestHash is a SHA256 hash of the full request URL and the Config Key.
    """
    if not request_hash:
        return False
        
    expected_hash_input = url + EXPECTED_SEB_CONFIG_KEY
    expected_hash = hashlib.sha256(expected_hash_input.encode('utf-8')).hexdigest()
    
    return expected_hash.lower() == request_hash.lower()

def verify_seb_headers_http(request: Request):
    """
    FastAPI dependency to verify SEB headers for HTTP requests.
    """
    # Allow a bypass for development/testing via custom header or if SEB isn't strictly required
    if request.headers.get("X-Bypass-SEB") == "1":
        return True
        
    request_hash = request.headers.get("x-safeexambrowser-requesthash")
    config_key_hash = request.headers.get("x-safeexambrowser-configkeyhash")
    
    if not request_hash and not config_key_hash:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Missing Safe Exam Browser headers. Cryptographic Trust verification failed."
        )
        
    full_url = str(request.url)
    
    # Verify request hash if present
    if request_hash and not verify_seb_request_hash(full_url, request_hash):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Safe Exam Browser RequestHash. Cryptographic Trust verification failed."
        )
        
    # If only config_key_hash is provided, verify it directly
    if not request_hash and config_key_hash != EXPECTED_SEB_CONFIG_KEY_HASH:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Safe Exam Browser ConfigKeyHash. Cryptographic Trust verification failed."
        )
        
    return True

async def verify_seb_headers_ws(websocket: WebSocket) -> bool:
    """
    Verifies SEB headers for WebSocket connections.
    """
    if websocket.headers.get("x-bypass-seb") == "1":
        return True
        
    request_hash = websocket.headers.get("x-safeexambrowser-requesthash")
    config_key_hash = websocket.headers.get("x-safeexambrowser-configkeyhash")
    
    if not request_hash and not config_key_hash:
        return False
        
    full_url = str(websocket.url)
    
    if request_hash and not verify_seb_request_hash(full_url, request_hash):
        return False
        
    if not request_hash and config_key_hash != EXPECTED_SEB_CONFIG_KEY_HASH:
        return False
        
    return True
