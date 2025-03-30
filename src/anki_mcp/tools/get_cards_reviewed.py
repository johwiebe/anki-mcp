import mcp.types as types

from .utils import make_anki_request

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
