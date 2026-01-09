"""
L2 Foundation: MCP Client
Provides MCP (Model Context Protocol) client for tool integration.
Following the 4-Layer Hierarchy: L2 = Foundation (Depends only on L1)
"""

import json
import subprocess
import requests
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from tools.L1_config.mcp_config import (
    get_mcp_settings,
    MCPServerConfig,
    MCPTransport
)
from tools.L1_config.logging_config import get_logger

logger = get_logger(__name__)


@dataclass
class MCPTool:
    """Represents an MCP tool."""
    name: str
    description: str
    input_schema: Dict[str, Any]
    server_name: str


@dataclass
class MCPToolResult:
    """Result from MCP tool execution."""
    success: bool
    result: Any
    error: Optional[str] = None


class MCPClient:
    """
    Client for interacting with MCP (Model Context Protocol) servers.
    
    Supports multiple transport methods:
    - STDIO: Local command execution
    - HTTP/SSE: Remote server communication
    
    Example:
        >>> client = MCPClient()
        >>> tools = client.discover_tools("supabase")
        >>> result = client.execute_tool("supabase", "query_table", {...})
    """
    
    def __init__(self):
        """Initialize MCP client with settings from L1 config."""
        self.settings = get_mcp_settings()
        self._tool_cache: Dict[str, List[MCPTool]] = {}
    
    def discover_tools(self, server_name: str) -> List[MCPTool]:
        """
        Discover available tools from an MCP server.
        
        Args:
            server_name: Name of the MCP server
            
        Returns:
            List of available MCPTool objects
            
        Raises:
            ValueError: If server not found or disabled
            ConnectionError: If cannot connect to server
        """
        # Check cache first
        if server_name in self._tool_cache:
            logger.info(
                "mcp_tools_cached",
                server=server_name,
                count=len(self._tool_cache[server_name])
            )
            return self._tool_cache[server_name]
        
        # Get server config
        server = self.settings.get_server(server_name)
        if not server:
            raise ValueError(f"MCP server '{server_name}' not found")
        
        if not server.get("enabled", False):
            raise ValueError(f"MCP server '{server_name}' is disabled")
        
        logger.info("mcp_discovering_tools", server=server_name)
        
        # Discover tools based on transport
        if server["transport"] == MCPTransport.STDIO:
            tools = self._discover_stdio_tools(server)
        elif server["transport"] in [MCPTransport.HTTP, MCPTransport.SSE, MCPTransport.STREAMABLE_HTTP]:
            tools = self._discover_http_tools(server)
        else:
            raise ValueError(f"Unsupported transport: {server['transport']}")
        
        # Cache the tools
        self._tool_cache[server_name] = tools
        
        logger.info(
            "mcp_tools_discovered",
            server=server_name,
            count=len(tools)
        )
        
        return tools
    
    def _discover_stdio_tools(self, server: MCPServerConfig) -> List[MCPTool]:
        """Discover tools from STDIO MCP server."""
        # TODO: Implement STDIO tool discovery
        # This would execute the command and communicate via stdin/stdout
        logger.warning("mcp_stdio_not_implemented", server=server["name"])
        return []
    
    def _discover_http_tools(self, server: MCPServerConfig) -> List[MCPTool]:
        """Discover tools from HTTP MCP server."""
        try:
            url = server["url"]
            if not url:
                raise ValueError("HTTP server requires URL")
            
            # Make discovery request
            response = requests.get(
                f"{url}/tools",
                timeout=self.settings.timeout
            )
            response.raise_for_status()
            
            # Parse tools
            tools_data = response.json()
            tools = []
            
            for tool_data in tools_data.get("tools", []):
                tool = MCPTool(
                    name=tool_data["name"],
                    description=tool_data.get("description", ""),
                    input_schema=tool_data.get("inputSchema", {}),
                    server_name=server["name"]
                )
                tools.append(tool)
            
            return tools
            
        except requests.RequestException as e:
            logger.error(
                "mcp_http_discovery_failed",
                server=server["name"],
                error=str(e)
            )
            raise ConnectionError(f"Failed to discover tools from {server['name']}: {e}")
    
    def execute_tool(
        self,
        server_name: str,
        tool_name: str,
        parameters: Dict[str, Any]
    ) -> MCPToolResult:
        """
        Execute an MCP tool.
        
        Args:
            server_name: Name of the MCP server
            tool_name: Name of the tool to execute
            parameters: Tool parameters
            
        Returns:
            MCPToolResult with execution result
            
        Example:
            >>> result = client.execute_tool(
            ...     "supabase",
            ...     "query_table",
            ...     {"table": "users", "limit": 10}
            ... )
            >>> if result.success:
            ...     print(result.result)
        """
        # Get server config
        server = self.settings.get_server(server_name)
        if not server:
            return MCPToolResult(
                success=False,
                result=None,
                error=f"Server '{server_name}' not found"
            )
        
        logger.info(
            "mcp_executing_tool",
            server=server_name,
            tool=tool_name,
            parameters=parameters
        )
        
        # Execute based on transport
        try:
            if server["transport"] == MCPTransport.STDIO:
                result = self._execute_stdio_tool(server, tool_name, parameters)
            elif server["transport"] in [MCPTransport.HTTP, MCPTransport.SSE, MCPTransport.STREAMABLE_HTTP]:
                result = self._execute_http_tool(server, tool_name, parameters)
            else:
                return MCPToolResult(
                    success=False,
                    result=None,
                    error=f"Unsupported transport: {server['transport']}"
                )
            
            logger.info(
                "mcp_tool_executed",
                server=server_name,
                tool=tool_name,
                success=result.success
            )
            
            return result
            
        except Exception as e:
            logger.error(
                "mcp_tool_execution_failed",
                server=server_name,
                tool=tool_name,
                error=str(e)
            )
            return MCPToolResult(
                success=False,
                result=None,
                error=str(e)
            )
    
    def _execute_stdio_tool(
        self,
        server: MCPServerConfig,
        tool_name: str,
        parameters: Dict[str, Any]
    ) -> MCPToolResult:
        """Execute tool via STDIO transport."""
        # TODO: Implement STDIO tool execution
        logger.warning("mcp_stdio_not_implemented", server=server["name"])
        return MCPToolResult(
            success=False,
            result=None,
            error="STDIO transport not yet implemented"
        )
    
    def _execute_http_tool(
        self,
        server: MCPServerConfig,
        tool_name: str,
        parameters: Dict[str, Any]
    ) -> MCPToolResult:
        """Execute tool via HTTP transport."""
        try:
            url = server["url"]
            if not url:
                raise ValueError("HTTP server requires URL")
            
            # Make execution request
            response = requests.post(
                f"{url}/execute",
                json={
                    "tool": tool_name,
                    "parameters": parameters
                },
                timeout=self.settings.timeout
            )
            response.raise_for_status()
            
            # Parse result
            result_data = response.json()
            
            return MCPToolResult(
                success=result_data.get("success", False),
                result=result_data.get("result"),
                error=result_data.get("error")
            )
            
        except requests.RequestException as e:
            return MCPToolResult(
                success=False,
                result=None,
                error=f"HTTP request failed: {e}"
            )
    
    def get_all_tools(self) -> Dict[str, List[MCPTool]]:
        """
        Get all tools from all enabled MCP servers.
        
        Returns:
            Dictionary mapping server names to their tools
        """
        all_tools = {}
        enabled_servers = self.settings.get_enabled_servers()
        
        for server_name in enabled_servers.keys():
            try:
                tools = self.discover_tools(server_name)
                all_tools[server_name] = tools
            except Exception as e:
                logger.error(
                    "mcp_server_discovery_failed",
                    server=server_name,
                    error=str(e)
                )
        
        return all_tools


# Singleton instance
_mcp_client: Optional[MCPClient] = None


def get_mcp_client() -> MCPClient:
    """
    Get the singleton MCP client instance.
    
    Returns:
        MCPClient instance
        
    Example:
        >>> from tools.L2_foundation.mcp_client import get_mcp_client
        >>> client = get_mcp_client()
        >>> tools = client.discover_tools("supabase")
    """
    global _mcp_client
    
    if _mcp_client is None:
        _mcp_client = MCPClient()
    
    return _mcp_client


if __name__ == "__main__":
    # Test the MCP client
    print("🔍 Testing MCP Client...")
    print()
    
    client = get_mcp_client()
    
    print("✅ MCP Client initialized")
    print()
    
    # Get all tools
    print("📋 Discovering tools from enabled servers...")
    all_tools = client.get_all_tools()
    
    if not all_tools:
        print("⚠️  No enabled MCP servers found")
        print("   Enable servers in L1 config to use MCP tools")
    else:
        for server_name, tools in all_tools.items():
            print(f"\n🔧 {server_name}:")
            for tool in tools:
                print(f"  • {tool.name}: {tool.description}")
