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

## Optional: Language Learning Skill

This repository includes a complementary Claude skill that provides best practices for creating effective language learning flashcards. The skill works alongside the MCP server:

- **MCP Server**: Provides the tools to interact with Anki
- **Skill**: Provides guidance on how to use those tools effectively

To use the skill, copy `.claude/skills/language-learning.md` to your project's `.claude/skills/` directory. The AI will automatically invoke it when relevant for language learning flashcard creation.

The skill includes:
- Recommended workflow for card creation
- Card quality guidelines (length, content, cloze usage)
- Note type variety recommendations
- Examples of good vs bad cards
- Proficiency level guidelines (CEFR A1-C2)

This separation allows:
- Using the MCP server for any Anki workflow (not just language learning)
- Customizing or replacing the skill based on your learning methodology
- Sharing skills independently from the MCP infrastructure