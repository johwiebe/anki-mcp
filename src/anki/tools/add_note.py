from typing import Dict, Annotated, List
from pydantic import Field, BaseModel
import mcp.types as types

from .utils import make_anki_request, DEFAULT_DECK_NAME, DEFAULT_MODEL_NAME

class Note(BaseModel):
    name: Annotated[str, Field(description="Name of the note", max_length=64)]
    deck: Annotated[str, Field(description="Deck name (optional)", default=DEFAULT_DECK_NAME)]
    model: Annotated[str, Field(description="Model name (optional)", default=DEFAULT_MODEL_NAME)]
    fields: Annotated[Dict[str, str], Field(description="Field values for the note (varies by model)")]


async def add_notes(notes: list[Note]) -> list[types.TextContent]:
    """Add one or more notes to Anki.
    
    Notes are processed individually to allow partial success. This means
    if some notes fail to add, others can still be added successfully.
    """
    if not notes:
        raise ValueError("No notes provided")

    # Track results for each note
    successful_notes = []
    failed_notes = []
    
    for note in notes:
        if not note.fields:
            failed_notes.append((note.name, "Note has no fields"))
            continue
            
        note_data = {
            "deckName": note.deck,
            "modelName": note.model,
            "fields": note.fields,
            "options": {"allowDuplicate": False},
            "tags": []
        }
        
        # Add note to Anki
        result = await make_anki_request("addNote", note=note_data)
        
        if result["success"]:
            successful_notes.append((note.name, result["result"]))  # name, id
        else:
            failed_notes.append((note.name, result["error"]))  # name, error
    
    # Prepare response
    response_lines = []
    
    # Add successful notes to response
    for name, note_id in successful_notes:
        response_lines.append(f"Added note '{name}' with ID: {note_id}")
    
    # Add failed notes to response
    for name, error in failed_notes:
        response_lines.append(f"Failed to add note '{name}': {error}")
    
    # Add summary
    response_lines.append(f"\nSummary: Added {len(successful_notes)} of {len(notes)} notes successfully.")
    
    return [
        types.TextContent(
            type="text",
            text="\n".join(response_lines)
        )
    ]
