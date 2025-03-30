import mcp.server.stdio
from mcp.server.fastmcp import FastMCP

from anki_mcp.tools.add_note import add_notes
from anki_mcp.tools.get_collection_overview import get_collection_overview
from anki_mcp.tools.get_cards_reviewed import get_cards_reviewed
from anki_mcp.tools.find_notes import find_notes
from anki_mcp.tools.update_note import update_notes

app = FastMCP("anki")

# Register tools with the app
app.tool(name="add-notes", description="Add one or more notes to Anki")(add_notes)
app.tool(name="get-collection-overview", description="Get comprehensive information about the Anki collection including decks, models, and fields")(get_collection_overview)
app.tool(name="get-cards-reviewed", description="Get the number of cards reviewed by day")(get_cards_reviewed)
app.tool(name='find-notes', description='Find notes matching a query in Anki')(find_notes)
app.tool(name="update-notes", description="Update one or more existing notes in Anki")(update_notes)

if __name__ == "__main__":
    # Initialize and run the server
    import mcp
    mcp.run(transport='stdio')