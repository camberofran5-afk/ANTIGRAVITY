"""
Centralized Orchestrator
Manages agent communication and task routing
"""

import asyncio
import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from execution.mcp_client import MCPClient


class AgentMessage:
    """Standard message format for agent communication"""
    
    def __init__(
        self,
        agent_id: str,
        message_type: str,
        payload: Dict[str, Any],
        priority: str = "medium"
    ):
        self.agent_id = agent_id
        self.timestamp = datetime.utcnow().isoformat()
        self.message_type = message_type  # request|response|error|status
        self.payload = payload
        self.metadata = {
            "priority": priority,
            "retry_count": 0
        }
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "timestamp": self.timestamp,
            "message_type": self.message_type,
            "payload": self.payload,
            "metadata": self.metadata
        }


class Orchestrator:
    """
    Centralized orchestration engine
    Routes tasks to agents and manages execution flow
    """
    
    def __init__(self):
        self.mcp_client = MCPClient()
        self.agent_registry = self._load_agent_registry()
        self.execution_log = []
        self.max_retries = 3
        
        # Create temp/logs directory
        self.log_dir = Path("/Users/franciscocambero/Anitgravity/temp/logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_agent_registry(self) -> Dict[str, Any]:
        """Load agent definitions from directives"""
        # In a full implementation, this would parse all agent directive files
        # For now, return a basic registry
        return {
            "data_processor": {
                "name": "Data Processor",
                "capabilities": ["data_validation", "data_transformation"],
                "layer": "L2"
            },
            "database_manager": {
                "name": "Database Manager",
                "capabilities": ["crud_operations", "schema_management"],
                "layer": "L1"
            }
        }
    
    async def route_task(
        self,
        task_type: str,
        task_data: Dict[str, Any],
        priority: str = "medium"
    ) -> Dict[str, Any]:
        """
        Route a task to the appropriate agent
        
        Args:
            task_type: Type of task (e.g., "data_validation", "crud_operation")
            task_data: Task parameters
            priority: Task priority (high|medium|low)
        
        Returns:
            Task execution result
        """
        # Find capable agent
        agent_id = self._find_agent_for_task(task_type)
        
        if not agent_id:
            return {
                "status": "error",
                "message": f"No agent found for task type: {task_type}"
            }
        
        # Create message
        message = AgentMessage(
            agent_id=agent_id,
            message_type="request",
            payload={"task_type": task_type, "data": task_data},
            priority=priority
        )
        
        # Execute with retry logic
        result = await self._execute_with_retry(message)
        
        # Log execution
        self._log_execution(message, result)
        
        return result
    
    def _find_agent_for_task(self, task_type: str) -> Optional[str]:
        """Find agent capable of handling task type"""
        for agent_id, agent_info in self.agent_registry.items():
            if task_type in agent_info.get("capabilities", []):
                return agent_id
        return None
    
    async def _execute_with_retry(
        self,
        message: AgentMessage,
        retry_count: int = 0
    ) -> Dict[str, Any]:
        """Execute task with automatic retry on failure"""
        try:
            # In a full implementation, this would call the actual agent
            # For now, demonstrate the pattern
            result = await self._execute_agent_task(message)
            return result
        except Exception as e:
            if retry_count < self.max_retries:
                print(f"⚠️  Retry {retry_count + 1}/{self.max_retries} for {message.agent_id}")
                message.metadata["retry_count"] = retry_count + 1
                await asyncio.sleep(2 ** retry_count)  # Exponential backoff
                return await self._execute_with_retry(message, retry_count + 1)
            else:
                # Trigger self-annealing
                await self._trigger_self_annealing(message, e)
                return {
                    "status": "error",
                    "message": str(e),
                    "agent_id": message.agent_id
                }
    
    async def _execute_agent_task(self, message: AgentMessage) -> Dict[str, Any]:
        """Execute the actual agent task"""
        # This is where agent-specific logic would be called
        # For database operations, use MCP client
        task_type = message.payload.get("task_type")
        task_data = message.payload.get("data", {})
        
        if task_type == "crud_operation":
            operation = task_data.get("operation")
            if operation == "query":
                result = await self.mcp_client.query_database(
                    table=task_data.get("table"),
                    filters=task_data.get("filters"),
                    limit=task_data.get("limit")
                )
                return {"status": "success", "data": result}
            elif operation == "insert":
                result = await self.mcp_client.insert_record(
                    table=task_data.get("table"),
                    data=task_data.get("data")
                )
                return {"status": "success", "data": result}
        
        return {"status": "success", "message": "Task executed"}
    
    async def _trigger_self_annealing(self, message: AgentMessage, error: Exception):
        """Trigger self-annealing protocol for error recovery"""
        from orchestration.error_handler import ErrorHandler
        
        error_handler = ErrorHandler()
        await error_handler.handle_error(
            agent_id=message.agent_id,
            error=error,
            context=message.to_dict()
        )
    
    def _log_execution(self, message: AgentMessage, result: Dict[str, Any]):
        """Log execution for observability"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "agent_id": message.agent_id,
            "message": message.to_dict(),
            "result": result
        }
        self.execution_log.append(log_entry)
        
        # Write to file
        log_file = self.log_dir / f"{datetime.utcnow().strftime('%Y-%m-%d')}.jsonl"
        with open(log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    
    async def execute_parallel_tasks(
        self,
        tasks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Execute multiple independent tasks in parallel"""
        task_coroutines = [
            self.route_task(
                task_type=task.get("task_type"),
                task_data=task.get("data", {}),
                priority=task.get("priority", "medium")
            )
            for task in tasks
        ]
        
        results = await asyncio.gather(*task_coroutines, return_exceptions=True)
        return results
    
    def get_agent_status(self, agent_id: str) -> Dict[str, Any]:
        """Get status of a specific agent"""
        if agent_id not in self.agent_registry:
            return {"status": "unknown", "message": "Agent not found"}
        
        # Count recent executions
        recent_executions = [
            log for log in self.execution_log
            if log["agent_id"] == agent_id
        ]
        
        return {
            "status": "active",
            "agent_id": agent_id,
            "info": self.agent_registry[agent_id],
            "recent_executions": len(recent_executions)
        }


async def main():
    """Test orchestrator"""
    print("🎭 Initializing Orchestrator...\n")
    
    orchestrator = Orchestrator()
    
    print("📋 Registered Agents:")
    for agent_id, info in orchestrator.agent_registry.items():
        print(f"  ✓ {agent_id}: {info['name']} (Layer {info['layer']})")
    
    print("\n✅ Orchestrator ready")
    print("Use this module to route tasks to agents")


if __name__ == "__main__":
    asyncio.run(main())
