"""
L3 Analysis: State Manager
Manages workflow execution state with persistence.
Following the 4-Layer Hierarchy: L3 = Analysis
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
import json

from tools.L1_config.logging_config import get_logger

logger = get_logger(__name__)


class WorkflowStatus(str, Enum):
    """Workflow execution status."""
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    WAITING_APPROVAL = "waiting_approval"
    COMPLETE = "complete"
    FAILED = "failed"
    CANCELLED = "cancelled"


class StepStatus(str, Enum):
    """Step execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETE = "complete"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class StepResult:
    """Result from a step execution."""
    step_id: str
    status: StepStatus
    output: Any = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_seconds: float = 0.0
    retry_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Checkpoint:
    """Workflow checkpoint for recovery."""
    checkpoint_id: str
    workflow_id: str
    timestamp: datetime
    completed_steps: List[str]
    current_step: Optional[str]
    context: Dict[str, Any]


@dataclass
class WorkflowState:
    """Complete workflow execution state."""
    workflow_id: str
    workflow_name: str
    status: WorkflowStatus
    current_step: Optional[str] = None
    completed_steps: List[str] = field(default_factory=list)
    failed_steps: List[str] = field(default_factory=list)
    step_results: Dict[str, StepResult] = field(default_factory=dict)
    context: Dict[str, Any] = field(default_factory=dict)
    checkpoints: List[Checkpoint] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None


class StateManager:
    """
    Manages workflow execution state with persistence.
    
    Features:
    - In-memory state storage
    - Checkpointing for recovery
    - State inspection
    - Time-travel debugging
    
    Example:
        >>> manager = StateManager()
        >>> state = manager.create_workflow_state("wf-1", "My Workflow")
        >>> manager.update_step_status("wf-1", "step-1", StepStatus.COMPLETE)
    """
    
    def __init__(self, persist_to_file: bool = False, storage_path: str = "temp/workflows"):
        """
        Initialize state manager.
        
        Args:
            persist_to_file: Whether to persist state to files
            storage_path: Path for file storage
        """
        self.states: Dict[str, WorkflowState] = {}
        self.persist_to_file = persist_to_file
        self.storage_path = storage_path
        
        if persist_to_file:
            import os
            os.makedirs(storage_path, exist_ok=True)
        
        logger.info(
            "state_manager_initialized",
            persist_to_file=persist_to_file,
            storage_path=storage_path
        )
    
    def create_workflow_state(
        self,
        workflow_id: str,
        workflow_name: str
    ) -> WorkflowState:
        """
        Create a new workflow state.
        
        Args:
            workflow_id: Workflow ID
            workflow_name: Workflow name
            
        Returns:
            New WorkflowState
        """
        state = WorkflowState(
            workflow_id=workflow_id,
            workflow_name=workflow_name,
            status=WorkflowStatus.PENDING
        )
        
        self.states[workflow_id] = state
        self._persist_state(state)
        
        logger.info(
            "workflow_state_created",
            workflow_id=workflow_id,
            name=workflow_name
        )
        
        return state
    
    def get_state(self, workflow_id: str) -> Optional[WorkflowState]:
        """Get workflow state by ID."""
        return self.states.get(workflow_id)
    
    def update_status(
        self,
        workflow_id: str,
        status: WorkflowStatus,
        error: Optional[str] = None
    ):
        """Update workflow status."""
        state = self.states.get(workflow_id)
        if not state:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        state.status = status
        state.updated_at = datetime.now()
        
        if status == WorkflowStatus.RUNNING and not state.started_at:
            state.started_at = datetime.now()
        elif status in [WorkflowStatus.COMPLETE, WorkflowStatus.FAILED, WorkflowStatus.CANCELLED]:
            state.completed_at = datetime.now()
        
        if error:
            state.error = error
        
        self._persist_state(state)
        
        logger.info(
            "workflow_status_updated",
            workflow_id=workflow_id,
            status=status.value,
            error=error
        )
    
    def update_step_status(
        self,
        workflow_id: str,
        step_id: str,
        status: StepStatus,
        output: Any = None,
        error: Optional[str] = None
    ):
        """Update step status."""
        state = self.states.get(workflow_id)
        if not state:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        # Get or create step result
        if step_id not in state.step_results:
            state.step_results[step_id] = StepResult(
                step_id=step_id,
                status=status,
                started_at=datetime.now()
            )
        
        result = state.step_results[step_id]
        result.status = status
        result.output = output
        result.error = error
        
        if status == StepStatus.RUNNING and not result.started_at:
            result.started_at = datetime.now()
        elif status in [StepStatus.COMPLETE, StepStatus.FAILED]:
            result.completed_at = datetime.now()
            if result.started_at:
                result.duration_seconds = (
                    result.completed_at - result.started_at
                ).total_seconds()
        
        # Update workflow state
        if status == StepStatus.RUNNING:
            state.current_step = step_id
        elif status == StepStatus.COMPLETE:
            if step_id not in state.completed_steps:
                state.completed_steps.append(step_id)
            if state.current_step == step_id:
                state.current_step = None
        elif status == StepStatus.FAILED:
            if step_id not in state.failed_steps:
                state.failed_steps.append(step_id)
        
        state.updated_at = datetime.now()
        self._persist_state(state)
        
        logger.info(
            "step_status_updated",
            workflow_id=workflow_id,
            step_id=step_id,
            status=status.value
        )
    
    def create_checkpoint(
        self,
        workflow_id: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Checkpoint:
        """Create a checkpoint for recovery."""
        state = self.states.get(workflow_id)
        if not state:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        checkpoint_id = f"cp-{len(state.checkpoints)}"
        
        checkpoint = Checkpoint(
            checkpoint_id=checkpoint_id,
            workflow_id=workflow_id,
            timestamp=datetime.now(),
            completed_steps=state.completed_steps.copy(),
            current_step=state.current_step,
            context=context or state.context.copy()
        )
        
        state.checkpoints.append(checkpoint)
        self._persist_state(state)
        
        logger.info(
            "checkpoint_created",
            workflow_id=workflow_id,
            checkpoint_id=checkpoint_id
        )
        
        return checkpoint
    
    def restore_checkpoint(
        self,
        workflow_id: str,
        checkpoint_id: str
    ):
        """Restore workflow to a checkpoint."""
        state = self.states.get(workflow_id)
        if not state:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        checkpoint = next(
            (cp for cp in state.checkpoints if cp.checkpoint_id == checkpoint_id),
            None
        )
        
        if not checkpoint:
            raise ValueError(f"Checkpoint {checkpoint_id} not found")
        
        state.completed_steps = checkpoint.completed_steps.copy()
        state.current_step = checkpoint.current_step
        state.context = checkpoint.context.copy()
        state.status = WorkflowStatus.RUNNING
        state.updated_at = datetime.now()
        
        self._persist_state(state)
        
        logger.info(
            "checkpoint_restored",
            workflow_id=workflow_id,
            checkpoint_id=checkpoint_id
        )
    
    def get_execution_summary(self, workflow_id: str) -> Dict[str, Any]:
        """Get execution summary for a workflow."""
        state = self.states.get(workflow_id)
        if not state:
            return {}
        
        total_steps = len(state.step_results)
        completed = len(state.completed_steps)
        failed = len(state.failed_steps)
        
        duration = None
        if state.started_at:
            end_time = state.completed_at or datetime.now()
            duration = (end_time - state.started_at).total_seconds()
        
        return {
            "workflow_id": workflow_id,
            "name": state.workflow_name,
            "status": state.status.value,
            "total_steps": total_steps,
            "completed_steps": completed,
            "failed_steps": failed,
            "progress_percent": (completed / total_steps * 100) if total_steps > 0 else 0,
            "duration_seconds": duration,
            "checkpoints": len(state.checkpoints),
            "created_at": state.created_at.isoformat(),
            "started_at": state.started_at.isoformat() if state.started_at else None,
            "completed_at": state.completed_at.isoformat() if state.completed_at else None,
        }
    
    def _persist_state(self, state: WorkflowState):
        """Persist state to file if enabled."""
        if not self.persist_to_file:
            return
        
        try:
            import os
            filepath = os.path.join(self.storage_path, f"{state.workflow_id}.json")
            
            # Convert state to dict
            state_dict = {
                "workflow_id": state.workflow_id,
                "workflow_name": state.workflow_name,
                "status": state.status.value,
                "current_step": state.current_step,
                "completed_steps": state.completed_steps,
                "failed_steps": state.failed_steps,
                "context": state.context,
                "created_at": state.created_at.isoformat(),
                "updated_at": state.updated_at.isoformat(),
                "started_at": state.started_at.isoformat() if state.started_at else None,
                "completed_at": state.completed_at.isoformat() if state.completed_at else None,
                "error": state.error,
            }
            
            with open(filepath, 'w') as f:
                json.dump(state_dict, f, indent=2)
                
        except Exception as e:
            logger.error(
                "state_persistence_failed",
                workflow_id=state.workflow_id,
                error=str(e)
            )


# Singleton instance
_state_manager: Optional[StateManager] = None


def get_state_manager() -> StateManager:
    """Get the singleton state manager instance."""
    global _state_manager
    
    if _state_manager is None:
        _state_manager = StateManager(persist_to_file=True)
    
    return _state_manager


if __name__ == "__main__":
    # Test the state manager
    print("🔍 Testing State Manager...")
    print()
    
    manager = StateManager(persist_to_file=False)
    
    # Create workflow state
    state = manager.create_workflow_state("wf-test", "Test Workflow")
    print(f"✅ Created workflow state: {state.workflow_id}")
    print()
    
    # Update status
    manager.update_status("wf-test", WorkflowStatus.RUNNING)
    print(f"Status: {state.status.value}")
    
    # Update steps
    manager.update_step_status("wf-test", "step-1", StepStatus.RUNNING)
    manager.update_step_status("wf-test", "step-1", StepStatus.COMPLETE, output="Schema designed")
    manager.update_step_status("wf-test", "step-2", StepStatus.RUNNING)
    manager.update_step_status("wf-test", "step-2", StepStatus.COMPLETE, output="API created")
    
    # Create checkpoint
    checkpoint = manager.create_checkpoint("wf-test")
    print(f"Checkpoint created: {checkpoint.checkpoint_id}")
    print()
    
    # Get summary
    summary = manager.get_execution_summary("wf-test")
    print("Execution Summary:")
    for key, value in summary.items():
        print(f"  {key}: {value}")
