import mcp.server.stdio
from mcp.server.fastmcp import FastMCP

# Import all tools
from .tools import (
    add_note, 
    check_connection, 
    list_decks, 
    get_cards_reviewed,
    list_models,
    get_model_fields
)

app = FastMCP("anki")

# Register tools with the app
app.tool(name="add-note", description="Add a new note to Anki")(add_note)
app.tool(name="check-connection", description="Check connection to Anki")(check_connection)
app.tool(name="list-decks", description="List all available decks in Anki")(list_decks)
app.tool(name="get-cards-reviewed", description="Get the number of cards reviewed by day")(get_cards_reviewed)
app.tool(name="list-models", description="List all available note models in Anki")(list_models)
app.tool(name="get-model-fields", description="Get all field names and descriptions for a specific Anki note model")(get_model_fields)

if __name__ == "__main__":
    # Initialize and run the server
    import mcp
    mcp.run(transport='stdio')