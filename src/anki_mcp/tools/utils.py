import httpx
from typing import Dict, Any

# Constants for Anki Connect
ANKI_CONNECT_URL = "http://localhost:8765"
ANKI_CONNECT_VERSION = 6
DEFAULT_DECK_NAME = "Default"    # Pre-specified deck name
DEFAULT_MODEL_NAME = "Basic"     # Pre-specified model name

async def make_anki_request(action: str, **params) -> Dict[str, Any]:
    """Make a request to the Anki Connect API with proper error handling."""
    request_data = {
        "action": action,
        "version": ANKI_CONNECT_VERSION
    }
    
    if params:
        request_data["params"] = params
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(ANKI_CONNECT_URL, json=request_data, timeout=30.0)
            response.raise_for_status()
            result = response.json()
            
            # Anki Connect returns an object with either a result or error field
            if "error" in result and result["error"]:
                return {"success": False, "error": result["error"]}
            
            return {"success": True, "result": result.get("result")}
        except Exception as e:
            return {"success": False, "error": str(e)}
