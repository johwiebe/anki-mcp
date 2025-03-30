# Anki MCP Server

A Model Context Protocol (MCP) server for integrating AI assistants with Anki, the popular spaced repetition flashcard software.

## Features

This MCP server enables AI assistants to interact with Anki through the following tools:

### Tools

- **add-notes**: Add one or more notes to Anki
  - Create new flashcards with specified deck, model, and field values
  - Returns success/failure status for each note

- **update-notes**: Update one or more existing notes in Anki
  - Modify field values and/or tags for existing notes
  - Requires note IDs for the notes to be updated

- **find-notes**: Find notes matching a query in Anki
  - Search for existing notes using Anki's search syntax

- **check-connection**: Check connection to Anki
  - Verifies that AnkiConnect is running and accessible

- **list-decks**: List all available decks in Anki
  - Returns a list of all deck names in your Anki collection

- **get-cards-reviewed**: Get the number of cards reviewed by day
  - Retrieves review statistics showing cards studied per day

- **list-models**: List all available note models in Anki
  - Returns a list of all note types (models) available in your collection

- **get-model-fields**: Get all field names and descriptions for a specific Anki note model
  - Shows the structure of a specific note type, including field names and descriptions

## Requirements

- Anki must be installed and running
- [AnkiConnect](https://ankiweb.net/shared/info/2055492159) add-on must be installed in Anki

## Installation

### Installing uv

uv is a required dependency for running this MCP server. Follow these steps to install uv:

#### macOS and Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Windows

```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

For alternative installation methods and more detailed instructions, visit the [uv installation documentation](https://docs.astral.sh/uv/getting-started/installation/).

### Installing the Anki MCP Server

Once uv is installed, you can install the Anki MCP server using:

```bash
uvx install anki-mcp
```

To install a specific version:

```bash
uvx install anki-mcp==1.0.0
```

To update to the latest version:

```bash
uvx install --upgrade anki-mcp
```

## Configuration

### Claude Desktop

To add this MCP server to Claude Desktop:

On MacOS: Edit `~/Library/Application\ Support/Claude/claude_desktop_config.json`
On Windows: Edit `%APPDATA%/Claude/claude_desktop_config.json`

<details>
  <summary>Development/Unpublished Servers Configuration</summary>
  
  ```
  "mcpServers": {
    "anki-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/path/to/anki-mcp",
        "run",
        "anki-mcp"
      ]
    }
  }
  ```
</details>

<details>
  <summary>Published Servers Configuration</summary>
  
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
</details>

## Development

### Building and Publishing

To prepare the package for distribution:

1. Sync dependencies and update lockfile:
```bash
uv sync
```

2. Build package distributions:
```bash
uv build
```

This will create source and wheel distributions in the `dist/` directory.

3. Publish to PyPI:
```bash
uv publish
```

Note: You'll need to set PyPI credentials via environment variables or command flags:
- Token: `--token` or `UV_PUBLISH_TOKEN`
- Or username/password: `--username`/`UV_PUBLISH_USERNAME` and `--password`/`UV_PUBLISH_PASSWORD`

### Debugging

Since MCP servers run over stdio, debugging can be challenging. For the best debugging
experience, we strongly recommend using the [MCP Inspector](https://github.com/modelcontextprotocol/inspector).

You can launch the MCP Inspector via [`npm`](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) with this command:

```bash
npx @modelcontextprotocol/inspector uv --directory /path/to/anki-mcp run anki-mcp
```

Upon launching, the Inspector will display a URL that you can access in your browser to begin debugging.