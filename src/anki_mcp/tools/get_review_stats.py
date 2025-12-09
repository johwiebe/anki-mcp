import mcp.types as types
from datetime import datetime, timedelta
from .utils import make_anki_request


async def get_review_stats(
    time_range: str = "month"
) -> list[types.TextContent]:
    """
    Get review statistics from Anki showing cards reviewed per day.

    Parameters:
    - time_range: Time range for statistics ("day", "week", "month", "year", "all")
    """
    # Calculate date cutoff based on time_range
    today = datetime.now().date()

    if time_range == "day":
        cutoff_date = today
    elif time_range == "week":
        cutoff_date = today - timedelta(days=7)
    elif time_range == "month":
        cutoff_date = today - timedelta(days=30)
    elif time_range == "year":
        cutoff_date = today - timedelta(days=365)
    elif time_range == "all":
        cutoff_date = None  # No filtering
    else:
        return [
            types.TextContent(
                type="text",
                text=f"Invalid time_range '{time_range}'. Valid options: day, week, month, year, all"
            )
        ]

    # Get review statistics from Anki
    review_result = await make_anki_request("getNumCardsReviewedByDay")

    if not review_result["success"]:
        return [
            types.TextContent(
                type="text",
                text=f"Failed to retrieve review statistics: {review_result['error']}"
            )
        ]

    review_data = review_result["result"]

    # Filter by date if cutoff_date is specified
    if cutoff_date:
        filtered_data = [
            (date_str, count) for date_str, count in review_data
            if _parse_date(date_str) >= cutoff_date
        ]
    else:
        filtered_data = review_data

    # Format the output
    if not filtered_data:
        text = "No reviews found for the specified time range."
    else:
        total_cards = sum(count for _, count in filtered_data)
        formatted_lines = [f"  {date_str}: {count} cards" for date_str, count in filtered_data]

        text = f"Cards reviewed ({len(filtered_data)} days, {total_cards} total reviews):\n"
        text += "\n".join(formatted_lines)

    return [types.TextContent(type="text", text=text)]


def _parse_date(date_str: str) -> datetime.date:
    """Parse date string from Anki format to date object."""
    try:
        # Anki returns dates in YYYY-MM-DD format
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        # If parsing fails, return a very old date so it gets filtered out
        return datetime(1900, 1, 1).date()
