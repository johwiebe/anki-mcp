import mcp.types as types

from .utils import make_anki_request

async def check_connection() -> list[types.TextContent]:
    result = await make_anki_request("version")
    
    if result["success"]:
        return [
            types.TextContent(
                type="text",
                text=f"Connected to AnkiConnect v{result['result']}",
            )
        ]
    else:
        return [
            types.TextContent(
                type="text",
                text=f"Failed to connect to AnkiConnect: {result['error']}",
            )
        ]
