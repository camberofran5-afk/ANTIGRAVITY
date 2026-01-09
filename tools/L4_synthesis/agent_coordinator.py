"""
L4 Synthesis: Agent Coordinator
Orchestrates multi-agent workflows using Gemini and MCP.
Following the 4-Layer Hierarchy: L4 = Synthesis (Depends on L1, L2, L3)
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

from tools.L1_config.logging_config import get_logger
from tools.L2_foundation.agent_helpers import AgentRole, AgentTask, AgentMessage, get_agent_helper
from tools.L3_analysis.agent_logic import get_agent_logic, AgentDecision

logger = get_logger(__name__)


@dataclass
class WorkflowState:
    """Represents the state of a multi-agent workflow."""
    workflow_id: str
    description: str
    tasks: List[AgentTask]
    messages: List[AgentMessage] = field(default_factory=list)
    decisions: List[AgentDecision] = field(default_factory=list)
    status: str = "pending"  # pending, in_progress, complete, failed
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class AgentCoordinator:
    """
    Coordinates multi-agent workflows.
    
    Manages:
    - Task distribution across agents
    - Inter-agent communication
    - Workflow state tracking
    - Decision logging
    
    Example:
        >>> coordinator = AgentCoordinator()
        >>> workflow = coordinator.create_workflow(
        ...     "Build user authentication system"
        ... )
        >>> coordinator.execute_workflow(workflow)
    """
    
    def __init__(self):
        """Initialize the agent coordinator."""
        self.workflows: Dict[str, WorkflowState] = {}
        self.agent_logics: Dict[AgentRole, Any] = {}
        
        # Initialize agent logic for each role
        for role in AgentRole:
            self.agent_logics[role] = get_agent_logic(role)
        
        logger.info("agent_coordinator_initialized")
    
    def create_workflow(
        self,
        description: str,
        context: Optional[str] = None
    ) -> WorkflowState:
        """
        Create a new multi-agent workflow.
        
        Args:
            description: Description of the workflow goal
            context: Additional context
            
        Returns:
            WorkflowState object
        """
        workflow_id = f"workflow-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        logger.info(
            "workflow_creating",
            workflow_id=workflow_id,
            description=description
        )
        
        # Use orchestrator to decompose into tasks
        orchestrator = get_agent_helper(AgentRole.ORCHESTRATOR)
        tasks = orchestrator.decompose_task(description, context)
        
        workflow = WorkflowState(
            workflow_id=workflow_id,
            description=description,
            tasks=tasks,
            status="pending"
        )
        
        self.workflows[workflow_id] = workflow
        
        logger.info(
            "workflow_created",
            workflow_id=workflow_id,
            task_count=len(tasks)
        )
        
        return workflow
    
    def execute_workflow(
        self,
        workflow: WorkflowState,
        dry_run: bool = False
    ) -> WorkflowState:
        """
        Execute a multi-agent workflow.
        
        Args:
            workflow: The workflow to execute
            dry_run: If True, only plan without executing
            
        Returns:
            Updated WorkflowState
        """
        logger.info(
            "workflow_executing",
            workflow_id=workflow.workflow_id,
            dry_run=dry_run
        )
        
        workflow.status = "in_progress"
        workflow.started_at = datetime.now()
        
        # Get agent logic for orchestrator
        orchestrator_logic = self.agent_logics[AgentRole.ORCHESTRATOR]
        
        # Prioritize tasks
        prioritized_tasks = orchestrator_logic.prioritize_tasks(
            workflow.tasks,
            criteria="dependencies and logical order"
        )
        
        workflow.tasks = prioritized_tasks
        
        if dry_run:
            logger.info(
                "workflow_dry_run_complete",
                workflow_id=workflow.workflow_id,
                task_order=[t.id for t in prioritized_tasks]
            )
            workflow.status = "planned"
            return workflow
        
        # Execute tasks in order
        for task in prioritized_tasks:
            self._execute_task(workflow, task)
        
        workflow.status = "complete"
        workflow.completed_at = datetime.now()
        
        logger.info(
            "workflow_completed",
            workflow_id=workflow.workflow_id,
            duration=(workflow.completed_at - workflow.started_at).total_seconds()
        )
        
        return workflow
    
    def _execute_task(
        self,
        workflow: WorkflowState,
        task: AgentTask
    ):
        """Execute a single task."""
        logger.info(
            "task_executing",
            workflow_id=workflow.workflow_id,
            task_id=task.id,
            agent=task.assigned_to.value
        )
        
        task.status = "in_progress"
        
        try:
            # Get agent logic for this task
            agent_logic = self.agent_logics[task.assigned_to]
            
            # Decide if we need tools
            tool_decision = agent_logic.decide_tool_for_task(
                task.description,
                context={"workflow": workflow.description}
            )
            
            if tool_decision:
                workflow.decisions.append(tool_decision)
                logger.info(
                    "task_tool_selected",
                    task_id=task.id,
                    tool=tool_decision.chosen_option
                )
            
            # For now, mark as complete
            # In a real implementation, this would execute the actual work
            task.status = "complete"
            task.result = {
                "status": "simulated",
                "message": f"Task {task.id} would be executed by {task.assigned_to.value}"
            }
            
            logger.info(
                "task_completed",
                workflow_id=workflow.workflow_id,
                task_id=task.id
            )
            
        except Exception as e:
            logger.error(
                "task_failed",
                workflow_id=workflow.workflow_id,
                task_id=task.id,
                error=str(e)
            )
            
            # Handle error using agent logic
            agent_logic = self.agent_logics[task.assigned_to]
            error_decision = agent_logic.handle_error(
                e,
                context={"task": task.description, "workflow": workflow.description}
            )
            
            workflow.decisions.append(error_decision)
            
            task.status = "failed"
            task.error = str(e)
    
    def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the status of a workflow.
        
        Args:
            workflow_id: The workflow ID
            
        Returns:
            Dictionary with workflow status
        """
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            return None
        
        return {
            "workflow_id": workflow.workflow_id,
            "description": workflow.description,
            "status": workflow.status,
            "total_tasks": len(workflow.tasks),
            "completed_tasks": len([t for t in workflow.tasks if t.status == "complete"]),
            "failed_tasks": len([t for t in workflow.tasks if t.status == "failed"]),
            "decisions_made": len(workflow.decisions),
            "started_at": workflow.started_at.isoformat() if workflow.started_at else None,
            "completed_at": workflow.completed_at.isoformat() if workflow.completed_at else None,
        }
    
    def list_workflows(self) -> List[Dict[str, Any]]:
        """
        List all workflows.
        
        Returns:
            List of workflow status dictionaries
        """
        return [
            self.get_workflow_status(wf_id)
            for wf_id in self.workflows.keys()
        ]


# Singleton instance
_coordinator: Optional[AgentCoordinator] = None


def get_coordinator() -> AgentCoordinator:
    """
    Get the singleton agent coordinator instance.
    
    Returns:
        AgentCoordinator instance
    """
    global _coordinator
    
    if _coordinator is None:
        _coordinator = AgentCoordinator()
    
    return _coordinator


if __name__ == "__main__":
    # Test the agent coordinator
    print("🔍 Testing Agent Coordinator...")
    print()
    
    coordinator = get_coordinator()
    print("✅ Agent Coordinator initialized")
    print()
    
    # Create a workflow
    print("📋 Creating workflow...")
    workflow = coordinator.create_workflow(
        "Build user authentication system",
        context="Using Supabase for database, Gemini for AI features"
    )
    
    print(f"Workflow ID: {workflow.workflow_id}")
    print(f"Tasks created: {len(workflow.tasks)}")
    for task in workflow.tasks:
        print(f"  • [{task.id}] {task.assigned_to.value}: {task.description}")
    print()
    
    # Execute workflow (dry run)
    print("🚀 Executing workflow (dry run)...")
    result = coordinator.execute_workflow(workflow, dry_run=True)
    
    print(f"Status: {result.status}")
    print(f"Task order:")
    for i, task in enumerate(result.tasks, 1):
        print(f"  {i}. [{task.id}] {task.description}")
    print()
    
    # Get workflow status
    status = coordinator.get_workflow_status(workflow.workflow_id)
    print("📊 Workflow Status:")
    for key, value in status.items():
        print(f"  {key}: {value}")
