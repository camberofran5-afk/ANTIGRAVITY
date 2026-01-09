"""
L3 Analysis: Agent Logic
Provides decision-making and reasoning logic for agents using Gemini.
Following the 4-Layer Hierarchy: L3 = Analysis (Depends on L1, L2)
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

from tools.L1_config.llm_client import get_gemini_model
from tools.L1_config.logging_config import get_logger
from tools.L2_foundation.agent_helpers import AgentRole, AgentTask, AgentHelper
from tools.L2_foundation.mcp_client import get_mcp_client, MCPTool

logger = get_logger(__name__)


class DecisionType(str, Enum):
    """Types of decisions an agent can make."""
    TOOL_SELECTION = "tool_selection"
    TASK_PRIORITIZATION = "task_prioritization"
    RESOURCE_ALLOCATION = "resource_allocation"
    ERROR_HANDLING = "error_handling"
    ARCHITECTURE_CHOICE = "architecture_choice"


@dataclass
class AgentDecision:
    """Represents a decision made by an agent."""
    decision_type: DecisionType
    question: str
    options: List[str]
    chosen_option: str
    reasoning: str
    confidence: float  # 0.0 to 1.0


class AgentLogic:
    """
    Core decision-making and reasoning logic for agents.
    
    Uses Gemini to make intelligent decisions about:
    - Which tools to use
    - How to prioritize tasks
    - How to handle errors
    - Architecture choices
    
    Example:
        >>> logic = AgentLogic(AgentRole.DATABASE)
        >>> decision = logic.decide_tool_for_task("Query user data")
        >>> tasks = logic.prioritize_tasks([task1, task2, task3])
    """
    
    def __init__(self, role: AgentRole, model_name: str = "gemini-1.5-flash"):
        """
        Initialize agent logic.
        
        Args:
            role: The agent's role
            model_name: Gemini model to use
        """
        self.role = role
        self.helper = AgentHelper(role, model_name)
        self.mcp_client = get_mcp_client()
        
        logger.info("agent_logic_initialized", role=role.value)
    
    def decide_tool_for_task(
        self,
        task_description: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Optional[AgentDecision]:
        """
        Decide which tool to use for a task.
        
        Args:
            task_description: Description of the task
            context: Additional context (current state, available data, etc.)
            
        Returns:
            AgentDecision with the chosen tool, or None if no tool needed
        """
        logger.info("agent_deciding_tool", task=task_description)
        
        # Get available MCP tools
        all_tools = self.mcp_client.get_all_tools()
        
        # Flatten to list of tool descriptions
        available_tools = []
        for server_name, tools in all_tools.items():
            for tool in tools:
                available_tools.append({
                    "name": f"{server_name}.{tool.name}",
                    "description": tool.description
                })
        
        if not available_tools:
            logger.info("agent_no_tools_available", task=task_description)
            return None
        
        # Use helper to select tool
        selected_tool = self.helper.select_tool(task_description, available_tools)
        
        if not selected_tool:
            return None
        
        # Create decision record
        decision = AgentDecision(
            decision_type=DecisionType.TOOL_SELECTION,
            question=f"Which tool to use for: {task_description}",
            options=[t["name"] for t in available_tools],
            chosen_option=selected_tool,
            reasoning=f"Selected based on task requirements and tool capabilities",
            confidence=0.8
        )
        
        logger.info(
            "agent_tool_decided",
            task=task_description,
            tool=selected_tool
        )
        
        return decision
    
    def prioritize_tasks(
        self,
        tasks: List[AgentTask],
        criteria: Optional[str] = None
    ) -> List[AgentTask]:
        """
        Prioritize a list of tasks.
        
        Args:
            tasks: List of tasks to prioritize
            criteria: Prioritization criteria (e.g., "urgency", "dependencies")
            
        Returns:
            Sorted list of tasks by priority
        """
        if not tasks:
            return []
        
        logger.info("agent_prioritizing_tasks", task_count=len(tasks))
        
        # Build prompt for Gemini
        task_list = "\n".join([
            f"{i+1}. [{t.id}] {t.description} (assigned to: {t.assigned_to.value}, dependencies: {t.dependencies})"
            for i, t in enumerate(tasks)
        ])
        
        prompt = f"""You are a {self.role.value} prioritizing tasks.

Tasks to prioritize:
{task_list}

{f"Criteria: {criteria}" if criteria else "Criteria: Consider dependencies, urgency, and logical order"}

Return the task IDs in priority order (highest priority first), one per line.
Just the IDs, no explanations.
"""
        
        try:
            model = get_gemini_model()
            response = model.generate_content(prompt)
            
            # Parse task IDs from response
            priority_ids = [
                line.strip().replace("[", "").replace("]", "")
                for line in response.text.strip().split("\n")
                if line.strip()
            ]
            
            # Reorder tasks based on priority
            task_map = {t.id: t for t in tasks}
            prioritized = []
            
            for task_id in priority_ids:
                if task_id in task_map:
                    prioritized.append(task_map[task_id])
            
            # Add any tasks that weren't in the response
            for task in tasks:
                if task not in prioritized:
                    prioritized.append(task)
            
            logger.info(
                "agent_tasks_prioritized",
                original_order=[t.id for t in tasks],
                new_order=[t.id for t in prioritized]
            )
            
            return prioritized
            
        except Exception as e:
            logger.error(
                "agent_prioritization_failed",
                error=str(e)
            )
            # Return original order as fallback
            return tasks
    
    def handle_error(
        self,
        error: Exception,
        context: Dict[str, Any]
    ) -> AgentDecision:
        """
        Decide how to handle an error.
        
        Args:
            error: The error that occurred
            context: Context about what was being done
            
        Returns:
            AgentDecision with error handling strategy
        """
        logger.info("agent_handling_error", error=str(error))
        
        error_type = type(error).__name__
        error_message = str(error)
        
        # Define possible error handling strategies
        strategies = [
            "retry_with_backoff",
            "use_alternative_approach",
            "escalate_to_user",
            "skip_and_continue",
            "rollback_changes"
        ]
        
        # Use Gemini to decide strategy
        decision_text = self.helper.make_decision(
            f"How to handle {error_type}: {error_message}",
            strategies,
            context=f"Context: {context}"
        )
        
        # Find which strategy was chosen
        chosen_strategy = next(
            (s for s in strategies if s in decision_text.lower()),
            "escalate_to_user"  # Safe default
        )
        
        decision = AgentDecision(
            decision_type=DecisionType.ERROR_HANDLING,
            question=f"How to handle error: {error_type}",
            options=strategies,
            chosen_option=chosen_strategy,
            reasoning=decision_text,
            confidence=0.7
        )
        
        logger.info(
            "agent_error_strategy_decided",
            error=error_type,
            strategy=chosen_strategy
        )
        
        return decision
    
    def choose_architecture(
        self,
        requirement: str,
        options: List[Dict[str, str]]
    ) -> AgentDecision:
        """
        Make an architecture decision.
        
        Args:
            requirement: The requirement to satisfy
            options: List of architecture options with pros/cons
            
        Returns:
            AgentDecision with chosen architecture
        """
        logger.info("agent_choosing_architecture", requirement=requirement)
        
        # Format options for Gemini
        options_text = "\n".join([
            f"{i+1}. {opt['name']}\n   Pros: {opt.get('pros', 'N/A')}\n   Cons: {opt.get('cons', 'N/A')}"
            for i, opt in enumerate(options)
        ])
        
        prompt = f"""You are a {self.role.value} making an architecture decision.

Requirement: {requirement}

Options:
{options_text}

Choose the best option and explain your reasoning.
Consider: scalability, maintainability, performance, and alignment with the 4-Layer Hierarchy.

Format: "CHOICE: [option name] - [reasoning]"
"""
        
        try:
            model = get_gemini_model()
            response = model.generate_content(prompt)
            
            response_text = response.text.strip()
            
            # Extract choice
            if "CHOICE:" in response_text:
                parts = response_text.split("CHOICE:")[1].split("-", 1)
                chosen = parts[0].strip()
                reasoning = parts[1].strip() if len(parts) > 1 else "See response"
            else:
                # Fallback: find which option name appears
                chosen = next(
                    (opt["name"] for opt in options if opt["name"].lower() in response_text.lower()),
                    options[0]["name"]
                )
                reasoning = response_text
            
            decision = AgentDecision(
                decision_type=DecisionType.ARCHITECTURE_CHOICE,
                question=requirement,
                options=[opt["name"] for opt in options],
                chosen_option=chosen,
                reasoning=reasoning,
                confidence=0.85
            )
            
            logger.info(
                "agent_architecture_decided",
                requirement=requirement,
                choice=chosen
            )
            
            return decision
            
        except Exception as e:
            logger.error(
                "agent_architecture_decision_failed",
                error=str(e)
            )
            # Return first option as fallback
            return AgentDecision(
                decision_type=DecisionType.ARCHITECTURE_CHOICE,
                question=requirement,
                options=[opt["name"] for opt in options],
                chosen_option=options[0]["name"],
                reasoning=f"Fallback choice due to error: {e}",
                confidence=0.5
            )


def get_agent_logic(role: AgentRole, model_name: str = "gemini-1.5-flash") -> AgentLogic:
    """
    Get an agent logic instance.
    
    Args:
        role: The agent role
        model_name: Gemini model to use
        
    Returns:
        AgentLogic instance
    """
    return AgentLogic(role, model_name)


if __name__ == "__main__":
    # Test the agent logic
    print("🔍 Testing Agent Logic...")
    print()
    
    # Test as Database agent
    logic = get_agent_logic(AgentRole.DATABASE)
    print(f"✅ Agent Logic initialized as {logic.role.value}")
    print()
    
    # Test task prioritization
    print("📋 Testing task prioritization...")
    test_tasks = [
        AgentTask(
            id="db-1",
            description="Create users table schema",
            assigned_to=AgentRole.DATABASE,
            status="pending",
            dependencies=[]
        ),
        AgentTask(
            id="db-2",
            description="Add RLS policies",
            assigned_to=AgentRole.DATABASE,
            status="pending",
            dependencies=["db-1"]
        ),
        AgentTask(
            id="db-3",
            description="Create indexes",
            assigned_to=AgentRole.DATABASE,
            status="pending",
            dependencies=["db-1"]
        ),
    ]
    
    prioritized = logic.prioritize_tasks(test_tasks)
    print("Prioritized order:")
    for i, task in enumerate(prioritized, 1):
        print(f"  {i}. [{task.id}] {task.description}")
    print()
    
    # Test architecture decision
    print("🏗️  Testing architecture decision...")
    decision = logic.choose_architecture(
        "Choose database for user authentication",
        [
            {
                "name": "Supabase",
                "pros": "Built-in auth, real-time, easy setup",
                "cons": "Vendor lock-in"
            },
            {
                "name": "PostgreSQL",
                "pros": "Full control, mature, flexible",
                "cons": "More setup required"
            }
        ]
    )
    print(f"Decision: {decision.chosen_option}")
    print(f"Reasoning: {decision.reasoning}")
