# Anki MCP Server

A Model Context Protocol (MCP) server for integrating AI assistants with Anki, the popular spaced repetition flashcard software.

## Features

This MCP server enables AI assistants to interact with Anki through the following tools:

### Tools

- **get-collection-overview**: Returns an overview of the Anki collection like available decks, available models and their fields

- **add-or-update-notes**: Adds new notes or updates existing ones. Allows batch adding/updating multiple notes at once.

- **get-cards-reviewed**: Get the number of cards reviewed by day

- **find-notes**: Allows querying notes using the [Anki searching syntax](https://docs.ankiweb.net/searching.html)

- **find-cards**: Find card IDs matching a query in Anki

- **suspend-cards**: Suspend cards by their card IDs

- **unsuspend-cards**: Unsuspend cards by their card IDs

### Resources

- **anki://docs/search-syntax**: Comprehensive reference guide for Anki's search query syntax. Includes basic operators, field searches, tags, decks, card states, properties, timing, IDs, custom data, and advanced query examples. This resource provides language-agnostic documentation useful for anyone constructing search queries with the find-notes or find-cards tools

### Prompts

- **get_create_language_cards_prompt**: Guides the creation of effective language learning flashcards with best practices for spaced repetition. This prompt template helps create short, natural example sentences and vocabulary cards appropriate for different proficiency levels (A1-C2). It follows a structured workflow: check collection → generate examples → review with user → add confirmed cards. Parameters:
  - `target_language`: The language being learned (e.g., "Spanish", "French")
  - `focus`: What to focus on (e.g., "common verbs", "food vocabulary")
  - `source_language`: Native/source language (default: "English")
  - `proficiency_level`: Learning level A1-C2 (default: "B1")
  - `target_deck`: Anki deck to add cards to (default: "Default")

## Requirements

- Anki must be installed and running
- The [AnkiConnect](https://ankiweb.net/shared/info/2055492159) add-on must be installed in Anki and running
- This MCP server uses `uv`. To install `uv`, follow the [official instructions](https://docs.astral.sh/uv/getting-started/installation/).


## Configuration

### Claude Desktop

1. Open your Claude Desktop config file:
  - MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
  - Windows: `%APPDATA%/Claude/claude_desktop_config.json`

2. Add `anki-mcp` to the `mcpServers` section:  
  ```
  "mcpServers": {
    "anki-mcp": {
      "command": "uvx",
      "args": [
        "anki-mcp"
      ]
    }
  }
  ```

3. Restart Claude Desktop.