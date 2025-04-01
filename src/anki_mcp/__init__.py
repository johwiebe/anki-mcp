#!/usr/bin/env python3
"""
Entry point for the Anki MCP server.
This allows the package to be run directly with `python -m anki_mcp`
or as an installed executable.
"""

from .server import app

def main():
    """Run the Anki MCP server."""
    app.run(transport='stdio')

if __name__ == "__main__":
    main()