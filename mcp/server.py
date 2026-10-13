#!/usr/bin/env python3
"""
Hermes MCP Server - Model Context Protocol Integration

Provides tools for:
1. Listing prompt files from prompts/raw directory
2. Validating prompt files using schema validator
3. Getting prompt metadata and statistics

Usage:
    python3 mcp/server.py
"""

import json
import sys
import os
from pathlib import Path
from typing import Any, Optional
from dataclasses import dataclass, asdict

# Add scripts to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

try:
    from schema_validator import SchemaValidator
except ImportError:
    SchemaValidator = None


@dataclass
class PromptFile:
    """Represents a prompt file"""
    filename: str
    path: str
    size: int
    exists: bool
    valid: Optional[bool] = None
    errors: list = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []


class HermesMCPServer:
    """Minimal MCP Server for Hermes Figma Prompt Hub"""
    
    PROMPTS_DIR = Path(__file__).parent.parent / 'prompts' / 'raw'
    SCHEMA_VALIDATOR = SchemaValidator() if SchemaValidator else None
    
    @classmethod
    def list_prompts(cls) -> dict:
        """List all prompt files in prompts/raw directory
        
        Returns:
            {
                "prompts": [
                    {"filename": "...", "path": "...", "size": ...},
                    ...
                ],
                "total": 0,
                "status": "success" | "error"
            }
        """
        try:
            if not cls.PROMPTS_DIR.exists():
                return {
                    "prompts": [],
                    "total": 0,
                    "status": "error",
                    "message": f"Directory not found: {cls.PROMPTS_DIR}"
                }
            
            prompts = []
            for file_path in sorted(cls.PROMPTS_DIR.glob('*.json')):
                if file_path.is_file():
                    size = file_path.stat().st_size
                    prompts.append(
                        asdict(PromptFile(
                            filename=file_path.name,
                            path=str(file_path.relative_to(cls.PROMPTS_DIR.parent)),
                            size=size,
                            exists=True
                        ))
                    )
            
            return {
                "prompts": prompts,
                "total": len(prompts),
                "status": "success"
            }
        except Exception as e:
            return {
                "prompts": [],
                "total": 0,
                "status": "error",
                "message": str(e)
            }
    
    @classmethod
    def validate_prompt(cls, filename: str) -> dict:
        """Validate a specific prompt file against schema
        
        Args:
            filename: Name of prompt file in prompts/raw/
            
        Returns:
            {
                "filename": "...",
                "valid": true | false,
                "status": "success" | "error",
                "errors": ["..."],
                "warnings": ["..."],
                "metadata": {...}
            }
        """
        try:
            file_path = cls.PROMPTS_DIR / filename
            
            if not file_path.exists():
                return {
                    "filename": filename,
                    "valid": False,
                    "status": "error",
                    "message": f"File not found: {filename}"
                }
            
            # Load prompt file
            with open(file_path, 'r') as f:
                prompt_data = json.load(f)
            
            # Validate with schema validator if available
            errors = []
            warnings = []
            valid = True
            
            if cls.SCHEMA_VALIDATOR:
                result = cls.SCHEMA_VALIDATOR.validate(prompt_data)
                valid = result.get('valid', True)
                errors = result.get('errors', [])
                warnings = result.get('warnings', [])
            
            # Extract metadata
            metadata = {
                "title": prompt_data.get('title', 'Untitled'),
                "description": prompt_data.get('description', ''),
                "strategy": prompt_data.get('strategy', 'unknown'),
                "category": prompt_data.get('category', 'general'),
                "version": prompt_data.get('version', '1.0')
            }
            
            return {
                "filename": filename,
                "valid": valid,
                "status": "success",
                "errors": errors,
                "warnings": warnings,
                "metadata": metadata,
                "file_size": file_path.stat().st_size
            }
        except json.JSONDecodeError as e:
            return {
                "filename": filename,
                "valid": False,
                "status": "error",
                "message": f"Invalid JSON: {str(e)}"
            }
        except Exception as e:
            return {
                "filename": filename,
                "valid": False,
                "status": "error",
                "message": str(e)
            }
    
    @classmethod
    def get_prompt_stats(cls) -> dict:
        """Get statistics about prompts collection
        
        Returns:
            {
                "total_prompts": 0,
                "total_size_bytes": 0,
                "valid_prompts": 0,
                "invalid_prompts": 0,
                "strategies": {...},
                "categories": {...}
            }
        """
        try:
            if not cls.PROMPTS_DIR.exists():
                return {
                    "total_prompts": 0,
                    "status": "error",
                    "message": f"Directory not found: {cls.PROMPTS_DIR}"
                }
            
            stats = {
                "total_prompts": 0,
                "total_size_bytes": 0,
                "valid_prompts": 0,
                "invalid_prompts": 0,
                "strategies": {},
                "categories": {}
            }
            
            for file_path in cls.PROMPTS_DIR.glob('*.json'):
                if not file_path.is_file():
                    continue
                
                stats["total_prompts"] += 1
                stats["total_size_bytes"] += file_path.stat().st_size
                
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                    
                    # Track validation
                    validation = cls.validate_prompt(file_path.name)
                    if validation.get('valid'):
                        stats["valid_prompts"] += 1
                    else:
                        stats["invalid_prompts"] += 1
                    
                    # Track strategy
                    strategy = data.get('strategy', 'unknown')
                    stats["strategies"][strategy] = stats["strategies"].get(strategy, 0) + 1
                    
                    # Track category
                    category = data.get('category', 'general')
                    stats["categories"][category] = stats["categories"].get(category, 0) + 1
                
                except Exception:
                    stats["invalid_prompts"] += 1
            
            stats["status"] = "success"
            return stats
        except Exception as e:
            return {
                "total_prompts": 0,
                "status": "error",
                "message": str(e)
            }
    
    @classmethod
    def mcp_tools(cls) -> list:
        """Return list of MCP tools available
        
        Returns:
            List of tool definitions for MCP
        """
        return [
            {
                "name": "list_prompts",
                "description": "List all prompt files in prompts/raw directory",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "validate_prompt",
                "description": "Validate a specific prompt file against schema",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "filename": {
                            "type": "string",
                            "description": "Name of prompt file in prompts/raw/"
                        }
                    },
                    "required": ["filename"]
                }
            },
            {
                "name": "get_prompt_stats",
                "description": "Get statistics about prompts collection",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            }
        ]
    
    @classmethod
    def handle_tool_call(cls, tool_name: str, args: dict) -> Any:
        """Handle MCP tool call
        
        Args:
            tool_name: Name of tool to call
            args: Tool arguments
            
        Returns:
            Tool result
        """
        if tool_name == "list_prompts":
            return cls.list_prompts()
        elif tool_name == "validate_prompt":
            return cls.validate_prompt(args.get("filename", ""))
        elif tool_name == "get_prompt_stats":
            return cls.get_prompt_stats()
        else:
            return {"error": f"Unknown tool: {tool_name}"}


def main():
    """Simple CLI for testing MCP server"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Hermes MCP Server CLI"
    )
    parser.add_argument(
        "command",
        nargs="?",
        choices=["list", "validate", "stats", "tools"],
        default="tools",
        help="Command to run"
    )
    parser.add_argument(
        "--filename",
        help="Prompt filename for validate command"
    )
    
    args = parser.parse_args()
    
    server = HermesMCPServer()
    
    if args.command == "list":
        result = server.list_prompts()
    elif args.command == "validate":
        if not args.filename:
            print("Error: --filename required for validate command")
            sys.exit(1)
        result = server.validate_prompt(args.filename)
    elif args.command == "stats":
        result = server.get_prompt_stats()
    elif args.command == "tools":
        result = server.mcp_tools()
    else:
        result = {"error": f"Unknown command: {args.command}"}
    
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
