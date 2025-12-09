import mcp.types as types
from typing import Optional
from datetime import datetime, timedelta
from .utils import make_anki_request


async def get_review_stats(
    time_range: str = "month",
    deck_name: Optional[str] = None
) -> list[types.TextContent]:
    """
    Get review statistics from Anki showing cards reviewed per day.

    Parameters:
    - time_range: Time range for statistics ("day", "week", "month", "year", "all")
    - deck_name: Optional deck name to filter statistics (shows only reviews from this deck)
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
    if deck_name:
        # When filtering by deck, we need to use a different approach
        # Get reviews for the specific deck using findCards and card info
        result = await _get_deck_review_stats(deck_name, cutoff_date)
    else:
        # Get all reviews across all decks
        result = await _get_all_review_stats(cutoff_date)

    return result


async def _get_all_review_stats(cutoff_date: Optional[datetime.date]) -> list[types.TextContent]:
    """Get review statistics for all decks."""
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


async def _get_deck_review_stats(deck_name: str, cutoff_date: Optional[datetime.date]) -> list[types.TextContent]:
    """Get review statistics for a specific deck."""
    # Note: AnkiConnect's getNumCardsReviewedByDay doesn't support deck filtering
    # We need to use a workaround by finding reviewed cards in the deck
    # This is an approximation based on cards in the deck that have review history

    # For now, we'll get the deck stats which shows current state
    # A full implementation would require tracking individual card reviews
    deck_stats_result = await make_anki_request("getDeckStats", decks=[deck_name])

    if not deck_stats_result["success"]:
        return [
            types.TextContent(
                type="text",
                text=f"Failed to retrieve deck statistics: {deck_stats_result['error']}"
            )
        ]

    # Also try to get the overall review stats and note the limitation
    all_reviews_result = await _get_all_review_stats(cutoff_date)

    deck_stats = deck_stats_result["result"]
    if deck_stats:
        stats = deck_stats[0]
        deck_info = (
            f"Deck '{deck_name}' current statistics:\n"
            f"  Total cards: {stats.get('total_in_deck', 'N/A')}\n"
            f"  Reviews today: {stats.get('reviews_today', 'N/A')}\n\n"
            f"Note: Per-day review history by deck is not available via AnkiConnect.\n"
            f"Showing overall review statistics below:\n\n"
        )
        all_reviews_text = all_reviews_result[0].text
        text = deck_info + all_reviews_text
    else:
        text = f"Deck '{deck_name}' not found."

    return [types.TextContent(type="text", text=text)]


def _parse_date(date_str: str) -> datetime.date:
    """Parse date string from Anki format to date object."""
    try:
        # Anki returns dates in YYYY-MM-DD format
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        # If parsing fails, return a very old date so it gets filtered out
        return datetime(1900, 1, 1).date()
