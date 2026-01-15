"""
Senior Product Manager - Autonomous Orchestration System
Coordinates multi-agent team for ERP Ganadero development
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from enum import Enum
from dataclasses import dataclass, asdict
import structlog

logger = structlog.get_logger()


class AgentRole(str, Enum):
    """Agent roles in the team"""
    PM = "senior_pm"
    FRONTEND = "frontend_specialist"
    BACKEND = "backend_specialist"
    RESEARCH = "research_specialist"
    UX = "ux_specialist"
    INTEGRATION = "integration_specialist"
    LLM = "llm_expert"
    QA = "qa_specialist"
    DEVOPS = "devops_specialist"
    DATA = "data_engineer"
    MCP = "mcp_specialist"


class TaskStatus(str, Enum):
    """Task status"""
    BACKLOG = "backlog"
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"
    BLOCKED = "blocked"


class Priority(str, Enum):
    """Task priority"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class Task:
    """Individual task"""
    id: str
    title: str
    description: str
    assigned_to: AgentRole
    status: TaskStatus
    priority: Priority
    estimated_hours: float
    actual_hours: float = 0.0
    dependencies: List[str] = None
    blockers: List[str] = None
    created_at: str = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.blockers is None:
            self.blockers = []
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()


@dataclass
class Sprint:
    """Sprint definition"""
    id: str
    name: str
    goal: str
    start_date: str
    end_date: str
    tasks: List[Task]
    status: str = "active"
    
    def get_progress(self) -> float:
        """Calculate sprint progress"""
        if not self.tasks:
            return 0.0
        done = sum(1 for t in self.tasks if t.status == TaskStatus.DONE)
        return (done / len(self.tasks)) * 100
    
    def get_burndown(self) -> Dict[str, float]:
        """Calculate burndown metrics"""
        total_hours = sum(t.estimated_hours for t in self.tasks)
        completed_hours = sum(
            t.estimated_hours for t in self.tasks 
            if t.status == TaskStatus.DONE
        )
        remaining_hours = total_hours - completed_hours
        
        return {
            "total_hours": total_hours,
            "completed_hours": completed_hours,
            "remaining_hours": remaining_hours,
            "progress_percent": (completed_hours / total_hours * 100) if total_hours > 0 else 0
        }


class SeniorPM:
    """Senior Product Manager - Autonomous Orchestration"""
    
    def __init__(self, project_dir: str):
        self.project_dir = project_dir
        self.sprints: List[Sprint] = []
        self.current_sprint: Optional[Sprint] = None
        self.backlog: List[Task] = []
        
    def create_sprint_from_user_request(self, user_request: str) -> Sprint:
        """
        Break down user request into sprint with tasks
        
        This is where PM applies best practices:
        1. Understand requirements
        2. Break into user stories
        3. Create tasks
        4. Assign to agents
        5. Set priorities
        6. Estimate effort
        """
        logger.info("pm_creating_sprint", request=user_request)
        
        # Parse user request (in production, use LLM for this)
        sprint_id = f"sprint-{len(self.sprints) + 1}"
        sprint_name = f"Sprint {len(self.sprints) + 1}"
        
        # Create sprint
        sprint = Sprint(
            id=sprint_id,
            name=sprint_name,
            goal=user_request[:100],  # Simplified
            start_date=datetime.now().isoformat(),
            end_date=(datetime.now() + timedelta(days=14)).isoformat(),
            tasks=[]
        )
        
        # Example: Break down "Add AI analytics" into tasks
        tasks = self._decompose_request_to_tasks(user_request, sprint_id)
        sprint.tasks = tasks
        
        self.sprints.append(sprint)
        self.current_sprint = sprint
        
        logger.info("pm_sprint_created", 
                   sprint_id=sprint_id, 
                   task_count=len(tasks))
        
        return sprint
    
    def _decompose_request_to_tasks(self, request: str, sprint_id: str) -> List[Task]:
        """
        Decompose user request into tasks
        
        PM applies:
        - INVEST criteria (Independent, Negotiable, Valuable, Estimable, Small, Testable)
        - Dependency analysis
        - Resource allocation
        """
        tasks = []
        
        # Example decomposition (in production, use LLM + templates)
        if "AI analytics" in request.lower():
            tasks.extend([
                Task(
                    id=f"{sprint_id}-task-1",
                    title="Research AI provider options",
                    description="Compare OpenAI, Gemini, local LLM for cost/performance",
                    assigned_to=AgentRole.RESEARCH,
                    status=TaskStatus.TODO,
                    priority=Priority.HIGH,
                    estimated_hours=4.0
                ),
                Task(
                    id=f"{sprint_id}-task-2",
                    title="Design LLM integration architecture",
                    description="Create provider abstraction, caching, prompt system",
                    assigned_to=AgentRole.LLM,
                    status=TaskStatus.TODO,
                    priority=Priority.CRITICAL,
                    estimated_hours=8.0,
                    dependencies=[f"{sprint_id}-task-1"]
                ),
                Task(
                    id=f"{sprint_id}-task-3",
                    title="Implement AI analytics endpoints",
                    description="Create /analytics/* endpoints for health, finance, etc",
                    assigned_to=AgentRole.BACKEND,
                    status=TaskStatus.TODO,
                    priority=Priority.HIGH,
                    estimated_hours=12.0,
                    dependencies=[f"{sprint_id}-task-2"]
                ),
                Task(
                    id=f"{sprint_id}-task-4",
                    title="Build AI insight UI components",
                    description="Create AIInsightCard, integrate into dashboard",
                    assigned_to=AgentRole.FRONTEND,
                    status=TaskStatus.TODO,
                    priority=Priority.MEDIUM,
                    estimated_hours=6.0,
                    dependencies=[f"{sprint_id}-task-3"]
                ),
                Task(
                    id=f"{sprint_id}-task-5",
                    title="Test AI integration end-to-end",
                    description="Verify AI responses, error handling, performance",
                    assigned_to=AgentRole.QA,
                    status=TaskStatus.TODO,
                    priority=Priority.HIGH,
                    estimated_hours=4.0,
                    dependencies=[f"{sprint_id}-task-4"]
                )
            ])
        
        return tasks
    
    def get_next_task_for_agent(self, agent: AgentRole) -> Optional[Task]:
        """
        Get next available task for agent
        
        PM considers:
        - Agent availability
        - Task dependencies
        - Priority
        - Sprint goals
        """
        if not self.current_sprint:
            return None
        
        # Find highest priority task for this agent that's ready
        available_tasks = [
            t for t in self.current_sprint.tasks
            if t.assigned_to == agent
            and t.status == TaskStatus.TODO
            and self._dependencies_met(t)
        ]
        
        if not available_tasks:
            return None
        
        # Sort by priority
        priority_order = {
            Priority.CRITICAL: 0,
            Priority.HIGH: 1,
            Priority.MEDIUM: 2,
            Priority.LOW: 3
        }
        available_tasks.sort(key=lambda t: priority_order[t.priority])
        
        return available_tasks[0]
    
    def _dependencies_met(self, task: Task) -> bool:
        """Check if all task dependencies are complete"""
        if not task.dependencies:
            return True
        
        for dep_id in task.dependencies:
            dep_task = self._find_task(dep_id)
            if not dep_task or dep_task.status != TaskStatus.DONE:
                return False
        return True
    
    def _find_task(self, task_id: str) -> Optional[Task]:
        """Find task by ID"""
        if not self.current_sprint:
            return None
        for task in self.current_sprint.tasks:
            if task.id == task_id:
                return task
        return None
    
    def update_task_status(self, task_id: str, status: TaskStatus, 
                          actual_hours: Optional[float] = None):
        """Update task status"""
        task = self._find_task(task_id)
        if not task:
            logger.warning("pm_task_not_found", task_id=task_id)
            return
        
        old_status = task.status
        task.status = status
        
        if status == TaskStatus.IN_PROGRESS and not task.started_at:
            task.started_at = datetime.now().isoformat()
        
        if status == TaskStatus.DONE:
            task.completed_at = datetime.now().isoformat()
            if actual_hours:
                task.actual_hours = actual_hours
        
        logger.info("pm_task_updated",
                   task_id=task_id,
                   old_status=old_status,
                   new_status=status)
    
    def identify_blockers(self) -> List[Dict]:
        """Identify blocked tasks and suggest actions"""
        if not self.current_sprint:
            return []
        
        blockers = []
        for task in self.current_sprint.tasks:
            if task.status == TaskStatus.BLOCKED:
                blockers.append({
                    "task_id": task.id,
                    "task_title": task.title,
                    "assigned_to": task.assigned_to,
                    "blockers": task.blockers,
                    "suggested_action": self._suggest_blocker_resolution(task)
                })
        
        return blockers
    
    def _suggest_blocker_resolution(self, task: Task) -> str:
        """Suggest how to resolve blocker"""
        # PM applies problem-solving
        if task.blockers:
            if "dependency" in task.blockers[0].lower():
                return "Prioritize dependency task or find workaround"
            if "resource" in task.blockers[0].lower():
                return "Allocate additional resources or adjust timeline"
        return "Review with team in standup"
    
    def generate_daily_standup(self) -> Dict:
        """Generate daily standup report"""
        if not self.current_sprint:
            return {"error": "No active sprint"}
        
        burndown = self.current_sprint.get_burndown()
        blockers = self.identify_blockers()
        
        # Tasks by status
        status_counts = {}
        for status in TaskStatus:
            status_counts[status.value] = sum(
                1 for t in self.current_sprint.tasks if t.status == status
            )
        
        return {
            "sprint": self.current_sprint.name,
            "progress": self.current_sprint.get_progress(),
            "burndown": burndown,
            "tasks_by_status": status_counts,
            "blockers": blockers,
            "at_risk": burndown["remaining_hours"] > burndown["total_hours"] * 0.5,
            "generated_at": datetime.now().isoformat()
        }
    
    def save_sprint_state(self, filepath: str):
        """Save sprint state to file"""
        if not self.current_sprint:
            return
        
        state = {
            "sprint": {
                "id": self.current_sprint.id,
                "name": self.current_sprint.name,
                "goal": self.current_sprint.goal,
                "start_date": self.current_sprint.start_date,
                "end_date": self.current_sprint.end_date,
                "status": self.current_sprint.status
            },
            "tasks": [asdict(t) for t in self.current_sprint.tasks],
            "updated_at": datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)
        
        logger.info("pm_state_saved", filepath=filepath)
    
    def load_sprint_state(self, filepath: str):
        """Load sprint state from file"""
        if not os.path.exists(filepath):
            logger.warning("pm_state_file_not_found", filepath=filepath)
            return
        
        with open(filepath, 'r') as f:
            state = json.load(f)
        
        # Reconstruct sprint
        sprint_data = state["sprint"]
        tasks = [Task(**t) for t in state["tasks"]]
        
        self.current_sprint = Sprint(
            id=sprint_data["id"],
            name=sprint_data["name"],
            goal=sprint_data["goal"],
            start_date=sprint_data["start_date"],
            end_date=sprint_data["end_date"],
            tasks=tasks,
            status=sprint_data["status"]
        )
        
        logger.info("pm_state_loaded", sprint_id=self.current_sprint.id)


# Example usage
if __name__ == "__main__":
    pm = SeniorPM("/Users/franciscocambero/Anitgravity/projects/erp_ganadero")
    
    # User request
    user_request = "Add AI-powered analytics to dashboard with insights for health, reproduction, and finances"
    
    # PM creates sprint
    sprint = pm.create_sprint_from_user_request(user_request)
    
    # Generate standup
    standup = pm.generate_daily_standup()
    print(json.dumps(standup, indent=2))
    
    # Save state
    pm.save_sprint_state("sprint_state.json")
