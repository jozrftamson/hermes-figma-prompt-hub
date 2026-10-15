# MCP Server Integration Guide

## Overview

Hermes Figma Prompt Hub integrates the **Model Context Protocol (MCP)** to enable dynamic prompt management and seamless Figma-to-AI workflow integration.

## What is MCP?

The Model Context Protocol is a standardized interface for AI models to interact with external tools and data sources. In this project, MCP enables:

- **Prompt Synchronization**: Real-time sync of prompts from Figma to MCP-compatible clients
- **Schema Validation**: Automatic validation of prompt schemas
- **Tool Integration**: Connect with LLMs, code generation tools, and AI evaluation frameworks
- **State Management**: Track prompt versions and changes

## Architecture

```
┌─────────────────┐
│  Figma Design   │
│   Components    │
└────────┬────────┘
         │
    ✓ PROMPT frames
    ✓ Validation rules
    ✓ Metadata
         │
         ▼
┌─────────────────────────────┐
│ MCP Server (mcp_server.py)  │
├─────────────────────────────┤
│ • Prompt extraction         │
│ • Schema validation         │
│ • Version tracking          │
│ • Export/import tools       │
└────────┬────────────────────┘
         │
         ▼
┌────────────────────────────────┐
│ MCP Clients                    │
├────────────────────────────────┤
│ • Claude Desktop               │
│ • Cursor IDE                   │
│ • GitHub Copilot (via agent)   │
│ • Custom LLM applications      │
└────────────────────────────────┘
```

## Installation

### Prerequisites

- Python 3.10+
- Figma API token
- MCP SDK (`pip install mcp`)

### Setup Steps

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   # Includes: mcp, pydantic, figma-api, python-dotenv
   ```

2. **Configure Environment**
   ```bash
   export FIGMA_API_TOKEN="your-figma-token-here"
   export MCP_PORT=8080
   export MCP_HOST="127.0.0.1"
   ```

   Or add to `.env`:
   ```env
   FIGMA_API_TOKEN=your_token
   FIGMA_FILE_KEY=your_figma_file_key
   MCP_PORT=8080
   MCP_HOST=127.0.0.1
   ```

3. **Start MCP Server**
   ```bash
   python -m scripts.mcp_server
   # Output: MCP Server running on 127.0.0.1:8080
   ```

## Core Features

### 1. Prompt Extraction from Figma

```python
from scripts.figma_importer import FigmaImporter

importer = FigmaImporter(api_token=os.getenv("FIGMA_API_TOKEN"))
prompts = importer.extract_prompts(figma_file_key="abc123xyz")

for prompt in prompts:
    print(f"Prompt: {prompt.name}")
    print(f"Content: {prompt.content}")
    print(f"Tags: {prompt.tags}")
```

### 2. Schema Validation

```python
from scripts.schema_validator import SchemaValidator

validator = SchemaValidator()
validation_result = validator.validate_prompt(
    name="system_prompt",
    content="You are a helpful assistant...",
    required_fields=["name", "content", "version"]
)

if validation_result.is_valid:
    print("✓ Prompt is valid")
else:
    print(f"✗ Validation errors: {validation_result.errors}")
```

### 3. Batch Processing

```python
from scripts.validate_all import BatchValidator

batch = BatchValidator()
results = batch.validate_directory("./prompts/")

print(f"Total: {results.total}")
print(f"Valid: {results.valid_count}")
print(f"Failed: {results.failed_count}")
```

## MCP Tool Registration

### Available Tools

The MCP server exposes the following tools:

| Tool | Description | Parameters |
|------|-------------|-----------|
| `extract_prompts` | Extract prompts from Figma | `figma_file_key`, `filter_tags` |
| `validate_prompt` | Validate prompt schema | `prompt_data` |
| `sync_to_github` | Sync prompts to GitHub | `target_branch` |
| `generate_docs` | Auto-generate documentation | `prompt_ids` |

### Registering Custom Tools

```python
from mcp.server import MCP

mcp = MCP()

@mcp.tool()
def my_custom_tool(param1: str, param2: int) -> str:
    """
    Description of what this tool does.
    """
    return f"Result: {param1} + {param2}"

mcp.run()
```

## Integration Examples

### Claude Desktop

Add to `~/.config/claude.json`:

```json
{
  "mcpServers": {
    "hermes-figma": {
      "command": "python",
      "args": ["-m", "scripts.mcp_server"],
      "env": {
        "FIGMA_API_TOKEN": "sk-..."
      }
    }
  }
}
```

### Cursor IDE

Add to `.cursor/settings.json`:

```json
{
  "mcpServers": [
    {
      "name": "hermes-figma",
      "url": "http://127.0.0.1:8080",
      "auth": "token YOUR_TOKEN"
    }
  ]
}
```

### Custom Python Client

```python
import httpx

client = httpx.AsyncClient()

response = await client.post(
    "http://127.0.0.1:8080/tools/extract_prompts",
    json={"figma_file_key": "abc123", "filter_tags": ["system"]}
)

prompts = response.json()["result"]
```

## Configuration

### Environment Variables

```bash
# Figma Configuration
FIGMA_API_TOKEN          # Your Figma API token
FIGMA_FILE_KEY           # Default Figma file to use

# MCP Server Configuration
MCP_PORT                 # Default: 8080
MCP_HOST                 # Default: 127.0.0.1
MCP_WORKERS              # Default: 4 (for async handlers)

# Logging
LOG_LEVEL                # Default: INFO (DEBUG, INFO, WARNING, ERROR)
LOG_FORMAT               # Default: json

# Validation
SCHEMA_VERSION           # JSON Schema version to use
STRICT_VALIDATION        # Enforce strict schema validation (default: false)
```

### Config File (`.mcp.json`)

```json
{
  "server": {
    "port": 8080,
    "host": "127.0.0.1",
    "workers": 4,
    "timeout": 30
  },
  "figma": {
    "api_version": "v1",
    "rate_limit": 120,
    "cache_ttl": 3600
  },
  "validation": {
    "strict": false,
    "schema_version": "2024.1"
  }
}
```

## API Reference

### POST `/tools/extract_prompts`

Extract prompts from a Figma file.

**Request:**
```json
{
  "figma_file_key": "abc123xyz",
  "filter_tags": ["system", "user"],
  "include_metadata": true
}
```

**Response:**
```json
{
  "success": true,
  "prompts": [
    {
      "id": "uuid",
      "name": "system_greeting",
      "content": "You are a helpful assistant.",
      "tags": ["system"],
      "version": "1.0",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### POST `/tools/validate_prompt`

Validate a prompt against schema.

**Request:**
```json
{
  "name": "my_prompt",
  "content": "Prompt content here...",
  "tags": ["system"]
}
```

**Response:**
```json
{
  "valid": true,
  "errors": [],
  "warnings": []
}
```

## Troubleshooting

### Issue: "Connection refused" on port 8080

**Solution**: Check if port is in use:
```bash
lsof -i :8080
# Kill process if needed: kill -9 <PID>

# Or use different port:
export MCP_PORT=8081
```

### Issue: "Invalid Figma token"

**Solution**: Verify token:
```bash
curl -H "X-Figma-Token: $FIGMA_API_TOKEN" \
  https://api.figma.com/v1/me
```

### Issue: "Schema validation failed"

**Solution**: Check validation logs:
```bash
export LOG_LEVEL=DEBUG
python -m scripts.mcp_server
```

## Development

### Running Tests

```bash
# Unit tests
python -m pytest tests/mcp/ -v

# Integration tests (requires Figma token)
python -m pytest tests/integration/ -v --figma-token=$FIGMA_API_TOKEN

# All tests
pytest
```

### Building Custom Schemas

```python
from pydantic import BaseModel

class CustomPrompt(BaseModel):
    name: str
    content: str
    custom_field: str
    
validator.register_schema("custom", CustomPrompt)
```

## Performance Optimization

### Caching

```python
from scripts.mcp_server import MCPServer

server = MCPServer(
    cache_enabled=True,
    cache_ttl=3600,  # 1 hour
    cache_backend="redis"  # or "memory"
)
```

### Async Processing

```python
import asyncio

async def process_prompts():
    prompts = await importer.extract_prompts_async(figma_file_key)
    results = await asyncio.gather(*[
        validator.validate_prompt(p) for p in prompts
    ])
    return results
```

## Security

### API Token Protection

Never commit tokens to version control:
```bash
# Use .env files (add to .gitignore)
echo "FIGMA_API_TOKEN=sk-..." > .env

# Or use GitHub Secrets (for CI/CD)
```

### Rate Limiting

Figma API has rate limits. Implement exponential backoff:
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
async def call_figma_api():
    # Implementation
    pass
```

## Resources

- [MCP Protocol Spec](https://spec.modelcontextprotocol.io/)
- [Figma API Docs](https://www.figma.com/developers/api)
- [Hermes Project README](../README.md)
- [Contributing Guide](../CONTRIBUTING.md)

## Support

- 📖 [Documentation](./index.md)
- 🐛 [Report Issues](https://github.com/jozrftamson/hermes-figma-prompt-hub/issues)
- 💬 [Discussions](https://github.com/jozrftamson/hermes-figma-prompt-hub/discussions)
