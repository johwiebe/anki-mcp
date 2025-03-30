import mcp.types as types

from .utils import make_anki_request

async def list_decks() -> list[types.TextContent]:
    result = await make_anki_request("deckNames")

    if result["success"]:
        decks = result["result"]
        return [
            types.TextContent(
                type="text",
                text=f"Available decks in Anki ({len(decks)}):\n" + "\n".join(f"- {deck}" for deck in decks),
            )
        ]
    else:
        return [
            types.TextContent(
                type="text",
                text=f"Failed to retrieve decks: {result['error']}",
            )
        ]
