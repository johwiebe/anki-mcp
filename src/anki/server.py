import asyncio
import httpx
from typing import Dict, Any, List

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from pydantic import AnyUrl
import mcp.server.stdio

# Constants for Anki Connect
ANKI_CONNECT_URL = "http://localhost:8765"
ANKI_CONNECT_VERSION = 6
DEFAULT_DECK_NAME = "Default"    # Pre-specified deck name
DEFAULT_MODEL_NAME = "Basic"     # Pre-specified model name

# Store added notes to track what we've sent to Anki
notes: dict[str, dict] = {}

server = Server("anki")

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

@server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    """
    List available note resources.
    Each note is exposed as a resource with a custom anki:// URI scheme.
    """
    return [
        types.Resource(
            uri=AnyUrl(f"anki://note/{name}"),
            name=f"Card: {name}",
            description=f"Anki flashcard with front: {note['front'][:30]}...",
            mimeType="text/plain",
        )
        for name, note in notes.items()
    ]

@server.read_resource()
async def handle_read_resource(uri: AnyUrl) -> str:
    """
    Read a specific note's content by its URI.
    """
    if uri.scheme != "anki":
        raise ValueError(f"Unsupported URI scheme: {uri.scheme}")

    name = uri.path
    if name is not None:
        name = name.lstrip("/")
        if name in notes:
            note = notes[name]
            return f"Front: {note['front']}\nBack: {note['back']}"
    raise ValueError(f"Note not found: {name}")

@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    """
    List available prompts.
    """
    return [
        types.Prompt(
            name="create-flashcard",
            description="Creates a new Anki flashcard",
            arguments=[
                types.PromptArgument(
                    name="topic",
                    description="Topic for the flashcard",
                    required=True,
                )
            ],
        )
    ]

@server.get_prompt()
async def handle_get_prompt(
    name: str, arguments: dict[str, str] | None
) -> types.GetPromptResult:
    """
    Generate a prompt for creating flashcards.
    """
    if name != "create-flashcard":
        raise ValueError(f"Unknown prompt: {name}")

    topic = (arguments or {}).get("topic", "")
    
    return types.GetPromptResult(
        description=f"Create an Anki flashcard about {topic}",
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(
                    type="text",
                    text=f"Create a flashcard about {topic}. The flashcard should have a clear question on the front and a concise answer on the back. Make sure the content is factually accurate and educational.",
                ),
            )
        ],
    )

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools for Anki integration.
    """
    return [
        types.Tool(
            name="add-note",
            description="Add a new note to Anki",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Identifier for the note"},
                    "front": {"type": "string", "description": "Content for front of the card"},
                    "back": {"type": "string", "description": "Content for back of the card"},
                    "deck": {"type": "string", "description": "Deck name (optional)"},
                    "model": {"type": "string", "description": "Model name (optional)"},
                },
                "required": ["name", "front", "back"],
            },
        ),
        types.Tool(
            name="check-connection",
            description="Check connection to Anki",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name="list-decks",
            description="List all available decks in Anki",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool execution requests for Anki operations.
    """
    if name == "add-note":
        if not arguments:
            raise ValueError("Missing arguments")

        note_name = arguments.get("name")
        front = arguments.get("front")
        back = arguments.get("back")
        deck = arguments.get("deck", DEFAULT_DECK_NAME)
        model = arguments.get("model", DEFAULT_MODEL_NAME)

        if not note_name or not front or not back:
            raise ValueError("Missing required fields: name, front, and back")

        # Create the note for Anki
        note = {
            "deckName": deck,
            "modelName": model,
            "fields": {
                "Front": front,
                "Back": back
            },
            "options": {
                "allowDuplicate": False
            },
            "tags": []
        }
        
        # Add the note to Anki
        result = await make_anki_request("addNote", note=note)
        
        if result["success"]:
            # Store note info locally for resource listing
            notes[note_name] = {
                "front": front,
                "back": back,
                "deck": deck,
                "model": model,
                "anki_id": result["result"]
            }
            
            # Notify clients that resources have changed
            await server.request_context.session.send_resource_list_changed()
            
            return [
                types.TextContent(
                    type="text",
                    text=f"Successfully added note '{note_name}' to deck '{deck}' with ID: {result['result']}",
                )
            ]
        else:
            return [
                types.TextContent(
                    type="text",
                    text=f"Failed to add note to Anki: {result['error']}",
                )
            ]
    
    elif name == "check-connection":
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
    
    elif name == "list-decks":
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
    
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="anki",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
