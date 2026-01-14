# Production Orchestration Guide

## 🎯 Workflows vs Apps: Key Distinctions

### **Agentic Workflows**
**Definition**: Coordinated sequences of autonomous agent tasks with defined inputs/outputs and decision points.

**Characteristics**:
- **Stateful**: Maintains execution state across steps
- **Resumable**: Can pause/resume at checkpoints
- **Branching**: Conditional logic based on agent outputs
- **Multi-agent**: Coordinates multiple specialized agents
- **Time-bound**: Typically completes in minutes to hours

**Examples**:
- Research → Analysis → Report Generation
- Code Review → Fix → Test → Deploy
- Data Collection → Processing → Validation → Storage

### **Agentic Apps**
**Definition**: Full-stack applications where agents are embedded as core functionality, running continuously.

**Characteristics**:
- **Persistent**: Always-on services with databases
- **Interactive**: User-facing interfaces (web/API)
- **Event-driven**: Responds to triggers (webhooks, schedules, user actions)
- **Scalable**: Handles concurrent requests
- **Long-lived**: Runs indefinitely

**Examples**:
- AI-powered SaaS platforms
- Automated customer support systems
- Continuous monitoring/alerting services
- Multi-tenant agent marketplaces

---

## 🏗️ Production Orchestration Requirements

### 1️⃣ **Workflow Engine** ❌ MISSING

**What's Needed**:
- Declarative workflow definitions (YAML/JSON)
- DAG (Directed Acyclic Graph) execution
- Parallel and sequential step execution
- Conditional branching and loops
- Workflow versioning

**Implementation**:
```python
# /tools/L4_synthesis/workflow_engine.py
from typing import Dict, List, Any, Callable
from enum import Enum
import asyncio
from dataclasses import dataclass, field
import json

class StepType(Enum):
    AGENT_TASK = "agent_task"
    PARALLEL = "parallel"
    CONDITIONAL = "conditional"
    LOOP = "loop"
    HUMAN_REVIEW = "human_review"

@dataclass
class WorkflowStep:
    id: str
    type: StepType
    agent_role: str = None
    task: str = None
    inputs: Dict[str, Any] = field(default_factory=dict)
    outputs: List[str] = field(default_factory=list)
    next_steps: List[str] = field(default_factory=list)
    condition: Callable = None
    retry_policy: Dict = field(default_factory=dict)

@dataclass
class WorkflowDefinition:
    name: str
    version: str
    steps: List[WorkflowStep]
    metadata: Dict[str, Any] = field(default_factory=dict)

class WorkflowEngine:
    """Production-ready workflow orchestration engine"""
    
    def __init__(self, state_manager, observability):
        self.state_manager = state_manager
        self.observability = observability
        self.workflows = {}
    
    def register_workflow(self, definition: WorkflowDefinition):
        """Register a workflow definition"""
        self.workflows[definition.name] = definition
    
    async def execute_workflow(self, workflow_name: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a workflow with state tracking"""
        workflow = self.workflows.get(workflow_name)
        if not workflow:
            raise ValueError(f"Workflow {workflow_name} not found")
        
        execution_id = self.state_manager.create_execution(workflow_name, inputs)
        context = {"inputs": inputs, "outputs": {}}
        
        try:
            for step in workflow.steps:
                await self._execute_step(execution_id, step, context)
            
            self.state_manager.mark_completed(execution_id)
            return context["outputs"]
        
        except Exception as e:
            self.state_manager.mark_failed(execution_id, str(e))
            raise
    
    async def _execute_step(self, execution_id: str, step: WorkflowStep, context: Dict):
        """Execute a single workflow step"""
        self.observability.log_step_start(execution_id, step.id)
        
        try:
            if step.type == StepType.AGENT_TASK:
                result = await self._execute_agent_task(step, context)
            elif step.type == StepType.PARALLEL:
                result = await self._execute_parallel(step, context)
            elif step.type == StepType.CONDITIONAL:
                result = await self._execute_conditional(step, context)
            elif step.type == StepType.HUMAN_REVIEW:
                result = await self._execute_human_review(step, context)
            
            # Store outputs
            for output_key in step.outputs:
                context["outputs"][output_key] = result.get(output_key)
            
            self.state_manager.update_step(execution_id, step.id, "completed", result)
            self.observability.log_step_complete(execution_id, step.id)
        
        except Exception as e:
            self.observability.log_step_error(execution_id, step.id, str(e))
            raise
    
    async def _execute_agent_task(self, step: WorkflowStep, context: Dict) -> Dict:
        """Execute an agent task"""
        from tools.L4_synthesis.agent_coordinator import AgentCoordinator
        
        coordinator = AgentCoordinator()
        result = await coordinator.execute_agent(
            role=step.agent_role,
            task=step.task.format(**context["inputs"], **context["outputs"]),
            context=context
        )
        return result
    
    async def _execute_parallel(self, step: WorkflowStep, context: Dict) -> Dict:
        """Execute parallel steps"""
        tasks = [self._execute_step(None, substep, context) for substep in step.next_steps]
        results = await asyncio.gather(*tasks)
        return {"parallel_results": results}
    
    async def _execute_conditional(self, step: WorkflowStep, context: Dict) -> Dict:
        """Execute conditional branching"""
        if step.condition(context):
            return await self._execute_step(None, step.next_steps[0], context)
        else:
            return await self._execute_step(None, step.next_steps[1], context)
    
    async def _execute_human_review(self, step: WorkflowStep, context: Dict) -> Dict:
        """Pause for human review"""
        # Implement human-in-the-loop mechanism
        approval = await self._request_approval(step, context)
        return {"approved": approval}
    
    def load_workflow_from_yaml(self, yaml_path: str) -> WorkflowDefinition:
        """Load workflow definition from YAML"""
        import yaml
        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f)
        
        steps = [WorkflowStep(**step_data) for step_data in data['steps']]
        return WorkflowDefinition(
            name=data['name'],
            version=data['version'],
            steps=steps,
            metadata=data.get('metadata', {})
        )
```

**Example Workflow Definition** (`/workflows/research_workflow.yaml`):
```yaml
name: research_and_report
version: 1.0
metadata:
  description: Research a topic and generate a comprehensive report
  author: Antigravity Team

steps:
  - id: research
    type: agent_task
    agent_role: researcher
    task: "Research {topic} and gather key insights"
    outputs:
      - research_findings
    next_steps:
      - analysis
  
  - id: analysis
    type: agent_task
    agent_role: analyst
    task: "Analyze the research findings: {research_findings}"
    outputs:
      - analysis_results
    next_steps:
      - report_generation
  
  - id: report_generation
    type: agent_task
    agent_role: writer
    task: "Create a report based on: {analysis_results}"
    outputs:
      - final_report
    retry_policy:
      max_retries: 3
      backoff: exponential
```

---

### 2️⃣ **Pattern Library** ❌ MISSING

**What's Needed**:
- Pre-built orchestration patterns
- Reusable workflow templates
- Common agent coordination patterns
- Best practices library

**Implementation**:
```python
# /tools/L4_synthesis/pattern_library.py
from typing import Dict, Any
from tools.L4_synthesis.workflow_engine import WorkflowDefinition, WorkflowStep, StepType

class OrchestrationPatterns:
    """Library of common orchestration patterns"""
    
    @staticmethod
    def sequential_pipeline(agents: list, task_template: str) -> WorkflowDefinition:
        """Sequential agent pipeline pattern"""
        steps = []
        for i, agent in enumerate(agents):
            step = WorkflowStep(
                id=f"step_{i}",
                type=StepType.AGENT_TASK,
                agent_role=agent,
                task=task_template,
                outputs=[f"output_{i}"],
                next_steps=[f"step_{i+1}"] if i < len(agents)-1 else []
            )
            steps.append(step)
        
        return WorkflowDefinition(
            name="sequential_pipeline",
            version="1.0",
            steps=steps
        )
    
    @staticmethod
    def map_reduce(mapper_agent: str, reducer_agent: str, items: list) -> WorkflowDefinition:
        """Map-Reduce pattern for parallel processing"""
        # Map phase: parallel processing
        map_steps = [
            WorkflowStep(
                id=f"map_{i}",
                type=StepType.AGENT_TASK,
                agent_role=mapper_agent,
                task=f"Process item: {item}",
                outputs=[f"map_result_{i}"]
            )
            for i, item in enumerate(items)
        ]
        
        # Reduce phase: aggregate results
        reduce_step = WorkflowStep(
            id="reduce",
            type=StepType.AGENT_TASK,
            agent_role=reducer_agent,
            task="Aggregate all map results",
            outputs=["final_result"]
        )
        
        return WorkflowDefinition(
            name="map_reduce",
            version="1.0",
            steps=map_steps + [reduce_step]
        )
    
    @staticmethod
    def human_in_loop_approval(agent_role: str, task: str) -> WorkflowDefinition:
        """Pattern with human approval checkpoints"""
        steps = [
            WorkflowStep(
                id="agent_work",
                type=StepType.AGENT_TASK,
                agent_role=agent_role,
                task=task,
                outputs=["draft_output"],
                next_steps=["human_review"]
            ),
            WorkflowStep(
                id="human_review",
                type=StepType.HUMAN_REVIEW,
                task="Review and approve draft",
                outputs=["approved"],
                next_steps=["finalize"]
            ),
            WorkflowStep(
                id="finalize",
                type=StepType.AGENT_TASK,
                agent_role=agent_role,
                task="Finalize based on feedback",
                outputs=["final_output"]
            )
        ]
        
        return WorkflowDefinition(
            name="human_in_loop",
            version="1.0",
            steps=steps
        )
    
    @staticmethod
    def retry_with_fallback(primary_agent: str, fallback_agent: str, task: str) -> WorkflowDefinition:
        """Pattern with automatic fallback on failure"""
        steps = [
            WorkflowStep(
                id="primary",
                type=StepType.AGENT_TASK,
                agent_role=primary_agent,
                task=task,
                outputs=["result"],
                retry_policy={"max_retries": 2, "backoff": "exponential"},
                next_steps=["fallback"]
            ),
            WorkflowStep(
                id="fallback",
                type=StepType.CONDITIONAL,
                condition=lambda ctx: ctx.get("primary_failed"),
                next_steps=["fallback_agent", "success"]
            ),
            WorkflowStep(
                id="fallback_agent",
                type=StepType.AGENT_TASK,
                agent_role=fallback_agent,
                task=task,
                outputs=["result"]
            )
        ]
        
        return WorkflowDefinition(
            name="retry_with_fallback",
            version="1.0",
            steps=steps
        )
```

---

### 3️⃣ **State Management** ❌ MISSING

**What's Needed**:
- Persistent workflow state storage
- Checkpoint/resume capabilities
- State versioning and rollback
- Distributed state synchronization

**Implementation**:
```python
# /tools/L3_analysis/state_manager.py
from typing import Dict, Any, Optional
from datetime import datetime
import json
from enum import Enum

class ExecutionStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class StateManager:
    """Production-grade workflow state management"""
    
    def __init__(self, storage_backend="supabase"):
        self.storage = self._init_storage(storage_backend)
    
    def _init_storage(self, backend: str):
        """Initialize storage backend (Supabase, Redis, PostgreSQL)"""
        if backend == "supabase":
            from tools.execution.supabase_client import get_supabase_client
            return get_supabase_client()
        # Add other backends as needed
    
    def create_execution(self, workflow_name: str, inputs: Dict[str, Any]) -> str:
        """Create a new workflow execution"""
        execution_id = self._generate_execution_id()
        
        execution_data = {
            "execution_id": execution_id,
            "workflow_name": workflow_name,
            "status": ExecutionStatus.PENDING.value,
            "inputs": json.dumps(inputs),
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "current_step": None,
            "context": json.dumps({}),
            "error": None
        }
        
        self.storage.table("workflow_executions").insert(execution_data).execute()
        return execution_id
    
    def update_step(self, execution_id: str, step_id: str, status: str, result: Dict):
        """Update step execution state"""
        step_data = {
            "execution_id": execution_id,
            "step_id": step_id,
            "status": status,
            "result": json.dumps(result),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.storage.table("workflow_steps").insert(step_data).execute()
        
        # Update execution current step
        self.storage.table("workflow_executions").update({
            "current_step": step_id,
            "updated_at": datetime.utcnow().isoformat()
        }).eq("execution_id", execution_id).execute()
    
    def mark_completed(self, execution_id: str):
        """Mark execution as completed"""
        self.storage.table("workflow_executions").update({
            "status": ExecutionStatus.COMPLETED.value,
            "updated_at": datetime.utcnow().isoformat()
        }).eq("execution_id", execution_id).execute()
    
    def mark_failed(self, execution_id: str, error: str):
        """Mark execution as failed"""
        self.storage.table("workflow_executions").update({
            "status": ExecutionStatus.FAILED.value,
            "error": error,
            "updated_at": datetime.utcnow().isoformat()
        }).eq("execution_id", execution_id).execute()
    
    def pause_execution(self, execution_id: str) -> Dict:
        """Pause execution and save checkpoint"""
        execution = self.get_execution(execution_id)
        
        self.storage.table("workflow_executions").update({
            "status": ExecutionStatus.PAUSED.value,
            "updated_at": datetime.utcnow().isoformat()
        }).eq("execution_id", execution_id).execute()
        
        return execution
    
    def resume_execution(self, execution_id: str) -> Dict:
        """Resume paused execution from checkpoint"""
        execution = self.get_execution(execution_id)
        
        if execution["status"] != ExecutionStatus.PAUSED.value:
            raise ValueError(f"Cannot resume execution in status: {execution['status']}")
        
        self.storage.table("workflow_executions").update({
            "status": ExecutionStatus.RUNNING.value,
            "updated_at": datetime.utcnow().isoformat()
        }).eq("execution_id", execution_id).execute()
        
        return execution
    
    def get_execution(self, execution_id: str) -> Dict:
        """Get execution state"""
        result = self.storage.table("workflow_executions").select("*").eq(
            "execution_id", execution_id
        ).execute()
        
        if not result.data:
            raise ValueError(f"Execution {execution_id} not found")
        
        return result.data[0]
    
    def get_execution_history(self, execution_id: str) -> list:
        """Get full execution history"""
        steps = self.storage.table("workflow_steps").select("*").eq(
            "execution_id", execution_id
        ).order("timestamp").execute()
        
        return steps.data
    
    def _generate_execution_id(self) -> str:
        """Generate unique execution ID"""
        import uuid
        return f"exec_{uuid.uuid4().hex[:12]}"
```

**Database Schema** (Supabase):
```sql
-- workflow_executions table
CREATE TABLE workflow_executions (
    execution_id TEXT PRIMARY KEY,
    workflow_name TEXT NOT NULL,
    status TEXT NOT NULL,
    inputs JSONB,
    context JSONB,
    current_step TEXT,
    error TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- workflow_steps table
CREATE TABLE workflow_steps (
    id SERIAL PRIMARY KEY,
    execution_id TEXT REFERENCES workflow_executions(execution_id),
    step_id TEXT NOT NULL,
    status TEXT NOT NULL,
    result JSONB,
    timestamp TIMESTAMP DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_executions_status ON workflow_executions(status);
CREATE INDEX idx_executions_workflow ON workflow_executions(workflow_name);
CREATE INDEX idx_steps_execution ON workflow_steps(execution_id);
```

---

### 4️⃣ **Human-in-the-Loop** ❌ MISSING

**What's Needed**:
- Approval/review mechanisms
- Notification system
- Review UI/API
- Timeout handling

**Implementation**:
```python
# /tools/L4_synthesis/human_in_loop.py
from typing import Dict, Any, Optional, Callable
from datetime import datetime, timedelta
import asyncio

class HumanInLoopManager:
    """Manage human approval and review workflows"""
    
    def __init__(self, state_manager, notification_service):
        self.state_manager = state_manager
        self.notifications = notification_service
        self.pending_reviews = {}
    
    async def request_approval(
        self,
        execution_id: str,
        step_id: str,
        data: Dict[str, Any],
        reviewers: list,
        timeout_minutes: int = 60
    ) -> Dict[str, Any]:
        """Request human approval with timeout"""
        
        review_id = f"review_{execution_id}_{step_id}"
        
        # Create review request
        review_request = {
            "review_id": review_id,
            "execution_id": execution_id,
            "step_id": step_id,
            "data": data,
            "reviewers": reviewers,
            "status": "pending",
            "created_at": datetime.utcnow(),
            "timeout_at": datetime.utcnow() + timedelta(minutes=timeout_minutes)
        }
        
        self.pending_reviews[review_id] = review_request
        
        # Send notifications
        await self._notify_reviewers(review_request)
        
        # Wait for approval or timeout
        try:
            result = await asyncio.wait_for(
                self._wait_for_approval(review_id),
                timeout=timeout_minutes * 60
            )
            return result
        except asyncio.TimeoutError:
            return {"approved": False, "reason": "timeout"}
    
    async def _wait_for_approval(self, review_id: str) -> Dict:
        """Wait for approval decision"""
        while True:
            review = self.pending_reviews.get(review_id)
            if review["status"] != "pending":
                return {
                    "approved": review["status"] == "approved",
                    "feedback": review.get("feedback"),
                    "reviewer": review.get("reviewer")
                }
            await asyncio.sleep(5)  # Poll every 5 seconds
    
    async def _notify_reviewers(self, review_request: Dict):
        """Send notifications to reviewers"""
        for reviewer in review_request["reviewers"]:
            await self.notifications.send(
                to=reviewer,
                subject=f"Review Required: {review_request['step_id']}",
                body=f"Please review execution {review_request['execution_id']}",
                review_url=f"/reviews/{review_request['review_id']}"
            )
    
    def submit_review(self, review_id: str, approved: bool, feedback: str, reviewer: str):
        """Submit review decision"""
        if review_id not in self.pending_reviews:
            raise ValueError(f"Review {review_id} not found")
        
        self.pending_reviews[review_id].update({
            "status": "approved" if approved else "rejected",
            "feedback": feedback,
            "reviewer": reviewer,
            "reviewed_at": datetime.utcnow()
        })
    
    def get_pending_reviews(self, reviewer: str) -> list:
        """Get pending reviews for a reviewer"""
        return [
            review for review in self.pending_reviews.values()
            if reviewer in review["reviewers"] and review["status"] == "pending"
        ]
```

---

### 5️⃣ **Observability** ❌ MISSING

**What's Needed**:
- Comprehensive logging
- Metrics collection
- Monitoring dashboard
- Alerting system
- Distributed tracing

**Implementation**:
```python
# /tools/L3_analysis/observability.py
from typing import Dict, Any
from datetime import datetime
import logging
import json

class ObservabilityService:
    """Comprehensive observability for workflows"""
    
    def __init__(self, metrics_backend="prometheus", logging_backend="cloudwatch"):
        self.logger = self._setup_logging(logging_backend)
        self.metrics = self._setup_metrics(metrics_backend)
        self.traces = {}
    
    def _setup_logging(self, backend: str):
        """Setup structured logging"""
        logger = logging.getLogger("antigravity.workflows")
        logger.setLevel(logging.INFO)
        
        # JSON formatter for structured logs
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
        ))
        logger.addHandler(handler)
        
        return logger
    
    def log_step_start(self, execution_id: str, step_id: str):
        """Log step start"""
        self.logger.info(json.dumps({
            "event": "step_start",
            "execution_id": execution_id,
            "step_id": step_id,
            "timestamp": datetime.utcnow().isoformat()
        }))
        
        self.metrics.increment("workflow.step.started", tags={
            "step_id": step_id
        })
    
    def log_step_complete(self, execution_id: str, step_id: str, duration_ms: float = None):
        """Log step completion"""
        self.logger.info(json.dumps({
            "event": "step_complete",
            "execution_id": execution_id,
            "step_id": step_id,
            "duration_ms": duration_ms,
            "timestamp": datetime.utcnow().isoformat()
        }))
        
        self.metrics.increment("workflow.step.completed", tags={
            "step_id": step_id
        })
        
        if duration_ms:
            self.metrics.histogram("workflow.step.duration", duration_ms, tags={
                "step_id": step_id
            })
    
    def log_step_error(self, execution_id: str, step_id: str, error: str):
        """Log step error"""
        self.logger.error(json.dumps({
            "event": "step_error",
            "execution_id": execution_id,
            "step_id": step_id,
            "error": error,
            "timestamp": datetime.utcnow().isoformat()
        }))
        
        self.metrics.increment("workflow.step.failed", tags={
            "step_id": step_id,
            "error_type": type(error).__name__
        })
    
    def track_token_usage(self, execution_id: str, step_id: str, tokens: int, cost: float):
        """Track LLM token usage and cost"""
        self.logger.info(json.dumps({
            "event": "token_usage",
            "execution_id": execution_id,
            "step_id": step_id,
            "tokens": tokens,
            "cost_usd": cost,
            "timestamp": datetime.utcnow().isoformat()
        }))
        
        self.metrics.histogram("workflow.tokens.used", tokens, tags={
            "step_id": step_id
        })
        self.metrics.histogram("workflow.cost.usd", cost, tags={
            "step_id": step_id
        })
    
    def create_trace(self, execution_id: str, workflow_name: str):
        """Create distributed trace"""
        self.traces[execution_id] = {
            "trace_id": execution_id,
            "workflow_name": workflow_name,
            "started_at": datetime.utcnow(),
            "spans": []
        }
    
    def add_span(self, execution_id: str, step_id: str, duration_ms: float):
        """Add span to trace"""
        if execution_id in self.traces:
            self.traces[execution_id]["spans"].append({
                "step_id": step_id,
                "duration_ms": duration_ms,
                "timestamp": datetime.utcnow().isoformat()
            })
```

---

### 6️⃣ **Error Recovery** ❌ MISSING

**What's Needed**:
- Sophisticated retry logic
- Circuit breakers
- Fallback strategies
- Dead letter queues
- Error classification

**Implementation**:
```python
# /tools/L3_analysis/error_recovery.py
from typing import Callable, Any, Dict
import asyncio
from functools import wraps
from enum import Enum

class ErrorSeverity(Enum):
    TRANSIENT = "transient"  # Retry immediately
    RECOVERABLE = "recoverable"  # Retry with backoff
    FATAL = "fatal"  # Don't retry

class RetryPolicy:
    """Configurable retry policy"""
    
    def __init__(
        self,
        max_retries: int = 3,
        backoff_strategy: str = "exponential",
        initial_delay: float = 1.0,
        max_delay: float = 60.0,
        jitter: bool = True
    ):
        self.max_retries = max_retries
        self.backoff_strategy = backoff_strategy
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.jitter = jitter
    
    def get_delay(self, attempt: int) -> float:
        """Calculate delay for retry attempt"""
        if self.backoff_strategy == "exponential":
            delay = min(self.initial_delay * (2 ** attempt), self.max_delay)
        elif self.backoff_strategy == "linear":
            delay = min(self.initial_delay * attempt, self.max_delay)
        else:
            delay = self.initial_delay
        
        if self.jitter:
            import random
            delay *= (0.5 + random.random())
        
        return delay

class CircuitBreaker:
    """Circuit breaker pattern for fault tolerance"""
    
    def __init__(self, failure_threshold: int = 5, timeout: float = 60.0):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failures = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half-open
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with circuit breaker"""
        if self.state == "open":
            if self._should_attempt_reset():
                self.state = "half-open"
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
    
    def _on_success(self):
        """Handle successful call"""
        self.failures = 0
        self.state = "closed"
    
    def _on_failure(self):
        """Handle failed call"""
        self.failures += 1
        self.last_failure_time = datetime.utcnow()
        
        if self.failures >= self.failure_threshold:
            self.state = "open"
    
    def _should_attempt_reset(self) -> bool:
        """Check if circuit should attempt reset"""
        if self.last_failure_time is None:
            return True
        
        elapsed = (datetime.utcnow() - self.last_failure_time).total_seconds()
        return elapsed >= self.timeout

class ErrorRecoveryManager:
    """Comprehensive error recovery"""
    
    def __init__(self, observability):
        self.observability = observability
        self.circuit_breakers = {}
    
    async def execute_with_retry(
        self,
        func: Callable,
        retry_policy: RetryPolicy,
        *args,
        **kwargs
    ) -> Any:
        """Execute function with retry logic"""
        
        for attempt in range(retry_policy.max_retries + 1):
            try:
                result = await func(*args, **kwargs)
                return result
            
            except Exception as e:
                severity = self._classify_error(e)
                
                if severity == ErrorSeverity.FATAL:
                    self.observability.log_step_error(
                        kwargs.get("execution_id"),
                        kwargs.get("step_id"),
                        f"Fatal error: {str(e)}"
                    )
                    raise
                
                if attempt < retry_policy.max_retries:
                    delay = retry_policy.get_delay(attempt)
                    self.observability.logger.warning(
                        f"Attempt {attempt + 1} failed, retrying in {delay}s: {str(e)}"
                    )
                    await asyncio.sleep(delay)
                else:
                    self.observability.log_step_error(
                        kwargs.get("execution_id"),
                        kwargs.get("step_id"),
                        f"Max retries exceeded: {str(e)}"
                    )
                    raise
    
    def _classify_error(self, error: Exception) -> ErrorSeverity:
        """Classify error severity"""
        # Network errors - transient
        if isinstance(error, (ConnectionError, TimeoutError)):
            return ErrorSeverity.TRANSIENT
        
        # Rate limits - recoverable
        if "rate limit" in str(error).lower():
            return ErrorSeverity.RECOVERABLE
        
        # Validation errors - fatal
        if isinstance(error, ValueError):
            return ErrorSeverity.FATAL
        
        # Default to recoverable
        return ErrorSeverity.RECOVERABLE
    
    def get_circuit_breaker(self, service_name: str) -> CircuitBreaker:
        """Get or create circuit breaker for service"""
        if service_name not in self.circuit_breakers:
            self.circuit_breakers[service_name] = CircuitBreaker()
        return self.circuit_breakers[service_name]
```

---

### 7️⃣ **Cost Optimization** ❌ MISSING

**What's Needed**:
- Token usage tracking
- Cost attribution per workflow
- Budget limits and alerts
- Model selection optimization
- Caching strategies

**Implementation**:
```python
# /tools/L3_analysis/cost_optimizer.py
from typing import Dict, Any
from datetime import datetime
import json

class CostOptimizer:
    """Track and optimize LLM costs"""
    
    # Token costs per 1K tokens (USD)
    MODEL_COSTS = {
        "gemini-2.0-flash-exp": {"input": 0.0, "output": 0.0},  # Free tier
        "gemini-1.5-pro": {"input": 0.00125, "output": 0.005},
        "gpt-4": {"input": 0.03, "output": 0.06},
        "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},
        "claude-3-opus": {"input": 0.015, "output": 0.075},
        "claude-3-sonnet": {"input": 0.003, "output": 0.015}
    }
    
    def __init__(self, state_manager, observability):
        self.state_manager = state_manager
        self.observability = observability
        self.cache = {}  # Simple in-memory cache
    
    def track_usage(
        self,
        execution_id: str,
        step_id: str,
        model: str,
        input_tokens: int,
        output_tokens: int
    ) -> Dict[str, Any]:
        """Track token usage and calculate cost"""
        
        costs = self.MODEL_COSTS.get(model, {"input": 0, "output": 0})
        
        input_cost = (input_tokens / 1000) * costs["input"]
        output_cost = (output_tokens / 1000) * costs["output"]
        total_cost = input_cost + output_cost
        
        usage_data = {
            "execution_id": execution_id,
            "step_id": step_id,
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "cost_usd": total_cost,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Store in database
        self.state_manager.storage.table("token_usage").insert(usage_data).execute()
        
        # Log metrics
        self.observability.track_token_usage(
            execution_id, step_id, input_tokens + output_tokens, total_cost
        )
        
        return usage_data
    
    def get_workflow_cost(self, execution_id: str) -> Dict[str, Any]:
        """Get total cost for a workflow execution"""
        result = self.state_manager.storage.table("token_usage").select(
            "model, input_tokens, output_tokens, cost_usd"
        ).eq("execution_id", execution_id).execute()
        
        total_cost = sum(row["cost_usd"] for row in result.data)
        total_tokens = sum(row["input_tokens"] + row["output_tokens"] for row in result.data)
        
        return {
            "execution_id": execution_id,
            "total_cost_usd": total_cost,
            "total_tokens": total_tokens,
            "breakdown": result.data
        }
    
    def suggest_model(self, task_complexity: str, budget_limit: float = None) -> str:
        """Suggest optimal model based on task and budget"""
        
        if task_complexity == "simple":
            return "gemini-2.0-flash-exp"  # Free and fast
        elif task_complexity == "medium":
            if budget_limit and budget_limit < 0.01:
                return "gpt-3.5-turbo"
            return "gemini-1.5-pro"
        else:  # complex
            if budget_limit and budget_limit < 0.05:
                return "claude-3-sonnet"
            return "gpt-4"
    
    def check_budget_limit(self, execution_id: str, limit_usd: float) -> bool:
        """Check if execution is within budget"""
        cost_data = self.get_workflow_cost(execution_id)
        return cost_data["total_cost_usd"] <= limit_usd
    
    def cache_response(self, prompt: str, response: str, model: str):
        """Cache LLM response to avoid redundant calls"""
        cache_key = f"{model}:{hash(prompt)}"
        self.cache[cache_key] = {
            "response": response,
            "timestamp": datetime.utcnow(),
            "hits": 0
        }
    
    def get_cached_response(self, prompt: str, model: str, max_age_hours: int = 24):
        """Get cached response if available"""
        cache_key = f"{model}:{hash(prompt)}"
        
        if cache_key in self.cache:
            cached = self.cache[cache_key]
            age = (datetime.utcnow() - cached["timestamp"]).total_seconds() / 3600
            
            if age < max_age_hours:
                cached["hits"] += 1
                return cached["response"]
        
        return None
```

**Database Schema**:
```sql
-- token_usage table
CREATE TABLE token_usage (
    id SERIAL PRIMARY KEY,
    execution_id TEXT NOT NULL,
    step_id TEXT NOT NULL,
    model TEXT NOT NULL,
    input_tokens INTEGER NOT NULL,
    output_tokens INTEGER NOT NULL,
    total_tokens INTEGER NOT NULL,
    cost_usd DECIMAL(10, 6) NOT NULL,
    timestamp TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_usage_execution ON token_usage(execution_id);
CREATE INDEX idx_usage_timestamp ON token_usage(timestamp);
```

---

## 🏗️ Hosting Architecture

### **4-Layer Deployment Structure**

```
┌─────────────────────────────────────────────────────────┐
│                    L4: SYNTHESIS                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Workflow Engine (Orchestration)                  │  │
│  │  - API Gateway (FastAPI/Flask)                    │  │
│  │  - Workflow Scheduler (Celery/Temporal)           │  │
│  │  - Agent Coordinator                              │  │
│  └──────────────────────────────────────────────────┘  │
│         Hosting: Cloud Run / ECS / Kubernetes          │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                   L3: ANALYSIS                           │
│  ┌──────────────────────────────────────────────────┐  │
│  │  State Manager (PostgreSQL/Supabase)              │  │
│  │  Observability (Prometheus + Grafana)             │  │
│  │  Error Recovery & Circuit Breakers                │  │
│  │  Cost Optimizer                                   │  │
│  └──────────────────────────────────────────────────┘  │
│         Hosting: Managed Database + Monitoring         │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                  L2: FOUNDATION                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │  MCP Client (Tool Integration)                    │  │
│  │  Agent Helpers (LLM Wrappers)                     │  │
│  │  Message Queue (Redis/RabbitMQ)                   │  │
│  └──────────────────────────────────────────────────┘  │
│         Hosting: Serverless Functions / Containers     │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                   L1: CONFIG                             │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Environment Variables (.env)                     │  │
│  │  API Keys (Secrets Manager)                       │  │
│  │  Model Configs (YAML/JSON)                        │  │
│  └──────────────────────────────────────────────────┘  │
│         Hosting: AWS Secrets / GCP Secret Manager      │
└─────────────────────────────────────────────────────────┘
```

### **Recommended Hosting Options**

#### **Option 1: Serverless (Low Cost, Auto-Scale)**
- **API**: Google Cloud Run / AWS Lambda
- **Database**: Supabase (PostgreSQL)
- **Queue**: Redis Cloud / AWS SQS
- **Monitoring**: Google Cloud Monitoring / AWS CloudWatch
- **Cost**: ~$20-50/month for moderate usage

#### **Option 2: Container-Based (More Control)**
- **Orchestration**: Kubernetes (GKE/EKS) or Docker Compose
- **API**: FastAPI in containers
- **Database**: Managed PostgreSQL (RDS/Cloud SQL)
- **Queue**: RabbitMQ / Redis
- **Monitoring**: Prometheus + Grafana
- **Cost**: ~$100-200/month

#### **Option 3: Hybrid (Best of Both)**
- **API**: Cloud Run (serverless)
- **Workers**: Kubernetes for long-running workflows
- **Database**: Supabase
- **Queue**: Redis Cloud
- **Monitoring**: Datadog / New Relic
- **Cost**: ~$50-150/month

---

## 🚀 Practical Implementation Guide

### **Step 1: Create a Simple Workflow**

```python
# /examples/simple_workflow.py
from tools.L4_synthesis.workflow_engine import WorkflowEngine, WorkflowDefinition, WorkflowStep, StepType
from tools.L3_analysis.state_manager import StateManager
from tools.L3_analysis.observability import ObservabilityService

# Initialize components
state_manager = StateManager(storage_backend="supabase")
observability = ObservabilityService()
engine = WorkflowEngine(state_manager, observability)

# Define workflow
workflow = WorkflowDefinition(
    name="research_workflow",
    version="1.0",
    steps=[
        WorkflowStep(
            id="research",
            type=StepType.AGENT_TASK,
            agent_role="researcher",
            task="Research {topic}",
            outputs=["findings"]
        ),
        WorkflowStep(
            id="summarize",
            type=StepType.AGENT_TASK,
            agent_role="writer",
            task="Summarize: {findings}",
            outputs=["summary"]
        )
    ]
)

# Register and execute
engine.register_workflow(workflow)
result = await engine.execute_workflow("research_workflow", {"topic": "AI agents"})
print(result["summary"])
```

### **Step 2: Create an Agentic App**

```python
# /apps/agent_api.py
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel

app = FastAPI(title="Antigravity Agent API")

class WorkflowRequest(BaseModel):
    workflow_name: str
    inputs: dict

@app.post("/workflows/execute")
async def execute_workflow(request: WorkflowRequest, background_tasks: BackgroundTasks):
    """Execute workflow asynchronously"""
    execution_id = state_manager.create_execution(request.workflow_name, request.inputs)
    
    # Run in background
    background_tasks.add_task(
        engine.execute_workflow,
        request.workflow_name,
        request.inputs
    )
    
    return {"execution_id": execution_id, "status": "started"}

@app.get("/workflows/{execution_id}")
async def get_workflow_status(execution_id: str):
    """Get workflow execution status"""
    execution = state_manager.get_execution(execution_id)
    return execution

@app.post("/workflows/{execution_id}/pause")
async def pause_workflow(execution_id: str):
    """Pause running workflow"""
    state_manager.pause_execution(execution_id)
    return {"status": "paused"}

@app.post("/workflows/{execution_id}/resume")
async def resume_workflow(execution_id: str):
    """Resume paused workflow"""
    state_manager.resume_execution(execution_id)
    return {"status": "resumed"}
```

**Deploy**:
```bash
# Build container
docker build -t antigravity-api .

# Deploy to Cloud Run
gcloud run deploy antigravity-api \
  --image gcr.io/PROJECT_ID/antigravity-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## 📊 Next Steps

1. **Implement missing components** in order of priority:
   - State Management (critical for production)
   - Workflow Engine (core orchestration)
   - Observability (debugging and monitoring)
   - Error Recovery (reliability)
   - Cost Optimization (efficiency)
   - Pattern Library (developer experience)
   - Human-in-the-Loop (governance)

2. **Set up hosting infrastructure**:
   - Choose deployment option (serverless recommended for start)
   - Configure Supabase database
   - Set up monitoring

3. **Build example workflows**:
   - Start with simple sequential workflows
   - Add parallel processing
   - Implement human review checkpoints

4. **Create reusable patterns**:
   - Document common patterns
   - Build pattern library
   - Share with team

Would you like me to implement any of these components first?
