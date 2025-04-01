from typing import Dict, List, Optional, Annotated

import mcp.types as types
from pydantic import BaseModel, Field

from anki_mcp.tools.utils import DEFAULT_DECK_NAME, DEFAULT_MODEL_NAME, make_anki_request


class Note(BaseModel):
    name: Annotated[str, Field(description="Name of the note", max_length=64)]
    id: Annotated[int | None, Field(description="Note ID, if the note already exists. If this is populated the existing note will be updated. If this is `None` a new note will be created.")]
    deck: Annotated[str, Field(description="Deck name (optional)", default=DEFAULT_DECK_NAME)]
    model: Annotated[str, Field(description="Model name (optional)", default=DEFAULT_MODEL_NAME)]
    fields: Annotated[Dict[str, str], Field(description="Field values for the note (varies by model)")]
    tags: Annotated[Optional[List[str]], Field(description="Tags to assign to the note (optional)", default=None)]


async def add_or_update_notes(notes: list[Note]) -> list[types.TextContent]:
    """Add one or more notes to Anki.
    
    Notes are processed individually to allow partial success. This means
    if some notes fail to add, others can still be added successfully.
    """
    if not notes:
        raise ValueError("No notes provided")

    response_lines = []
    
    for note in notes:
        if note.id:
            response = await update_note(note)
            response_lines.append(
                f"Updated note '{note.name}' with ID {note.id}"
                if response['success']
                else f"Failed to update note '{note.name}' with ID {note.id}: {response['error']}"
            )
        else:
            response = await add_note(note)
            response_lines.append(
                f"Added note '{note.name}' with ID {response['result']}"
                if response['success']
                else f"Failed to add note '{note.name}': {response['error']}"
            )
    
    return [
        types.TextContent(
            type="text",
            text="\n".join(response_lines)
        )
    ]


async def update_note(note: Note):
    if not note.fields and note.tags is None:
        return {'success': False, 'error': "Either fields or tags must be provided"}
        
    # Prepare the note update data
    note_data = {
        "id": note.id
    }
        
    # Add fields if provided
    if note.fields:
        note_data["fields"] = note.fields
        
    # Add tags if provided
    if note.tags is not None:
        note_data["tags"] = note.tags
        
    # Update the note in Anki
    return await make_anki_request("updateNote", note=note_data)


async def add_note(note: Note):
    if not note.fields:
        return {"success": False, "error": "Note has no fields"}
        
    note_data = {
        "deckName": note.deck,
        "modelName": note.model,
        "fields": note.fields,
        "options": {"allowDuplicate": False},
    }

    # Add tags if provided
    if note.tags is not None:
        note_data["tags"] = note.tags
        
    # Add note to Anki
    result = await make_anki_request("addNote", note=note_data)
        
    return result