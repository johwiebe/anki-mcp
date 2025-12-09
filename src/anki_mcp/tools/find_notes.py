import mcp.types as types
from .utils import make_anki_request
from datetime import datetime

async def find_notes(query: str, limit: int = 20) -> list[types.TextContent]:
    result = await make_anki_request("notesInfo", query=query)

    if result["success"]:
        notes = result["result"]
        total_count = len(notes)

        if not notes:
            return [
                types.TextContent(
                    type="text",
                    text=f"No notes found matching query: '{query}'",
                )
            ]

        # Apply limit
        limited_notes = notes[:limit]

        notes_info = []
        for note in limited_notes:
            note_id = note["noteId"]
            model_name = note["modelName"]
            tags = ", ".join(note["tags"]) if note["tags"] else "(no tags)"
            
            # Format fields
            fields_text = []
            for field_name, field_data in note["fields"].items():
                field_value = field_data["value"]
                # Truncate very long field values for display
                if len(field_value) > 100:
                    field_value = field_value[:97] + "..."
                fields_text.append(f"  - {field_name}: {field_value}")
            
            # Format modification time
            mod_time = datetime.fromtimestamp(note["mod"]).strftime("%Y-%m-%d %H:%M:%S")
            
            note_text = (
                f"Note ID: {note_id}\n"
                f"Model: {model_name}\n"
                f"Tags: {tags}\n"
                f"Modified: {mod_time}\n"
                f"Fields:\n" + "\n".join(fields_text) + "\n"
            )
            notes_info.append(note_text)
        
        # Build header message
        if total_count > limit:
            header = f"Showing {len(limited_notes)} of {total_count} notes matching query: '{query}' (use a more specific query or increase limit to see more)"
        else:
            header = f"Found {total_count} notes matching query: '{query}'"

        return [
            types.TextContent(
                type="text",
                text=header + "\n\n" + "\n\n".join(notes_info),
            )
        ]
    else:
        return [
            types.TextContent(
                type="text",
                text=f"Failed to retrieve notes: {result['error']}",
            )
        ]