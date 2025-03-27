from typing import Dict, List, Optional
import mcp.types as types

from anki.tools.utils import make_anki_request


async def update_note(note_id: int, fields: Dict[str, str], tags: Optional[List[str]] = None) -> list[types.TextContent]:
    # Prepare the note update data
    note_data = {
        "id": note_id,
        "fields": fields
    }
    
    # Add tags if provided
    if tags is not None:
        note_data["tags"] = tags
    
    result = await make_anki_request("updateNote", note=note_data)
    
    if result["success"]:
        return [
            types.TextContent(
                type="text",
                text=f"Successfully updated note (ID: {note_id}).",
            )
        ]
    else:
        return [
            types.TextContent(
                type="text",
                text=f"Failed to update note: {result['error']}",
            )
        ]