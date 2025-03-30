from typing import Dict, List, Optional, Annotated
from pydantic import Field, BaseModel
import mcp.types as types

from anki_mcp.tools.utils import make_anki_request


class NoteUpdate(BaseModel):
    note_id: Annotated[int, Field(description="ID of the note to update")]
    name: Annotated[str, Field(description="A name to identify this note in the results")]
    fields: Annotated[Optional[Dict[str, str]], Field(description="Field values to update (varies by model)", default=None)]
    tags: Annotated[Optional[List[str]], Field(description="Tags to assign to the note (optional)", default=None)]


async def update_notes(updates: list[NoteUpdate]) -> list[types.TextContent]:
    """Update one or more existing notes in Anki with new field values and/or tags.
    
    Notes are processed individually to allow partial success. This means
    if some notes fail to update, others can still be updated successfully.
    
    Note: The notes must not be open in the Anki browser during update.
    """
    if not updates:
        raise ValueError("No notes provided to update")
    
    # Track results for each note
    successful_updates = []
    failed_updates = []
    
    # Process each note update individually
    for update in updates:
        # Validate input
        if not update.fields and update.tags is None:
            failed_updates.append((update.name, "Either fields or tags must be provided"))
            continue
        
        # Prepare the note update data
        note_data = {
            "id": update.note_id
        }
        
        # Add fields if provided
        if update.fields:
            note_data["fields"] = update.fields
        
        # Add tags if provided
        if update.tags is not None:
            note_data["tags"] = update.tags
        
        # Update the note in Anki
        result = await make_anki_request("updateNote", note=note_data)
        
        if result["success"]:
            successful_updates.append(update.name)
        else:
            failed_updates.append((update.name, result["error"]))
    
    # Prepare response
    response_lines = []
    
    # Add successful updates to response
    for name in successful_updates:
        response_lines.append(f"Updated note '{name}' (ID: {next(u.note_id for u in updates if u.name == name)})")
    
    # Add failed updates to response
    for name, error in failed_updates:
        response_lines.append(f"Failed to update note '{name}': {error}")
    # Add summary
    response_lines.append(f"\nSummary: Updated {len(successful_updates)} of {len(updates)} notes successfully.")
    
    return [
        types.TextContent(
            type="text",
            text="\n".join(response_lines)
        )
    ]