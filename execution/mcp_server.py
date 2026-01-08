"""
MCP Server for Supabase Integration
Implements Model Context Protocol for agent-to-database communication
"""

import os
import json
import asyncio
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
import httpx
from pydantic import BaseModel, Field

load_dotenv()


class MCPTool(BaseModel):
    """MCP Tool definition"""
    name: str
    description: str
    input_schema: Dict[str, Any]


class MCPRequest(BaseModel):
    """MCP Request format"""
    jsonrpc: str = "2.0"
    id: str
    method: str
    params: Dict[str, Any] = Field(default_factory=dict)


class MCPResponse(BaseModel):
    """MCP Response format"""
    jsonrpc: str = "2.0"
    id: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None


class SupabaseMCPServer:
    """
    MCP Server for Supabase operations
    Exposes database operations as MCP tools
    """
    
    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_PROJECT_URL")
        self.access_token = os.getenv("SUPABASE_ACCESS_TOKEN")
        self.port = int(os.getenv("MCP_SERVER_PORT", "8080"))
        
        if not self.supabase_url or not self.access_token:
            raise ValueError("Missing SUPABASE_PROJECT_URL or SUPABASE_ACCESS_TOKEN")
        
        self.tools = self._register_tools()
    
    def _register_tools(self) -> List[MCPTool]:
        """Register available MCP tools"""
        return [
            MCPTool(
                name="query_table",
                description="Query data from a Supabase table with optional filters",
                input_schema={
                    "type": "object",
                    "properties": {
                        "table": {"type": "string", "description": "Table name"},
                        "select": {"type": "string", "description": "Columns to select (default: *)"},
                        "filters": {"type": "object", "description": "Filter conditions"},
                        "limit": {"type": "integer", "description": "Max rows to return"}
                    },
                    "required": ["table"]
                }
            ),
            MCPTool(
                name="insert_record",
                description="Insert a new record into a table",
                input_schema={
                    "type": "object",
                    "properties": {
                        "table": {"type": "string", "description": "Table name"},
                        "data": {"type": "object", "description": "Record data"}
                    },
                    "required": ["table", "data"]
                }
            ),
            MCPTool(
                name="update_record",
                description="Update existing records in a table",
                input_schema={
                    "type": "object",
                    "properties": {
                        "table": {"type": "string", "description": "Table name"},
                        "filters": {"type": "object", "description": "Filter conditions"},
                        "data": {"type": "object", "description": "Updated data"}
                    },
                    "required": ["table", "filters", "data"]
                }
            ),
            MCPTool(
                name="delete_record",
                description="Delete records from a table",
                input_schema={
                    "type": "object",
                    "properties": {
                        "table": {"type": "string", "description": "Table name"},
                        "filters": {"type": "object", "description": "Filter conditions"}
                    },
                    "required": ["table", "filters"]
                }
            ),
            MCPTool(
                name="get_schema",
                description="Get table schema information",
                input_schema={
                    "type": "object",
                    "properties": {
                        "table": {"type": "string", "description": "Table name"}
                    },
                    "required": ["table"]
                }
            ),
            MCPTool(
                name="batch_operations",
                description="Execute multiple operations in parallel",
                input_schema={
                    "type": "object",
                    "properties": {
                        "operations": {
                            "type": "array",
                            "description": "List of operations to execute",
                            "items": {"type": "object"}
                        }
                    },
                    "required": ["operations"]
                }
            )
        ]
    
    async def execute_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool and return results"""
        try:
            if tool_name == "query_table":
                return await self._query_table(**params)
            elif tool_name == "insert_record":
                return await self._insert_record(**params)
            elif tool_name == "update_record":
                return await self._update_record(**params)
            elif tool_name == "delete_record":
                return await self._delete_record(**params)
            elif tool_name == "get_schema":
                return await self._get_schema(**params)
            elif tool_name == "batch_operations":
                return await self._batch_operations(**params)
            else:
                raise ValueError(f"Unknown tool: {tool_name}")
        except Exception as e:
            return {"error": str(e), "tool": tool_name}
    
    async def _query_table(
        self, 
        table: str, 
        select: str = "*", 
        filters: Optional[Dict] = None, 
        limit: Optional[int] = None
    ) -> Dict[str, Any]:
        """Query table via Supabase REST API"""
        url = f"{self.supabase_url}/rest/v1/{table}"
        headers = {
            "apikey": self.access_token,
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        params = {"select": select}
        if limit:
            params["limit"] = limit
        
        # Add filters to query params
        if filters:
            for key, value in filters.items():
                params[key] = f"eq.{value}"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            return {"data": response.json(), "count": len(response.json())}
    
    async def _insert_record(self, table: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Insert record via Supabase REST API"""
        url = f"{self.supabase_url}/rest/v1/{table}"
        headers = {
            "apikey": self.access_token,
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data)
            response.raise_for_status()
            return {"data": response.json(), "status": "inserted"}
    
    async def _update_record(
        self, 
        table: str, 
        filters: Dict[str, Any], 
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update records via Supabase REST API"""
        url = f"{self.supabase_url}/rest/v1/{table}"
        headers = {
            "apikey": self.access_token,
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
        
        params = {}
        for key, value in filters.items():
            params[key] = f"eq.{value}"
        
        async with httpx.AsyncClient() as client:
            response = await client.patch(url, headers=headers, params=params, json=data)
            response.raise_for_status()
            return {"data": response.json(), "status": "updated"}
    
    async def _delete_record(self, table: str, filters: Dict[str, Any]) -> Dict[str, Any]:
        """Delete records via Supabase REST API"""
        url = f"{self.supabase_url}/rest/v1/{table}"
        headers = {
            "apikey": self.access_token,
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        params = {}
        for key, value in filters.items():
            params[key] = f"eq.{value}"
        
        async with httpx.AsyncClient() as client:
            response = await client.delete(url, headers=headers, params=params)
            response.raise_for_status()
            return {"status": "deleted", "filters": filters}
    
    async def _get_schema(self, table: str) -> Dict[str, Any]:
        """Get table schema information"""
        # This would typically query Supabase's metadata tables
        # For now, return a placeholder
        return {
            "table": table,
            "schema": "public",
            "note": "Schema introspection requires additional Supabase API calls"
        }
    
    async def _batch_operations(self, operations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute multiple operations in parallel"""
        tasks = []
        for op in operations:
            tool_name = op.get("tool")
            params = op.get("params", {})
            tasks.append(self.execute_tool(tool_name, params))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return {
            "results": results,
            "total": len(results),
            "successful": sum(1 for r in results if not isinstance(r, Exception))
        }
    
    async def handle_request(self, request: MCPRequest) -> MCPResponse:
        """Handle incoming MCP request"""
        try:
            if request.method == "tools/list":
                result = {"tools": [tool.dict() for tool in self.tools]}
            elif request.method == "tools/call":
                tool_name = request.params.get("name")
                tool_params = request.params.get("arguments", {})
                result = await self.execute_tool(tool_name, tool_params)
            else:
                raise ValueError(f"Unknown method: {request.method}")
            
            return MCPResponse(id=request.id, result=result)
        except Exception as e:
            return MCPResponse(
                id=request.id,
                error={"code": -32603, "message": str(e)}
            )
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """List all available tools"""
        return [tool.dict() for tool in self.tools]


async def main():
    """Main entry point for MCP server"""
    server = SupabaseMCPServer()
    print(f"🚀 Supabase MCP Server initialized")
    print(f"📍 Supabase URL: {server.supabase_url}")
    print(f"🔧 Available tools: {len(server.tools)}")
    print("\nTools:")
    for tool in server.tools:
        print(f"  - {tool.name}: {tool.description}")
    
    # For testing: demonstrate tool execution
    print("\n✅ Server ready for MCP requests")
    print("Use mcp_client.py to interact with this server")


if __name__ == "__main__":
    asyncio.run(main())
