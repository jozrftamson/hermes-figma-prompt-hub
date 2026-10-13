"""
Hermes MCP (Model Context Protocol) Server Package

Provides tools for prompt management through MCP clients like Claude Desktop.
"""

from .server import HermesMCPServer

__version__ = "1.0.0"
__all__ = ["HermesMCPServer"]
