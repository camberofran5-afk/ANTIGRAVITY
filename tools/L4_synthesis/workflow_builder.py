"""
L4 Synthesis: Workflow Builder
Declarative workflow definition with fluent API.
Following the 4-Layer Hierarchy: L4 = Synthesis
"""

from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

from tools.L1_config.logging_config import get_logger
from tools.L2_foundation.agent_helpers import AgentRole

logger = get_logger(__name__)


class WorkflowPattern(str, Enum):
    """Workflow execution patterns."""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    DEBATE = "debate"
    ADAPTIVE = "adaptive"


class StepType(str, Enum):
    """Types of workflow steps."""
    AGENT_TASK = "agent_task"
    APPROVAL_GATE = "approval_gate"
    PARALLEL_GROUP = "parallel_group"
    CONDITIONAL = "conditional"


@dataclass
class WorkflowStep:
    """Represents a single step in a workflow."""
    id: str
    type: StepType
    name: str
    agent_role: Optional[AgentRole] = None
    task_description: Optional[str] = None
    depends_on: List[str] = field(default_factory=list)
    timeout_seconds: int = 300
    retry_count: int = 3
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ApprovalGate:
    """Represents a human approval gate."""
    id: str
    name: str
    description: str
    timeout_hours: int = 24
    required_approvers: List[str] = field(default_factory=list)
    auto_approve_after_timeout: bool = False


@dataclass
class WorkflowDefinition:
    """Complete workflow definition."""
    id: str
    name: str
    description: str
    pattern: WorkflowPattern
    steps: List[WorkflowStep]
    approval_gates: List[ApprovalGate]
    created_at: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)


class WorkflowBuilder:
    """
    Fluent API for building workflows.
    
    Example:
        >>> workflow = (
        ...     WorkflowBuilder("My Workflow")
        ...     .sequential()
        ...     .add_step("step1", AgentRole.DATABASE, "Design schema")
        ...     .add_step("step2", AgentRole.API, "Create API")
        ...     .build()
        ... )
    """
    
    def __init__(self, name: str, description: str = ""):
        """
        Initialize workflow builder.
        
        Args:
            name: Workflow name
            description: Workflow description
        """
        self.workflow_id = f"wf-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        self.name = name
        self.description = description
        self.pattern = WorkflowPattern.SEQUENTIAL
        self.steps: List[WorkflowStep] = []
        self.approval_gates: List[ApprovalGate] = []
        self._step_counter = 0
        
        logger.info(
            "workflow_builder_initialized",
            workflow_id=self.workflow_id,
            name=name
        )
    
    def sequential(self) -> 'WorkflowBuilder':
        """Set workflow pattern to sequential."""
        self.pattern = WorkflowPattern.SEQUENTIAL
        return self
    
    def parallel(self) -> 'WorkflowBuilder':
        """Set workflow pattern to parallel."""
        self.pattern = WorkflowPattern.PARALLEL
        return self
    
    def debate(self) -> 'WorkflowBuilder':
        """Set workflow pattern to debate-consensus."""
        self.pattern = WorkflowPattern.DEBATE
        return self
    
    def adaptive(self) -> 'WorkflowBuilder':
        """Set workflow pattern to adaptive."""
        self.pattern = WorkflowPattern.ADAPTIVE
        return self
    
    def add_step(
        self,
        name: str,
        agent_role: AgentRole,
        task_description: str,
        depends_on: Optional[List[str]] = None,
        timeout_seconds: int = 300,
        retry_count: int = 3,
        **metadata
    ) -> 'WorkflowBuilder':
        """
        Add a step to the workflow.
        
        Args:
            name: Step name
            agent_role: Agent role to execute this step
            task_description: Task description for the agent
            depends_on: List of step names this depends on
            timeout_seconds: Timeout for this step
            retry_count: Number of retries on failure
            **metadata: Additional metadata
            
        Returns:
            Self for chaining
        """
        step_id = f"step-{self._step_counter}"
        self._step_counter += 1
        
        step = WorkflowStep(
            id=step_id,
            type=StepType.AGENT_TASK,
            name=name,
            agent_role=agent_role,
            task_description=task_description,
            depends_on=depends_on or [],
            timeout_seconds=timeout_seconds,
            retry_count=retry_count,
            metadata=metadata
        )
        
        self.steps.append(step)
        
        logger.debug(
            "workflow_step_added",
            workflow_id=self.workflow_id,
            step_id=step_id,
            name=name,
            agent=agent_role.value
        )
        
        return self
    
    def add_parallel_steps(
        self,
        steps: List[tuple],
        depends_on: Optional[List[str]] = None
    ) -> 'WorkflowBuilder':
        """
        Add multiple steps to execute in parallel.
        
        Args:
            steps: List of (name, agent_role, task_description) tuples
            depends_on: List of step names all parallel steps depend on
            
        Returns:
            Self for chaining
        """
        parallel_group_id = f"parallel-{self._step_counter}"
        self._step_counter += 1
        
        for name, agent_role, task_description in steps:
            step_id = f"step-{self._step_counter}"
            self._step_counter += 1
            
            step = WorkflowStep(
                id=step_id,
                type=StepType.AGENT_TASK,
                name=name,
                agent_role=agent_role,
                task_description=task_description,
                depends_on=depends_on or [],
                metadata={"parallel_group": parallel_group_id}
            )
            
            self.steps.append(step)
        
        logger.debug(
            "workflow_parallel_steps_added",
            workflow_id=self.workflow_id,
            parallel_group=parallel_group_id,
            step_count=len(steps)
        )
        
        return self
    
    def add_approval_gate(
        self,
        name: str,
        description: str,
        timeout_hours: int = 24,
        required_approvers: Optional[List[str]] = None,
        auto_approve_after_timeout: bool = False
    ) -> 'WorkflowBuilder':
        """
        Add a human approval gate.
        
        Args:
            name: Gate name
            description: Description of what needs approval
            timeout_hours: Hours to wait for approval
            required_approvers: List of required approver IDs
            auto_approve_after_timeout: Auto-approve if timeout reached
            
        Returns:
            Self for chaining
        """
        gate_id = f"gate-{len(self.approval_gates)}"
        
        gate = ApprovalGate(
            id=gate_id,
            name=name,
            description=description,
            timeout_hours=timeout_hours,
            required_approvers=required_approvers or [],
            auto_approve_after_timeout=auto_approve_after_timeout
        )
        
        self.approval_gates.append(gate)
        
        # Add gate as a step
        step = WorkflowStep(
            id=gate_id,
            type=StepType.APPROVAL_GATE,
            name=name,
            task_description=description,
            metadata={"gate": gate}
        )
        
        self.steps.append(step)
        
        logger.debug(
            "workflow_approval_gate_added",
            workflow_id=self.workflow_id,
            gate_id=gate_id,
            name=name
        )
        
        return self
    
    def build(self) -> WorkflowDefinition:
        """
        Build the workflow definition.
        
        Returns:
            WorkflowDefinition ready for execution
        """
        # Validate workflow
        self._validate()
        
        definition = WorkflowDefinition(
            id=self.workflow_id,
            name=self.name,
            description=self.description,
            pattern=self.pattern,
            steps=self.steps,
            approval_gates=self.approval_gates,
            created_at=datetime.now()
        )
        
        logger.info(
            "workflow_built",
            workflow_id=self.workflow_id,
            name=self.name,
            pattern=self.pattern.value,
            step_count=len(self.steps),
            gate_count=len(self.approval_gates)
        )
        
        return definition
    
    def _validate(self):
        """Validate workflow definition."""
        # Check for circular dependencies
        visited = set()
        
        def has_cycle(step_name: str, path: set) -> bool:
            if step_name in path:
                return True
            if step_name in visited:
                return False
            
            visited.add(step_name)
            path.add(step_name)
            
            # Find step
            step = next((s for s in self.steps if s.name == step_name), None)
            if step:
                for dep in step.depends_on:
                    if has_cycle(dep, path.copy()):
                        return True
            
            return False
        
        for step in self.steps:
            if has_cycle(step.name, set()):
                raise ValueError(f"Circular dependency detected involving step: {step.name}")
        
        # Validate dependencies exist
        step_names = {s.name for s in self.steps}
        for step in self.steps:
            for dep in step.depends_on:
                if dep not in step_names:
                    raise ValueError(f"Step '{step.name}' depends on non-existent step '{dep}'")
        
        logger.debug(
            "workflow_validated",
            workflow_id=self.workflow_id
        )


if __name__ == "__main__":
    # Test the workflow builder
    print("🔍 Testing Workflow Builder...")
    print()
    
    # Build a simple workflow
    workflow = (
        WorkflowBuilder("Test Workflow", "A test workflow")
        .sequential()
        .add_step("design", AgentRole.DATABASE, "Design database schema")
        .add_step("implement", AgentRole.API, "Implement API", depends_on=["design"])
        .add_step("test", AgentRole.QA, "Write tests", depends_on=["implement"])
        .add_approval_gate("review", "Review before deployment")
        .add_step("deploy", AgentRole.API, "Deploy to production")
        .build()
    )
    
    print(f"✅ Workflow built: {workflow.name}")
    print(f"Pattern: {workflow.pattern.value}")
    print(f"Steps: {len(workflow.steps)}")
    print(f"Approval gates: {len(workflow.approval_gates)}")
    print()
    
    print("Steps:")
    for step in workflow.steps:
        deps = f" (depends on: {', '.join(step.depends_on)})" if step.depends_on else ""
        print(f"  • {step.name}: {step.type.value}{deps}")
