"""Language learning flashcard creation prompt."""


def create_language_cards_prompt(
    target_language: str,
    focus: str,
    source_language: str = "English",
    proficiency_level: str = "B1",
    target_deck: str = "Default",
) -> str:
    """
    Generate a prompt for creating language learning flashcards.

    This prompt guides the AI to help create effective language learning flashcards
    using best practices for spaced repetition systems.

    Args:
        target_language: The language being learned (e.g., "Spanish", "French")
        focus: What to focus on (e.g., "common verbs", "food vocabulary", "past tense")
        source_language: The native/source language (default: "English")
        proficiency_level: Learning level - A1, A2, B1, B2, C1, or C2 (default: "B1")
        target_deck: Name of the Anki deck to add cards to (default: "Default")

    Returns:
        str: A formatted prompt for creating language learning flashcards
    """
    return f"""You are helping create {target_language} flashcards for a {proficiency_level} level learner.

## Task
Create flashcards focused on: {focus}

## Workflow
1. First, use the get-collection-overview tool to see available note types and their fields
2. Generate example sentences/words appropriate for {proficiency_level} level
3. Show them to the user as a numbered list ({source_language} and {target_language})
4. After user confirms which ones they like, use add-or-update-notes to create them
5. Add all cards to the "{target_deck}" deck
6. Tag new cards with "needs-review" so the user can verify them later

## Card Creation Guidelines

**Content Quality:**
- Keep sentences short and natural (ideally under 10 words)
- Use conversational, everyday language appropriate for {proficiency_level} level
- Create a mix of sentence examples and individual words
- For cloze cards: make ONE cloze deletion per card (on the key word/phrase)
- Include gender markers (el/la, der/die/das, le/la, etc.) where applicable

**Note Type Variety:**
- Mix different note types from the collection (e.g., cloze, basic front/back, etc.)
- Aim for about 30% individual words, 70% short example sentences
- Choose note types that match the content (cloze for context, basic for vocabulary)

**Examples of Good Cards:**

Cloze example:
- {target_language}: "I {{{{c1::broke}}}} the glass by accident"
- {source_language}: "I broke the glass by accident"

Basic word example:
- Front: "to wander alone"
- Back: "(word in {target_language})"

**What to Avoid:**
- Long, complex sentences
- Multiple cloze deletions in one card
- Formal or literary language (unless specifically requested)
- Overly simple content below the {proficiency_level} level

## Important Notes
- Always check the collection overview first to see what note types and fields are available
- Adapt your card format to match the available note types in the user's collection
- Wait for user confirmation before creating the cards in Anki
"""


def get_create_language_cards_prompt(
    target_language: str,
    focus: str,
    source_language: str = "English",
    proficiency_level: str = "B1",
    target_deck: str = "Default",
) -> str:
    """
    Wrapper function for the language learning prompt.

    This is the function that will be registered with the MCP server.

    Args:
        target_language: The language being learned
        focus: What to focus on (vocabulary, grammar topic, etc.)
        source_language: The native/source language (default: "English")
        proficiency_level: Learning level A1-C2 (default: "B1")
        target_deck: Target Anki deck name (default: "Default")

    Returns:
        str: The formatted prompt
    """
    return create_language_cards_prompt(
        target_language=target_language,
        focus=focus,
        source_language=source_language,
        proficiency_level=proficiency_level,
        target_deck=target_deck,
    )
