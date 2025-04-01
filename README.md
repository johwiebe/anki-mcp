# Anki MCP Server

A Model Context Protocol (MCP) server for integrating AI assistants with Anki, the popular spaced repetition flashcard software.

## Features

This MCP server enables AI assistants to interact with Anki through the following tools:

### Tools

- **get-collection-overview**: Returns an overview of the Anki collection like available decks, available models and their fields

- **add-or-update-notes**: Adds new notes or updates existing ones. Allows batch adding/updating multiple notes at once.

- **get-cards-reviewed**: Get the number of cards reviewed by day

- **find-notes**: Allows querying notes using the [Anki searching syntax](https://docs.ankiweb.net/searching.html)

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