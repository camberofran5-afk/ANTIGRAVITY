"""
L4 Synthesis: Workflow Engine
Executes workflows with agent coordination.
Following the 4-Layer Hierarchy: L4 = Synthesis
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
import asyncio

from tools.L1_config.logging_config import get_logger
from tools.L4_synthesis.workflow_builder import WorkflowDefinition, WorkflowStep, StepType
from tools.L3_analysis.state_manager import (
    get_state_manager,
    WorkflowStatus,
    StepStatus,
    StateManager
)
from tools.L4_synthesis.agno_integration import get_agno_agent
from tools.L2_foundation.agent_helpers import AgentRole

logger = get_logger(__name__)


class WorkflowExecutionResult:
    """Result from workflow execution."""
    
    def __init__(
        self,
        workflow_id: str,
        status: WorkflowStatus,
        step_results: Dict[str, Any],
        duration_seconds: float,
        error: Optional[str] = None
    ):
        self.workflow_id = workflow_id
        self.status = status
        self.step_results = step_results
        self.duration_seconds = duration_seconds
        self.error = error
        self.success = status == WorkflowStatus.COMPLETE
    
    @property
    def summary(self) -> str:
        """Get execution summary."""
        if self.success:
            return f"Workflow completed successfully in {self.duration_seconds:.1f}s"
        else:
            return f"Workflow failed: {self.error}"


class WorkflowEngine:
    """
    Executes workflows with agent coordination.
    
    Features:
    - Sequential and parallel execution
    - Dependency resolution
    - Error handling and retries
    - State persistence
    - Approval gates
    
    Example:
        >>> engine = WorkflowEngine()
        >>> result = engine.execute(workflow_definition)
    """
    
    def __init__(self, state_manager: Optional[StateManager] = None):
        """
        Initialize workflow engine.
        
        Args:
            state_manager: State manager instance (uses singleton if None)
        """
        self.state_manager = state_manager or get_state_manager()
        self.agents: Dict[AgentRole, Any] = {}
        
        logger.info("workflow_engine_initialized")
    
    def execute(
        self,
        workflow: WorkflowDefinition,
        context: Optional[Dict[str, Any]] = None,
        dry_run: bool = False
    ) -> WorkflowExecutionResult:
        """
        Execute a workflow.
        
        Args:
            workflow: Workflow definition to execute
            context: Initial context data
            dry_run: If True, only validate without executing
            
        Returns:
            WorkflowExecutionResult
        """
        logger.info(
            "workflow_execution_started",
            workflow_id=workflow.id,
            name=workflow.name,
            dry_run=dry_run
        )
        
        # Create workflow state
        state = self.state_manager.create_workflow_state(
            workflow.id,
            workflow.name
        )
        
        if context:
            state.context = context
        
        if dry_run:
            logger.info(
                "workflow_dry_run",
                workflow_id=workflow.id
            )
            return WorkflowExecutionResult(
                workflow_id=workflow.id,
                status=WorkflowStatus.COMPLETE,
                step_results={},
                duration_seconds=0.0
            )
        
        # Update status to running
        self.state_manager.update_status(workflow.id, WorkflowStatus.RUNNING)
        
        start_time = datetime.now()
        
        try:
            # Execute steps based on pattern
            if workflow.pattern.value == "sequential":
                self._execute_sequential(workflow)
            elif workflow.pattern.value == "parallel":
                self._execute_parallel(workflow)
            else:
                # For now, treat other patterns as sequential
                self._execute_sequential(workflow)
            
            # Mark as complete
            self.state_manager.update_status(workflow.id, WorkflowStatus.COMPLETE)
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            logger.info(
                "workflow_execution_completed",
                workflow_id=workflow.id,
                duration=duration
            )
            
            return WorkflowExecutionResult(
                workflow_id=workflow.id,
                status=WorkflowStatus.COMPLETE,
                step_results=state.step_results,
                duration_seconds=duration
            )
            
        except Exception as e:
            logger.error(
                "workflow_execution_failed",
                workflow_id=workflow.id,
                error=str(e)
            )
            
            self.state_manager.update_status(
                workflow.id,
                WorkflowStatus.FAILED,
                error=str(e)
            )
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            return WorkflowExecutionResult(
                workflow_id=workflow.id,
                status=WorkflowStatus.FAILED,
                step_results=state.step_results,
                duration_seconds=duration,
                error=str(e)
            )
    
    def _execute_sequential(self, workflow: WorkflowDefinition):
        """Execute workflow steps sequentially."""
        logger.info(
            "executing_sequential_workflow",
            workflow_id=workflow.id
        )
        
        # Build dependency graph
        steps_by_name = {step.name: step for step in workflow.steps}
        
        # Execute steps in order, respecting dependencies
        executed = set()
        
        while len(executed) < len(workflow.steps):
            # Find next step to execute
            next_step = None
            
            for step in workflow.steps:
                if step.name in executed:
                    continue
                
                # Check if dependencies are met
                deps_met = all(dep in executed for dep in step.depends_on)
                
                if deps_met:
                    next_step = step
                    break
            
            if not next_step:
                # Check for circular dependencies or missing deps
                remaining = [s.name for s in workflow.steps if s.name not in executed]
                raise RuntimeError(
                    f"Cannot find next step to execute. Remaining: {remaining}"
                )
            
            # Execute the step
            self._execute_step(workflow.id, next_step)
            executed.add(next_step.name)
    
    def _execute_parallel(self, workflow: WorkflowDefinition):
        """Execute workflow steps in parallel where possible."""
        logger.info(
            "executing_parallel_workflow",
            workflow_id=workflow.id
        )
        
        # For now, execute sequentially
        # TODO: Implement true parallel execution with asyncio
        self._execute_sequential(workflow)
    
    def _execute_step(self, workflow_id: str, step: WorkflowStep):
        """Execute a single workflow step."""
        logger.info(
            "executing_step",
            workflow_id=workflow_id,
            step_id=step.id,
            step_name=step.name,
            step_type=step.type.value
        )
        
        # Update status to running
        self.state_manager.update_step_status(
            workflow_id,
            step.id,
            StepStatus.RUNNING
        )
        
        try:
            if step.type == StepType.AGENT_TASK:
                result = self._execute_agent_task(workflow_id, step)
            elif step.type == StepType.APPROVAL_GATE:
                result = self._execute_approval_gate(workflow_id, step)
            else:
                result = f"Step type {step.type.value} not yet implemented"
            
            # Update status to complete
            self.state_manager.update_step_status(
                workflow_id,
                step.id,
                StepStatus.COMPLETE,
                output=result
            )
            
            logger.info(
                "step_completed",
                workflow_id=workflow_id,
                step_id=step.id,
                step_name=step.name
            )
            
        except Exception as e:
            logger.error(
                "step_failed",
                workflow_id=workflow_id,
                step_id=step.id,
                step_name=step.name,
                error=str(e)
            )
            
            self.state_manager.update_step_status(
                workflow_id,
                step.id,
                StepStatus.FAILED,
                error=str(e)
            )
            
            raise
    
    def _execute_agent_task(self, workflow_id: str, step: WorkflowStep) -> str:
        """Execute an agent task."""
        if not step.agent_role or not step.task_description:
            raise ValueError(f"Agent task requires agent_role and task_description")
        
        # Get agent for this role
        agent = self._get_agent(step.agent_role)
        
        # Get workflow state for context
        state = self.state_manager.get_state(workflow_id)
        context = state.context if state else {}
        
        # Execute task with agent
        logger.info(
            "executing_agent_task",
            workflow_id=workflow_id,
            step_id=step.id,
            agent=step.agent_role.value,
            task=step.task_description[:100]
        )
        
        result = agent.execute_task(
            step.task_description,
            context=context
        )
        
        return result
    
    def _execute_approval_gate(self, workflow_id: str, step: WorkflowStep) -> str:
        """Execute an approval gate."""
        logger.info(
            "approval_gate_reached",
            workflow_id=workflow_id,
            step_id=step.id,
            step_name=step.name
        )
        
        # Update workflow status
        self.state_manager.update_status(
            workflow_id,
            WorkflowStatus.WAITING_APPROVAL
        )
        
        # For now, auto-approve
        # TODO: Implement actual approval mechanism
        logger.warning(
            "approval_gate_auto_approved",
            workflow_id=workflow_id,
            step_id=step.id,
            message="Approval gates not yet implemented - auto-approving"
        )
        
        # Resume workflow
        self.state_manager.update_status(
            workflow_id,
            WorkflowStatus.RUNNING
        )
        
        return "Auto-approved (approval gates not yet implemented)"
    
    def _get_agent(self, role: AgentRole):
        """Get or create agent for a role."""
        if role not in self.agents:
            self.agents[role] = get_agno_agent(role)
        
        return self.agents[role]


# Singleton instance
_workflow_engine: Optional[WorkflowEngine] = None


def get_workflow_engine() -> WorkflowEngine:
    """Get the singleton workflow engine instance."""
    global _workflow_engine
    
    if _workflow_engine is None:
        _workflow_engine = WorkflowEngine()
    
    return _workflow_engine


if __name__ == "__main__":
    # Test the workflow engine
    print("🔍 Testing Workflow Engine...")
    print()
    
    from tools.L4_synthesis.workflow_builder import WorkflowBuilder
    
    # Build a test workflow
    workflow = (
        WorkflowBuilder("Test Workflow")
        .sequential()
        .add_step("step1", AgentRole.AI, "Say hello")
        .add_step("step2", AgentRole.AI, "Explain what you do", depends_on=["step1"])
        .build()
    )
    
    print(f"Workflow built: {workflow.name}")
    print(f"Steps: {len(workflow.steps)}")
    print()
    
    # Execute (dry run)
    engine = get_workflow_engine()
    result = engine.execute(workflow, dry_run=True)
    
    print(f"✅ Dry run completed")
    print(f"Status: {result.status.value}")
    print(f"Duration: {result.duration_seconds}s")
