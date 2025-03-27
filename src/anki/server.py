import asyncio
import httpx
from typing import Dict, Any, List

import mcp.types as types
import mcp.server.stdio
from mcp.server.fastmcp import FastMCP
from pydantic import Field

# Constants for Anki Connect
ANKI_CONNECT_URL = "http://localhost:8765"
ANKI_CONNECT_VERSION = 6
DEFAULT_DECK_NAME = "Default"    # Pre-specified deck name
DEFAULT_MODEL_NAME = "Basic"     # Pre-specified model name

app = FastMCP("anki")


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

@app.tool(name="add-note", description="Add a new note to Anki")
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

@app.tool(name="check-connection", description="Check connection to Anki")
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

@app.tool(name="list-decks", description="List all available decks in Anki")
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

@app.tool(name="get-cards-reviewed", description="Get the number of cards reviewed by day")
async def get_cards_reviewed() -> list[types.TextContent]:
    result = await make_anki_request("getNumCardsReviewedByDay")
    
    if result["success"]:
        review_data = result["result"]
        # Format the review data for better readability
        formatted_data = "\n".join([f"{day}: {count} cards" for day, count in review_data])
        
        return [
            types.TextContent(
                type="text",
                text=f"Cards reviewed by day:\n{formatted_data}",
            )
        ]
    else:
        return [
            types.TextContent(
                type="text",
                text=f"Failed to retrieve review statistics: {result['error']}",
            )
        ]


@app.tool(name="list-models", description="List all available note models in Anki")
async def list_models() -> list[types.TextContent]:
    result = await make_anki_request("modelNames")

    if result["success"]:
        models = result["result"]
        return [
            types.TextContent(
                type="text",
                text=f"Available note models in Anki ({len(models)}):\n" + "\n".join(f"- {model}" for model in models),
            )
        ]
    else:
        return [
            types.TextContent(
                type="text",
                text=f"Failed to retrieve models: {result['error']}",
            )
        ]


@app.tool(name="get-model-fields", description="Get all field names and descriptions for a specific Anki note model")
async def get_model_fields(model_name: str) -> list[types.TextContent]:
    # Get field names
    names_result = await make_anki_request("modelFieldNames", modelName=model_name)

    # Get field descriptions
    descriptions_result = await make_anki_request("modelFieldDescriptions", modelName=model_name)

    if names_result["success"] and descriptions_result["success"]:
        field_names = names_result["result"]
        field_descriptions = descriptions_result["result"]

        # Combine fields and descriptions
        field_info = []
        for i, (name, description) in enumerate(zip(field_names, field_descriptions)):
            desc_text = f": {description}" if description else ""
            field_info.append(f"- {name}{desc_text}")

        return [
            types.TextContent(
                type="text",
                text=f"Fields for model '{model_name}' ({len(field_names)}):\n" + "\n".join(field_info),
            )
        ]
    elif not names_result["success"]:
        return [
            types.TextContent(
                type="text",
                text=f"Failed to retrieve field names: {names_result['error']}",
            )
        ]
    else:
        return [
            types.TextContent(
                type="text",
                text=f"Failed to retrieve field descriptions: {descriptions_result['error']}",
            )
        ]


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')