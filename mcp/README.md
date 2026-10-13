# Hermes MCP Server

Model Context Protocol (MCP) server for Hermes Figma Prompt Hub.

## Overview

The Hermes MCP Server exposes tools for managing and validating prompts through MCP clients like Claude Desktop, Cursor, and other MCP-compatible applications.

## Features

- **List Prompts** — Enumerate all prompt files in `prompts/raw/`
- **Validate Prompt** — Validate a specific prompt against schema
- **Get Statistics** — Analyze prompt collection (strategies, categories, validity)
- **MCP Tools Definition** — Discover available tools

## Installation

### Prerequisites

- Python 3.10+
- Hermes project installed locally

### Setup

1. Copy MCP server configuration to Claude Desktop config:

```bash
# macOS/Linux
mkdir -p ~/.config/Claude/
cp mcp/claude_desktop_config.json ~/.config/Claude/claude_desktop_config.json

# Windows
mkdir %APPDATA%\Claude
copy mcp\claude_desktop_config.json %APPDATA%\Claude\claude_desktop_config.json
```

2. Update the path in config to point to your local installation:

```json
{
  "mcpServers": {
    "hermes": {
      "command": "python3",
      "args": ["/absolute/path/to/hermes-figma-prompt-hub/mcp/server.py"],
      "env": {
        "PYTHONPATH": "/absolute/path/to/hermes-figma-prompt-hub/scripts"
      }
    }
  }
}
```

3. Restart Claude Desktop to load the server.

## Tools

### list_prompts

List all prompt files in the `prompts/raw/` directory.

**Parameters:** None

**Returns:**
```json
{
  "prompts": [
    {
      "filename": "prompt-1.json",
      "path": "prompts/raw/prompt-1.json",
      "size": 1024,
      "exists": true
    }
  ],
  "total": 1,
  "status": "success"
}
```

### validate_prompt

Validate a specific prompt file against the schema.

**Parameters:**
- `filename` (string, required) — Name of file in `prompts/raw/`

**Returns:**
```json
{
  "filename": "prompt-1.json",
  "valid": true,
  "status": "success",
  "errors": [],
  "warnings": [],
  "metadata": {
    "title": "Example Prompt",
    "description": "...",
    "strategy": "chain-of-thought",
    "category": "analysis",
    "version": "1.0"
  },
  "file_size": 1024
}
```

### get_prompt_stats

Get statistics about the prompts collection.

**Parameters:** None

**Returns:**
```json
{
  "total_prompts": 10,
  "total_size_bytes": 50000,
  "valid_prompts": 9,
  "invalid_prompts": 1,
  "strategies": {
    "chain-of-thought": 5,
    "few-shot": 3,
    "role-play": 2
  },
  "categories": {
    "analysis": 7,
    "generation": 3
  },
  "status": "success"
}
```

## Usage

### CLI

Test the server from command line:

```bash
# List all prompts
python3 mcp/server.py list

# Validate a specific prompt
python3 mcp/server.py validate --filename prompt-1.json

# Get statistics
python3 mcp/server.py stats

# Show available tools
python3 mcp/server.py tools
```

### Claude Desktop

In Claude Desktop, use the Hermes tools in conversations:

```
"Can you list all my prompts?"
"Validate the file prompt-1.json"
"How many prompts do I have?"
```

## Architecture

### HermesMCPServer Class

Main server class with static methods for each tool:

- `list_prompts()` — List prompt files
- `validate_prompt(filename)` — Validate specific prompt
- `get_prompt_stats()` — Get collection statistics
- `mcp_tools()` — Return MCP tool definitions
- `handle_tool_call(tool_name, args)` — Route tool calls

### Schema Validation

Uses the existing `schema_validator.py` from `scripts/` to validate prompts:

```python
from scripts.schema_validator import SchemaValidator
```

If the validator is not available, validation returns a warning.

## Roadmap

- [ ] Add `get_prompt_content` tool for reading full prompt
- [ ] Add `create_prompt` tool for creating new prompts
- [ ] Add `update_prompt` tool for editing prompts
- [ ] Add `sync_from_figma` tool for Figma integration
- [ ] Add `export_prompt` tool for various formats (JSON, YAML, Markdown)
- [ ] Add caching layer for performance
- [ ] Support for streaming responses
- [ ] Error recovery and retry logic

## Troubleshooting

### Server not connecting

1. Check the path in `claude_desktop_config.json` is absolute
2. Verify `schema_validator.py` exists in `scripts/`
3. Restart Claude Desktop after config changes

### Tool calls failing

1. Check that `prompts/raw/` directory exists
2. Verify prompt files are valid JSON
3. Run `python3 mcp/server.py validate --filename <name>` to test

### Module import errors

1. Ensure `PYTHONPATH` in config points to `scripts/` directory
2. Run `python3 -c "import schema_validator"` to test import

## See Also

- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [Claude Desktop Config](https://github.com/anthropics/anthropic-sdk-python/blob/main/README.md#claude-desktop)
- [Hermes Documentation](../README.md)
