"""
L2 Foundation: Agent Helpers
Provides helper functions for multi-agent coordination using Gemini.
Following the 4-Layer Hierarchy: L2 = Foundation (Depends only on L1)
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

from tools.L1_config.llm_client import get_gemini_model
from tools.L1_config.logging_config import get_logger

logger = get_logger(__name__)


class AgentRole(str, Enum):
    """Agent roles in the multi-agent system."""
    DATABASE = "Agent-Database"
    AI = "Agent-AI"
    API = "Agent-API"
    QA = "Agent-QA"
    ORCHESTRATOR = "Agent-Orchestrator"


@dataclass
class AgentTask:
    """Represents a task for an agent."""
    id: str
    description: str
    assigned_to: AgentRole
    status: str  # "pending", "in_progress", "complete", "blocked"
    dependencies: List[str]  # Task IDs this depends on
    result: Optional[Any] = None
    error: Optional[str] = None


@dataclass
class AgentMessage:
    """Message between agents."""
    from_agent: AgentRole
    to_agent: AgentRole
    content: str
    task_id: Optional[str] = None


class AgentHelper:
    """
    Helper for multi-agent coordination using Gemini.
    
    Provides utilities for:
    - Task decomposition
    - Agent communication
    - Decision making
    - Tool selection
    
    Example:
        >>> helper = AgentHelper(AgentRole.ORCHESTRATOR)
        >>> tasks = helper.decompose_task("Build user authentication")
        >>> decision = helper.make_decision("Which database to use?", ["Supabase", "PostgreSQL"])
    """
    
    def __init__(self, role: AgentRole, model_name: str = "gemini-1.5-flash"):
        """
        Initialize agent helper.
        
        Args:
            role: The agent's role
            model_name: Gemini model to use
        """
        self.role = role
        self.model = get_gemini_model(model_name)
        self.conversation_history: List[Dict[str, str]] = []
        
        logger.info("agent_helper_initialized", role=role.value, model=model_name)
    
    def decompose_task(
        self,
        task_description: str,
        context: Optional[str] = None
    ) -> List[AgentTask]:
        """
        Decompose a high-level task into subtasks for different agents.
        
        Args:
            task_description: Description of the task to decompose
            context: Additional context about the system/project
            
        Returns:
            List of AgentTask objects
            
        Example:
            >>> tasks = helper.decompose_task(
            ...     "Build user authentication system",
            ...     context="Using Supabase for database"
            ... )
        """
        logger.info("agent_decomposing_task", task=task_description)
        
        prompt = f"""You are a {self.role.value} in a multi-agent system following the 4-Layer Hierarchy architecture.

Task to decompose: {task_description}

{f"Context: {context}" if context else ""}

Available agent roles:
- Agent-Database: Database schemas, data models, Supabase (L1-L3)
- Agent-AI: AI/LLM features, prompts, embeddings (L2-L3)
- Agent-API: API endpoints, integrations, webhooks (L4)
- Agent-QA: Testing, documentation, quality assurance

Decompose this task into specific subtasks for each agent role.
For each subtask, provide:
1. A unique ID (e.g., "db-1", "ai-1")
2. Clear description
3. Which agent role should handle it
4. Any dependencies on other subtasks

Format your response as JSON:
{{
  "tasks": [
    {{
      "id": "task-id",
      "description": "Task description",
      "assigned_to": "Agent-Database",
      "dependencies": ["other-task-id"]
    }}
  ]
}}
"""
        
        try:
            response = self.model.generate_content(prompt)
            # Parse JSON response
            import json
            # Extract JSON from response (handle markdown code blocks)
            text = response.text
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            
            data = json.loads(text.strip())
            
            # Convert to AgentTask objects
            tasks = []
            for task_data in data.get("tasks", []):
                task = AgentTask(
                    id=task_data["id"],
                    description=task_data["description"],
                    assigned_to=AgentRole(task_data["assigned_to"]),
                    status="pending",
                    dependencies=task_data.get("dependencies", [])
                )
                tasks.append(task)
            
            logger.info(
                "agent_task_decomposed",
                task=task_description,
                subtask_count=len(tasks)
            )
            
            return tasks
            
        except Exception as e:
            logger.error(
                "agent_task_decomposition_failed",
                task=task_description,
                error=str(e)
            )
            # Return a single task as fallback
            return [AgentTask(
                id="fallback-1",
                description=task_description,
                assigned_to=self.role,
                status="pending",
                dependencies=[]
            )]
    
    def make_decision(
        self,
        question: str,
        options: List[str],
        context: Optional[str] = None
    ) -> str:
        """
        Make a decision using Gemini.
        
        Args:
            question: The decision question
            options: List of possible options
            context: Additional context
            
        Returns:
            The chosen option
            
        Example:
            >>> decision = helper.make_decision(
            ...     "Which database should we use?",
            ...     ["Supabase", "PostgreSQL", "MongoDB"],
            ...     context="Need real-time features"
            ... )
        """
        logger.info("agent_making_decision", question=question)
        
        prompt = f"""You are a {self.role.value} making a technical decision.

Question: {question}

Options:
{chr(10).join(f"- {opt}" for opt in options)}

{f"Context: {context}" if context else ""}

Choose the best option and explain your reasoning briefly.
Format: "DECISION: [option] - [brief reasoning]"
"""
        
        try:
            response = self.model.generate_content(prompt)
            decision_text = response.text.strip()
            
            # Extract the decision
            if "DECISION:" in decision_text:
                decision = decision_text.split("DECISION:")[1].split("-")[0].strip()
            else:
                # Fallback: find which option appears in the response
                decision = next(
                    (opt for opt in options if opt.lower() in decision_text.lower()),
                    options[0]
                )
            
            logger.info(
                "agent_decision_made",
                question=question,
                decision=decision
            )
            
            return decision
            
        except Exception as e:
            logger.error(
                "agent_decision_failed",
                question=question,
                error=str(e)
            )
            # Return first option as fallback
            return options[0]
    
    def select_tool(
        self,
        task: str,
        available_tools: List[Dict[str, str]]
    ) -> Optional[str]:
        """
        Select the best tool for a task.
        
        Args:
            task: Description of the task
            available_tools: List of tools with name and description
            
        Returns:
            Name of the selected tool, or None
            
        Example:
            >>> tools = [
            ...     {"name": "query_database", "description": "Query Supabase tables"},
            ...     {"name": "search_web", "description": "Search the internet"}
            ... ]
            >>> tool = helper.select_tool("Get user data", tools)
        """
        logger.info("agent_selecting_tool", task=task)
        
        if not available_tools:
            return None
        
        prompt = f"""You are a {self.role.value} selecting the best tool for a task.

Task: {task}

Available tools:
{chr(10).join(f"- {t['name']}: {t['description']}" for t in available_tools)}

Which tool is best for this task? Respond with just the tool name, or "NONE" if no tool is suitable.
"""
        
        try:
            response = self.model.generate_content(prompt)
            tool_name = response.text.strip().split()[0]  # Get first word
            
            # Validate it's a real tool
            tool_names = [t["name"] for t in available_tools]
            if tool_name in tool_names:
                logger.info(
                    "agent_tool_selected",
                    task=task,
                    tool=tool_name
                )
                return tool_name
            
            return None
            
        except Exception as e:
            logger.error(
                "agent_tool_selection_failed",
                task=task,
                error=str(e)
            )
            return None
    
    def generate_prompt(
        self,
        task: str,
        role_specific_context: Optional[str] = None
    ) -> str:
        """
        Generate a role-specific prompt for a task.
        
        Args:
            task: The task description
            role_specific_context: Additional context for this role
            
        Returns:
            Generated prompt
        """
        base_context = {
            AgentRole.DATABASE: "You are a database specialist. Focus on schema design, data modeling, and Supabase integration.",
            AgentRole.AI: "You are an AI/LLM specialist. Focus on prompt engineering, embeddings, and AI features.",
            AgentRole.API: "You are an API integration specialist. Focus on REST endpoints, webhooks, and third-party integrations.",
            AgentRole.QA: "You are a quality assurance specialist. Focus on testing, documentation, and code quality.",
            AgentRole.ORCHESTRATOR: "You are the orchestrator. Coordinate between agents and manage the overall workflow."
        }
        
        context = base_context.get(self.role, "")
        if role_specific_context:
            context += f"\n\n{role_specific_context}"
        
        prompt = f"""{context}

Task: {task}

Follow the 4-Layer Hierarchy:
- L1: Configuration (constants, types)
- L2: Foundation (validation, data quality)
- L3: Analysis (business logic)
- L4: Synthesis (integration, reporting)

Provide a clear, actionable response.
"""
        
        return prompt


def get_agent_helper(role: AgentRole, model_name: str = "gemini-1.5-flash") -> AgentHelper:
    """
    Get an agent helper instance.
    
    Args:
        role: The agent role
        model_name: Gemini model to use
        
    Returns:
        AgentHelper instance
    """
    return AgentHelper(role, model_name)


if __name__ == "__main__":
    # Test the agent helper
    print("🔍 Testing Agent Helper...")
    print()
    
    # Test as orchestrator
    helper = get_agent_helper(AgentRole.ORCHESTRATOR)
    print(f"✅ Agent Helper initialized as {helper.role.value}")
    print()
    
    # Test task decomposition
    print("📋 Testing task decomposition...")
    tasks = helper.decompose_task(
        "Build a user authentication system",
        context="Using Supabase for database, Gemini for AI features"
    )
    
    print(f"Decomposed into {len(tasks)} tasks:")
    for task in tasks:
        print(f"  • [{task.id}] {task.assigned_to.value}: {task.description}")
        if task.dependencies:
            print(f"    Dependencies: {', '.join(task.dependencies)}")
    print()
    
    # Test decision making
    print("🤔 Testing decision making...")
    decision = helper.make_decision(
        "Which database should we use?",
        ["Supabase", "PostgreSQL", "MongoDB"],
        context="Need real-time features and easy setup"
    )
    print(f"Decision: {decision}")
