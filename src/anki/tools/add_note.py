from typing import Dict
from pydantic import Field
import mcp.types as types

from .utils import make_anki_request, DEFAULT_DECK_NAME, DEFAULT_MODEL_NAME

async def add_note(
    note_name: str = Field(description="Identifier for the note"),
    fields: Dict[str, str] = Field(description="Field values for the note (varies by model)"),
    deck: str = Field(description="Deck name (optional)", default=DEFAULT_DECK_NAME),
    model: str = Field(description="Model name (optional)", default=DEFAULT_MODEL_NAME)
) -> list[types.TextContent]:
    if not note_name or not fields:
        raise ValueError("Missing required fields: name and fields")

    # Create the note for Anki
    note = {
        "deckName": deck,
        "modelName": model,
        "fields": fields,
        "options": {
            "allowDuplicate": False
        },
        "tags": []
    }
    
    # Add the note to Anki
    result = await make_anki_request("addNote", note=note)
    
    if result["success"]:
        return [
            types.TextContent(
                type="text",
                text=f"Successfully added note to deck '{deck}' with ID: {result['result']}",
            )
        ]
    else:
        return [
            types.TextContent(
                type="text",
                text=f"Failed to add note to Anki: {result['error']}",
            )
        ]
