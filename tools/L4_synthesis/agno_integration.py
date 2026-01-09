"""
L4 Synthesis: Agno Agent Integration
Integrates Phidata (Agno) agents with the Antigravity multi-agent system.
Following the 4-Layer Hierarchy: L4 = Synthesis (Depends on L1, L2, L3)
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools import Toolkit

from tools.L1_config.llm_client import get_gemini_model
from tools.L1_config.logging_config import get_logger
from tools.L2_foundation.agent_helpers import AgentRole, AgentTask
from tools.L2_foundation.mcp_client import get_mcp_client, MCPTool

logger = get_logger(__name__)


class MCPToolkit(Toolkit):
    """
    Phidata Toolkit that wraps MCP tools.
    
    This allows Agno agents to use MCP tools seamlessly.
    """
    
    def __init__(self, server_name: str):
        """
        Initialize MCP toolkit for a specific server.
        
        Args:
            server_name: Name of the MCP server
        """
        super().__init__(name=f"mcp_{server_name}")
        self.server_name = server_name
        self.mcp_client = get_mcp_client()
        self._tools_cache: List[MCPTool] = []
    
    def register(self, agent: Agent):
        """Register MCP tools with the Agno agent."""
        # Discover tools from MCP server
        try:
            tools = self.mcp_client.discover_tools(self.server_name)
            self._tools_cache = tools
            
            # Convert MCP tools to Phidata functions
            for tool in tools:
                self._register_mcp_tool(agent, tool)
            
            logger.info(
                "mcp_toolkit_registered",
                server=self.server_name,
                tool_count=len(tools)
            )
        except Exception as e:
            logger.error(
                "mcp_toolkit_registration_failed",
                server=self.server_name,
                error=str(e)
            )
    
    def _register_mcp_tool(self, agent: Agent, tool: MCPTool):
        """Register a single MCP tool as a Phidata function."""
        def mcp_tool_wrapper(**kwargs):
            """Wrapper function for MCP tool execution."""
            result = self.mcp_client.execute_tool(
                self.server_name,
                tool.name,
                kwargs
            )
            if result.success:
                return result.result
            else:
                raise Exception(result.error)
        
        # Set function metadata
        mcp_tool_wrapper.__name__ = tool.name
        mcp_tool_wrapper.__doc__ = tool.description
        
        # Add to agent's functions
        if not hasattr(agent, '_mcp_functions'):
            agent._mcp_functions = []
        agent._mcp_functions.append(mcp_tool_wrapper)


@dataclass
class AgnoAgentConfig:
    """Configuration for an Agno agent."""
    role: AgentRole
    name: str
    description: str
    instructions: List[str]
    mcp_servers: List[str]  # MCP servers this agent can use
    model_name: str = "gemini-1.5-flash"
    temperature: float = 0.7
    max_tokens: int = 4096


class AgnoAgentWrapper:
    """
    Wrapper for Phidata (Agno) agents integrated with Antigravity.
    
    Provides:
    - Gemini-powered Agno agents
    - MCP tool integration
    - Role-based configuration
    - Task execution
    
    Example:
        >>> config = AgnoAgentConfig(
        ...     role=AgentRole.DATABASE,
        ...     name="Database Specialist",
        ...     description="Handles database operations",
        ...     instructions=["Use Supabase for all database operations"],
        ...     mcp_servers=["supabase"]
        ... )
        >>> wrapper = AgnoAgentWrapper(config)
        >>> result = wrapper.execute_task("Create users table")
    """
    
    def __init__(self, config: AgnoAgentConfig):
        """
        Initialize Agno agent wrapper.
        
        Args:
            config: Agent configuration
        """
        self.config = config
        self.agent = self._create_agent()
        
        logger.info(
            "agno_agent_created",
            role=config.role.value,
            name=config.name
        )
    
    def _create_agent(self) -> Agent:
        """Create the Phidata agent."""
        # Create Gemini model for Agno
        model = Gemini(
            id=self.config.model_name,
            api_key=None,  # Will use environment variable
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )
        
        # Create agent
        agent = Agent(
            name=self.config.name,
            role=self.config.description,
            model=model,
            instructions=self.config.instructions,
            markdown=True,
            show_tool_calls=True,
            debug_mode=False
        )
        
        # Register MCP toolkits
        for server_name in self.config.mcp_servers:
            toolkit = MCPToolkit(server_name)
            toolkit.register(agent)
        
        return agent
    
    def execute_task(
        self,
        task_description: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Execute a task using the Agno agent.
        
        Args:
            task_description: Description of the task
            context: Additional context
            
        Returns:
            Agent's response
        """
        logger.info(
            "agno_agent_executing_task",
            role=self.config.role.value,
            task=task_description
        )
        
        # Build prompt with context
        prompt = task_description
        if context:
            context_str = "\n".join([f"{k}: {v}" for k, v in context.items()])
            prompt = f"{task_description}\n\nContext:\n{context_str}"
        
        try:
            # Execute with Agno agent
            response = self.agent.run(prompt)
            
            logger.info(
                "agno_agent_task_completed",
                role=self.config.role.value,
                task=task_description
            )
            
            return response.content
            
        except Exception as e:
            logger.error(
                "agno_agent_task_failed",
                role=self.config.role.value,
                task=task_description,
                error=str(e)
            )
            raise
    
    def chat(self, message: str) -> str:
        """
        Chat with the agent.
        
        Args:
            message: User message
            
        Returns:
            Agent's response
        """
        response = self.agent.run(message)
        return response.content


# Pre-configured Agno agents for each role
AGNO_AGENT_CONFIGS = {
    AgentRole.DATABASE: AgnoAgentConfig(
        role=AgentRole.DATABASE,
        name="Database Specialist",
        description="Expert in database design, Supabase, and data modeling",
        instructions=[
            "You are a database specialist in the Antigravity system.",
            "Follow the 4-Layer Hierarchy: L1 (config) → L2 (foundation) → L3 (analysis).",
            "Use Supabase for all database operations.",
            "Design schemas with proper types, constraints, and RLS policies.",
            "Always consider data quality and validation."
        ],
        mcp_servers=["supabase"],  # Will be enabled when MCP server is created
        model_name="gemini-1.5-flash"
    ),
    
    AgentRole.AI: AgnoAgentConfig(
        role=AgentRole.AI,
        name="AI Specialist",
        description="Expert in LLM integration, embeddings, and AI features",
        instructions=[
            "You are an AI/LLM specialist in the Antigravity system.",
            "Follow the 4-Layer Hierarchy: L2 (foundation) → L3 (analysis).",
            "Use Gemini for all LLM operations.",
            "Design effective prompts and handle AI responses.",
            "Consider embeddings and semantic search when appropriate."
        ],
        mcp_servers=[],
        model_name="gemini-1.5-pro"  # Use Pro for AI tasks
    ),
    
    AgentRole.API: AgnoAgentConfig(
        role=AgentRole.API,
        name="API Integration Specialist",
        description="Expert in API design, integrations, and webhooks",
        instructions=[
            "You are an API integration specialist in the Antigravity system.",
            "Work at L4 (synthesis) layer.",
            "Design RESTful APIs following best practices.",
            "Handle third-party integrations securely.",
            "Implement proper error handling and logging."
        ],
        mcp_servers=["web_search"],  # Will be enabled when MCP server is created
        model_name="gemini-1.5-flash"
    ),
    
    AgentRole.QA: AgnoAgentConfig(
        role=AgentRole.QA,
        name="Quality Assurance Specialist",
        description="Expert in testing, documentation, and code quality",
        instructions=[
            "You are a QA specialist in the Antigravity system.",
            "Enforce the 10 Commandments Quality Rubric.",
            "Write comprehensive tests (pytest).",
            "Create clear documentation.",
            "Review code for SOLID principles and best practices."
        ],
        mcp_servers=["filesystem"],  # Will be enabled when MCP server is created
        model_name="gemini-1.5-flash"
    ),
}


def get_agno_agent(role: AgentRole) -> AgnoAgentWrapper:
    """
    Get an Agno agent for a specific role.
    
    Args:
        role: The agent role
        
    Returns:
        AgnoAgentWrapper instance
        
    Example:
        >>> agent = get_agno_agent(AgentRole.DATABASE)
        >>> result = agent.execute_task("Design a users table")
    """
    config = AGNO_AGENT_CONFIGS.get(role)
    if not config:
        raise ValueError(f"No Agno agent configuration for role: {role}")
    
    return AgnoAgentWrapper(config)


if __name__ == "__main__":
    # Test Agno integration
    print("🔍 Testing Agno Agent Integration...")
    print()
    
    # Create a database agent
    print("Creating Database Specialist agent...")
    db_agent = get_agno_agent(AgentRole.DATABASE)
    print(f"✅ Agent created: {db_agent.config.name}")
    print()
    
    # Test task execution
    print("Testing task execution...")
    try:
        result = db_agent.execute_task(
            "Explain the best practices for designing a users table in Supabase",
            context={"framework": "Supabase", "language": "Python"}
        )
        print("Response:")
        print(result)
    except Exception as e:
        print(f"Error: {e}")
