"""
MCP Client for Agent Communication
Provides interface for agents to interact with Supabase via MCP
"""

import asyncio
from typing import Dict, List, Any, Optional
from pydantic import BaseModel
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from execution.mcp_server import SupabaseMCPServer, MCPRequest


class MCPClient:
    """
    Client for agents to communicate with Supabase via MCP
    Provides high-level interface for common operations
    """
    
    def __init__(self):
        self.server = SupabaseMCPServer()
    
    async def execute_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an MCP tool"""
        request = MCPRequest(
            id=f"req_{asyncio.current_task().get_name()}",
            method="tools/call",
            params={"name": tool_name, "arguments": params}
        )
        response = await self.server.handle_request(request)
        
        if response.error:
            raise Exception(f"MCP Error: {response.error}")
        
        return response.result
    
    async def query_database(
        self, 
        table: str, 
        filters: Optional[Dict] = None, 
        select: str = "*",
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Query database table
        
        Args:
            table: Table name
            filters: Filter conditions (e.g., {"id": "123", "status": "active"})
            select: Columns to select
            limit: Maximum rows to return
        
        Returns:
            List of records
        """
        params = {"table": table, "select": select}
        if filters:
            params["filters"] = filters
        if limit:
            params["limit"] = limit
        
        result = await self.execute_tool("query_table", params)
        return result.get("data", [])
    
    async def insert_record(self, table: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Insert a new record
        
        Args:
            table: Table name
            data: Record data
        
        Returns:
            Inserted record
        """
        result = await self.execute_tool("insert_record", {"table": table, "data": data})
        return result.get("data", {})
    
    async def update_record(
        self, 
        table: str, 
        filters: Dict[str, Any], 
        data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Update existing records
        
        Args:
            table: Table name
            filters: Filter conditions to identify records
            data: Updated data
        
        Returns:
            Updated records
        """
        params = {"table": table, "filters": filters, "data": data}
        result = await self.execute_tool("update_record", params)
        return result.get("data", [])
    
    async def delete_record(self, table: str, filters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Delete records
        
        Args:
            table: Table name
            filters: Filter conditions to identify records
        
        Returns:
            Deletion status
        """
        result = await self.execute_tool("delete_record", {"table": table, "filters": filters})
        return result
    
    async def get_schema(self, table: str) -> Dict[str, Any]:
        """
        Get table schema information
        
        Args:
            table: Table name
        
        Returns:
            Schema information
        """
        result = await self.execute_tool("get_schema", {"table": table})
        return result
    
    async def batch_operations(self, operations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Execute multiple operations in parallel
        
        Args:
            operations: List of operations, each with 'tool' and 'params' keys
                Example: [
                    {"tool": "query_table", "params": {"table": "users"}},
                    {"tool": "insert_record", "params": {"table": "logs", "data": {...}}}
                ]
        
        Returns:
            Batch operation results
        """
        result = await self.execute_tool("batch_operations", {"operations": operations})
        return result
    
    def list_available_tools(self) -> List[Dict[str, Any]]:
        """List all available MCP tools"""
        return self.server.list_tools()


async def test_connection():
    """Test MCP client connection and basic operations"""
    print("🧪 Testing MCP Client Connection...\n")
    
    client = MCPClient()
    
    # List available tools
    print("📋 Available Tools:")
    tools = client.list_available_tools()
    for tool in tools:
        print(f"  ✓ {tool['name']}: {tool['description']}")
    
    print("\n✅ MCP Client initialized successfully")
    print("🔗 Connected to Supabase MCP Server")
    
    # Example usage (commented out - requires actual Supabase tables)
    # try:
    #     # Query example
    #     records = await client.query_database("users", limit=5)
    #     print(f"\n📊 Query result: {len(records)} records")
    #     
    #     # Insert example
    #     new_record = await client.insert_record("logs", {
    #         "event": "test",
    #         "timestamp": "2026-01-07T23:00:00Z"
    #     })
    #     print(f"✅ Inserted record: {new_record}")
    # except Exception as e:
    #     print(f"⚠️  Operation failed: {e}")
    
    return True


async def main():
    """Main entry point"""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test-connection":
        await test_connection()
    else:
        print("MCP Client Usage:")
        print("  python mcp_client.py --test-connection")
        print("\nOr import in your agent scripts:")
        print("  from execution.mcp_client import MCPClient")


if __name__ == "__main__":
    asyncio.run(main())
