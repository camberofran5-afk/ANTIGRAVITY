"""
L1 Configuration: Model Context Protocol (MCP) Configuration
Centralized configuration for MCP servers and tool integration.
Following the 4-Layer Hierarchy: L1 = Configuration (Zero dependencies on other layers)
"""

import os
from enum import Enum
from typing import TypedDict, Optional, List, Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class MCPTransport(str, Enum):
    """MCP transport methods."""
    STDIO = "stdio"  # Standard input/output (local command execution)
    SSE = "sse"  # Server-Sent Events (HTTP streaming)
    HTTP = "http"  # Standard HTTP
    STREAMABLE_HTTP = "streamable-http"  # HTTP with streaming support


class MCPServerConfig(TypedDict):
    """MCP server configuration structure."""
    name: str
    transport: MCPTransport
    url: Optional[str]  # For HTTP/SSE transports
    command: Optional[str]  # For STDIO transport
    args: Optional[List[str]]  # Command arguments for STDIO
    env: Optional[Dict[str, str]]  # Environment variables
    enabled: bool


class MCPSettings:
    """
    Centralized MCP (Model Context Protocol) configuration.
    
    Manages MCP server registry and connection settings.
    Supports multiple transport methods (stdio, SSE, HTTP).
    """
    
    # Default MCP server registry
    DEFAULT_SERVERS: Dict[str, MCPServerConfig] = {
        # Example: Supabase MCP server
        "supabase": {
            "name": "Supabase Database Tools",
            "transport": MCPTransport.HTTP,
            "url": "http://localhost:8000/mcp",
            "command": None,
            "args": None,
            "env": None,
            "enabled": False,  # Disabled by default until implemented
        },
        
        # Example: File system MCP server
        "filesystem": {
            "name": "File System Access",
            "transport": MCPTransport.STDIO,
            "url": None,
            "command": "python",
            "args": ["-m", "mcp.servers.filesystem"],
            "env": None,
            "enabled": False,
        },
        
        # Example: Web search MCP server
        "web_search": {
            "name": "Web Search Tools",
            "transport": MCPTransport.HTTP,
            "url": "http://localhost:8001/mcp",
            "command": None,
            "args": None,
            "env": None,
            "enabled": False,
        },
    }
    
    # MCP client settings
    DEFAULT_TIMEOUT = 30  # seconds
    DEFAULT_MAX_RETRIES = 3
    DEFAULT_RETRY_DELAY = 2  # seconds
    
    def __init__(self):
        """Initialize MCP configuration from environment variables."""
        self.timeout: int = int(os.getenv(
            "MCP_TIMEOUT",
            str(self.DEFAULT_TIMEOUT)
        ))
        self.max_retries: int = int(os.getenv(
            "MCP_MAX_RETRIES",
            str(self.DEFAULT_MAX_RETRIES)
        ))
        self.retry_delay: int = int(os.getenv(
            "MCP_RETRY_DELAY",
            str(self.DEFAULT_RETRY_DELAY)
        ))
        
        # Load custom servers from environment
        self.servers: Dict[str, MCPServerConfig] = self.DEFAULT_SERVERS.copy()
        self._load_custom_servers()
    
    def _load_custom_servers(self):
        """Load custom MCP servers from environment variables."""
        # Format: MCP_SERVER_<NAME>_URL, MCP_SERVER_<NAME>_TRANSPORT, etc.
        # This allows dynamic server configuration via .env
        pass  # TODO: Implement custom server loading
    
    def get_server(self, name: str) -> Optional[MCPServerConfig]:
        """
        Get MCP server configuration by name.
        
        Args:
            name: Server name
            
        Returns:
            MCPServerConfig if found, None otherwise
        """
        return self.servers.get(name)
    
    def get_enabled_servers(self) -> Dict[str, MCPServerConfig]:
        """
        Get all enabled MCP servers.
        
        Returns:
            Dictionary of enabled server configurations
        """
        return {
            name: config
            for name, config in self.servers.items()
            if config.get("enabled", False)
        }
    
    def register_server(
        self,
        name: str,
        transport: MCPTransport,
        url: Optional[str] = None,
        command: Optional[str] = None,
        args: Optional[List[str]] = None,
        env: Optional[Dict[str, str]] = None,
        enabled: bool = True,
    ):
        """
        Register a new MCP server.
        
        Args:
            name: Server name
            transport: Transport method
            url: Server URL (for HTTP/SSE)
            command: Command to execute (for STDIO)
            args: Command arguments
            env: Environment variables
            enabled: Whether server is enabled
        """
        self.servers[name] = {
            "name": name,
            "transport": transport,
            "url": url,
            "command": command,
            "args": args,
            "env": env,
            "enabled": enabled,
        }
    
    def enable_server(self, name: str):
        """Enable an MCP server."""
        if name in self.servers:
            self.servers[name]["enabled"] = True
    
    def disable_server(self, name: str):
        """Disable an MCP server."""
        if name in self.servers:
            self.servers[name]["enabled"] = False
    
    def list_servers(self) -> List[str]:
        """
        List all registered MCP server names.
        
        Returns:
            List of server names
        """
        return list(self.servers.keys())


# Singleton instance
_mcp_settings: Optional[MCPSettings] = None


def get_mcp_settings() -> MCPSettings:
    """
    Get the singleton MCP settings instance.
    
    Returns:
        MCPSettings instance
        
    Example:
        >>> from tools.L1_config.mcp_config import get_mcp_settings
        >>> settings = get_mcp_settings()
        >>> servers = settings.get_enabled_servers()
    """
    global _mcp_settings
    
    if _mcp_settings is None:
        _mcp_settings = MCPSettings()
    
    return _mcp_settings


if __name__ == "__main__":
    # Test the configuration
    print("🔍 Testing MCP Configuration...")
    print()
    
    settings = get_mcp_settings()
    
    print("✅ MCP Configuration loaded")
    print()
    print(f"Timeout: {settings.timeout}s")
    print(f"Max Retries: {settings.max_retries}")
    print(f"Retry Delay: {settings.retry_delay}s")
    print()
    
    # List all servers
    print("📋 Registered MCP Servers:")
    for name in settings.list_servers():
        server = settings.get_server(name)
        if server:
            status = "✅ Enabled" if server["enabled"] else "⚠️  Disabled"
            print(f"  • {server['name']} ({name})")
            print(f"    Status: {status}")
            print(f"    Transport: {server['transport']}")
            if server['url']:
                print(f"    URL: {server['url']}")
            if server['command']:
                print(f"    Command: {server['command']}")
            print()
    
    # Show enabled servers
    enabled = settings.get_enabled_servers()
    print(f"🟢 Enabled Servers: {len(enabled)}")
    if not enabled:
        print("   (No servers enabled yet)")
        print("   Enable servers in .env or via code")
