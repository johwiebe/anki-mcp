import mcp.server.stdio
from mcp.server.fastmcp import FastMCP

# Import all tools
from .tools import (
    add_notes, 
    check_connection, 
    list_decks, 
    get_cards_reviewed,
    list_models,
    get_model_fields,
    find_notes,
    update_notes
)

app = FastMCP("anki")

# Register tools with the app
app.tool(name="add-notes", description="Add one or more notes to Anki")(add_notes)
app.tool(name="check-connection", description="Check connection to Anki")(check_connection)
app.tool(name="list-decks", description="List all available decks in Anki")(list_decks)
app.tool(name="get-cards-reviewed", description="Get the number of cards reviewed by day")(get_cards_reviewed)
app.tool(name="list-models", description="List all available note models in Anki")(list_models)
app.tool(name="get-model-fields", description="Get all field names and descriptions for a specific Anki note model")(get_model_fields)
app.tool(name='find-notes', description='Find notes matching a query in Anki')(find_notes)
app.tool(name="update-notes", description="Update one or more existing notes in Anki")(update_notes)

if __name__ == "__main__":
    # Initialize and run the server
    import mcp
    mcp.run(transport='stdio')