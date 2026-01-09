# Quick Start: Building Apps with Orchestration Framework

## 5-Minute Quickstart

### 1. Simple Sequential Workflow

```python
# examples/simple_workflow.py
from tools.L4_synthesis.workflow_builder import WorkflowBuilder
from tools.L2_foundation.agent_helpers import AgentRole

# Build a simple 3-step workflow
workflow = (
    WorkflowBuilder("My First Workflow")
    .sequential()
    .add_step("step1", AgentRole.AI, "Analyze user requirements")
    .add_step("step2", AgentRole.DATABASE, "Design database schema")
    .add_step("step3", AgentRole.API, "Create API endpoints")
    .build()
)

# Execute
result = workflow.execute()
print(result.summary)
```

### 2. Parallel Research

```python
# examples/parallel_research.py
from tools.L4_synthesis.patterns import ParallelWorkflow
from tools.L4_synthesis.openmanus_integration import get_openmanus

# Research multiple topics simultaneously
workflow = ParallelWorkflow([
    ("ai_trends", get_openmanus(), "Research AI trends 2026"),
    ("db_trends", get_openmanus(), "Research database trends 2026"),
    ("api_trends", get_openmanus(), "Research API trends 2026"),
])

results = workflow.execute()
for topic, findings in results.items():
    print(f"{topic}: {findings.summary}")
```

### 3. With Human Approval

```python
# examples/with_approval.py
workflow = (
    WorkflowBuilder("Deploy to Production")
    .add_step("build", AgentRole.API, "Build application")
    .add_approval_gate("review", "Review build before deployment")
    .add_step("deploy", AgentRole.API, "Deploy to production")
    .build()
)

result = workflow.execute()
# Workflow pauses at approval gate, sends notification
# Resumes after human approval
```

---

## Common Patterns

### Pattern 1: Full Feature Development

```python
def build_feature(feature_name: str, description: str):
    """Build a complete feature following 4-Layer Hierarchy"""
    
    workflow = (
        WorkflowBuilder(f"Build Feature: {feature_name}")
        
        # L1: Configuration
        .add_step("config", AgentRole.DATABASE, 
                  f"Define configuration for {feature_name}")
        
        # L2: Foundation
        .add_step("schema", AgentRole.DATABASE,
                  f"Design database schema for {feature_name}",
                  depends_on=["config"])
        
        .add_step("validators", AgentRole.DATABASE,
                  "Create Pydantic validators",
                  depends_on=["schema"])
        
        # L3: Analysis
        .add_step("logic", AgentRole.AI,
                  f"Implement business logic: {description}",
                  depends_on=["validators"])
        
        # L4: Synthesis
        .add_step("api", AgentRole.API,
                  "Create API endpoints",
                  depends_on=["logic"])
        
        # Testing
        .add_step("tests", AgentRole.QA,
                  "Write comprehensive tests",
                  depends_on=["api"])
        
        .build()
    )
    
    return workflow.execute()

# Usage
result = build_feature(
    "User Authentication",
    "JWT-based auth with email/password and OAuth"
)
```

### Pattern 2: Research → Decide → Implement

```python
def research_and_build(question: str, implementation_task: str):
    """Research a topic, make a decision, then implement"""
    
    # Phase 1: Research
    research = get_openmanus().research(question, max_results=10)
    
    # Phase 2: Debate and decide
    from tools.L4_synthesis.patterns import DebateWorkflow
    
    decision = DebateWorkflow(
        question=question,
        context=research.synthesis,
        agents=[
            get_agno_agent(AgentRole.DATABASE),
            get_agno_agent(AgentRole.AI),
            get_agno_agent(AgentRole.API),
        ],
        rounds=2
    ).execute()
    
    # Phase 3: Implement if approved
    if decision.conclusion == "APPROVE":
        implementation = (
            WorkflowBuilder(f"Implement: {implementation_task}")
            .add_step("design", AgentRole.DATABASE, "Design solution")
            .add_step("implement", AgentRole.API, "Implement solution")
            .add_step("test", AgentRole.QA, "Test solution")
            .build()
        ).execute()
        
        return {
            "research": research,
            "decision": decision,
            "implementation": implementation
        }
    else:
        return {
            "research": research,
            "decision": decision,
            "implementation": None
        }

# Usage
result = research_and_build(
    "Should we use PostgreSQL or MongoDB?",
    "Database migration"
)
```

### Pattern 3: Autonomous Agent Loop

```python
def autonomous_agent(goal: str, max_iterations: int = 10):
    """Fully autonomous agent that works toward a goal"""
    
    from tools.L4_synthesis.patterns import AdaptiveWorkflow
    
    workflow = AdaptiveWorkflow(
        goal=goal,
        orchestrator=get_agno_agent(AgentRole.ORCHESTRATOR),
        specialists={
            "database": get_agno_agent(AgentRole.DATABASE),
            "ai": get_agno_agent(AgentRole.AI),
            "api": get_agno_agent(AgentRole.API),
            "qa": get_agno_agent(AgentRole.QA),
            "research": get_openmanus(),
        },
        max_iterations=max_iterations,
        enable_self_correction=True
    )
    
    return workflow.execute()

# Usage
result = autonomous_agent(
    "Build a complete blog platform with authentication, posts, and comments",
    max_iterations=20
)
```

### Pattern 4: Daily Automation

```python
def setup_daily_automation():
    """Set up automated daily workflows"""
    
    import schedule
    
    # Daily analytics workflow
    analytics_workflow = (
        WorkflowBuilder("Daily Analytics")
        .add_step("extract", AgentRole.DATABASE, "Extract yesterday's data")
        .add_step("analyze", AgentRole.AI, "Analyze trends and patterns")
        .add_step("report", AgentRole.API, "Generate and send report")
        .build()
    )
    
    # Daily backup workflow
    backup_workflow = (
        WorkflowBuilder("Daily Backup")
        .add_step("backup_db", AgentRole.DATABASE, "Backup database")
        .add_step("backup_files", AgentRole.API, "Backup files to S3")
        .add_step("verify", AgentRole.QA, "Verify backup integrity")
        .build()
    )
    
    # Schedule
    schedule.every().day.at("06:00").do(analytics_workflow.execute)
    schedule.every().day.at("02:00").do(backup_workflow.execute)
    
    # Run
    while True:
        schedule.run_pending()
        time.sleep(60)

# Usage
setup_daily_automation()
```

### Pattern 5: Multi-Stage Pipeline

```python
def build_deployment_pipeline():
    """Complete CI/CD pipeline with multiple stages"""
    
    pipeline = (
        WorkflowBuilder("CI/CD Pipeline")
        
        # Stage 1: Build
        .add_parallel_steps([
            ("lint", AgentRole.QA, "Run linter"),
            ("type_check", AgentRole.QA, "Run type checker"),
            ("unit_tests", AgentRole.QA, "Run unit tests"),
        ])
        
        # Stage 2: Integration Tests
        .add_step("integration_tests", AgentRole.QA,
                  "Run integration tests",
                  depends_on=["lint", "type_check", "unit_tests"])
        
        # Stage 3: Build
        .add_step("build", AgentRole.API,
                  "Build Docker image",
                  depends_on=["integration_tests"])
        
        # Stage 4: Security
        .add_step("security_scan", AgentRole.QA,
                  "Run security scan",
                  depends_on=["build"])
        
        # Stage 5: Deploy Staging
        .add_step("deploy_staging", AgentRole.API,
                  "Deploy to staging",
                  depends_on=["security_scan"])
        
        # Stage 6: Smoke Tests
        .add_step("smoke_tests", AgentRole.QA,
                  "Run smoke tests on staging",
                  depends_on=["deploy_staging"])
        
        # Stage 7: Human Approval
        .add_approval_gate("approve_prod",
                          "Approve production deployment")
        
        # Stage 8: Deploy Production
        .add_step("deploy_prod", AgentRole.API,
                  "Deploy to production")
        
        # Stage 9: Monitor
        .add_step("monitor", AgentRole.QA,
                  "Monitor for 1 hour",
                  depends_on=["deploy_prod"])
        
        .build()
    )
    
    return pipeline.execute()

# Usage
result = build_deployment_pipeline()
```

---

## Integration with agents.md

### How Agents Are Selected

```python
# agents.md defines:
# - Agent-Database: L1-L3, Supabase, SQL
# - Agent-AI: L2-L3, Gemini, embeddings
# - Agent-API: L4, REST APIs, integrations
# - Agent-QA: Testing, documentation

# Framework automatically uses the right agent:
workflow.add_step("design_schema", AgentRole.DATABASE, ...)  # Uses Agent-Database
workflow.add_step("implement_search", AgentRole.AI, ...)     # Uses Agent-AI
workflow.add_step("create_api", AgentRole.API, ...)          # Uses Agent-API
workflow.add_step("write_tests", AgentRole.QA, ...)          # Uses Agent-QA
```

### How Coordination Works

```python
# agents.md Coordination Protocol:
# 1. Claim task: Mark [/] in task.md
# 2. Log work: Use structured logging
# 3. Commit often: Use role prefix
# 4. Mark complete: Update task.md to [x]

# Framework automates this:
workflow = WorkflowBuilder("My Workflow")
    .add_step("step1", agent, task)  # Auto-claims [/] in task.md
    .build()

result = workflow.execute()
# During execution:
# - Logs to structlog automatically
# - Commits with [DB]/[AI]/[API]/[QA] prefix
# - Marks [x] in task.md when complete
```

### How 4-Layer Hierarchy Is Enforced

```python
# agents.md defines hierarchy:
# L1 → L2 → L3 → L4 (upward flow only)

# Framework validates dependencies:
workflow = (
    WorkflowBuilder("Feature")
    .add_step("l1_config", AgentRole.DATABASE, "L1 config")
    .add_step("l2_validation", AgentRole.DATABASE, "L2 validation",
              depends_on=["l1_config"])  # ✅ Valid: L1 → L2
    .add_step("l3_logic", AgentRole.AI, "L3 logic",
              depends_on=["l2_validation"])  # ✅ Valid: L2 → L3
    .add_step("l4_api", AgentRole.API, "L4 API",
              depends_on=["l3_logic"])  # ✅ Valid: L3 → L4
    
    # This would error:
    # .add_step("bad", AgentRole.DATABASE, "L1 task",
    #           depends_on=["l4_api"])  # ❌ Invalid: L4 → L1 (downward)
    
    .build()
)
```

---

## Real-World Example: Complete Blog Platform

```python
# examples/blog_platform.py
from tools.L4_synthesis.workflow_builder import WorkflowBuilder
from tools.L2_foundation.agent_helpers import AgentRole

def build_blog_platform():
    """Build a complete blog platform from scratch"""
    
    workflow = (
        WorkflowBuilder("Blog Platform")
        
        # === L1: Configuration ===
        .add_step(
            "config",
            AgentRole.DATABASE,
            """Define blog platform configuration:
            - User roles (admin, author, reader)
            - Post statuses (draft, published, archived)
            - Comment moderation settings
            - SEO requirements
            """
        )
        
        # === L2: Database Foundation ===
        .add_step(
            "schema",
            AgentRole.DATABASE,
            """Design Supabase schema:
            - users (auth, profiles)
            - posts (title, content, metadata)
            - comments (nested, moderation)
            - tags (many-to-many)
            - RLS policies for multi-tenant
            """,
            depends_on=["config"]
        )
        
        .add_step(
            "validators",
            AgentRole.DATABASE,
            """Create Pydantic models:
            - UserCreate, UserUpdate
            - PostCreate, PostUpdate
            - CommentCreate
            - Input validation
            """,
            depends_on=["schema"]
        )
        
        # === L3: Business Logic ===
        .add_parallel_steps([
            (
                "search",
                AgentRole.AI,
                "Implement full-text search with embeddings"
            ),
            (
                "recommendations",
                AgentRole.AI,
                "Implement post recommendations based on reading history"
            ),
            (
                "moderation",
                AgentRole.AI,
                "Implement comment moderation with AI"
            ),
        ], depends_on=["validators"])
        
        # === L4: API Layer ===
        .add_step(
            "api",
            AgentRole.API,
            """Create FastAPI endpoints:
            - Auth: /auth/register, /auth/login
            - Posts: CRUD + search + recommendations
            - Comments: CRUD + moderation
            - Tags: CRUD + autocomplete
            """,
            depends_on=["search", "recommendations", "moderation"]
        )
        
        # === Testing ===
        .add_step(
            "tests",
            AgentRole.QA,
            """Write comprehensive tests:
            - Unit tests for all validators
            - Integration tests for all endpoints
            - E2E tests for user flows
            - Performance tests for search
            - Security tests for RLS
            """,
            depends_on=["api"]
        )
        
        # === Documentation ===
        .add_step(
            "docs",
            AgentRole.QA,
            """Generate documentation:
            - API documentation (OpenAPI)
            - User guide
            - Deployment guide
            - Architecture diagrams
            """,
            depends_on=["tests"]
        )
        
        # === Human Review ===
        .add_approval_gate(
            "review",
            """Review before deployment:
            - All tests passing?
            - Documentation complete?
            - Security review done?
            - Performance acceptable?
            """
        )
        
        # === Deployment ===
        .add_step(
            "deploy",
            AgentRole.API,
            "Deploy to production with monitoring"
        )
        
        .build()
    )
    
    # Execute with full observability
    result = workflow.execute(
        enable_observability=True,
        enable_cost_tracking=True,
        notify_on_approval=True
    )
    
    return result

# Run it
if __name__ == "__main__":
    result = build_blog_platform()
    
    print(f"✅ Blog platform built successfully!")
    print(f"Duration: {result.duration}s")
    print(f"Cost: ${result.cost}")
    print(f"Files created: {result.files_created}")
    print(f"Tests written: {result.tests_count}")
    print(f"Test coverage: {result.coverage}%")
```

---

## Next Steps

1. **Review the implementation plan** for full framework details
2. **Choose your first use case** from the 5 examples above
3. **Start with a simple workflow** (Pattern 1: Sequential)
4. **Gradually add complexity** (Parallel, Debate, Adaptive)
5. **Add human oversight** when needed (Approval gates)

The framework handles all the coordination, logging, and state management - you just define what you want to build!
