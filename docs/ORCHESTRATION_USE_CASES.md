# Orchestration Framework Integration with agents.md

## How It Works Together

Your `agents.md` defines **WHO** the agents are and **WHAT** they do.  
The orchestration framework defines **HOW** they work together and **WHEN** they execute.

```
agents.md (Constitution)          Orchestration Framework (Execution)
        ↓                                      ↓
┌─────────────────┐                  ┌──────────────────────┐
│ Agent Roles     │  ────────────→   │ Workflow Builder     │
│ - Database      │                  │ - Sequential         │
│ - AI            │                  │ - Parallel           │
│ - API           │                  │ - Debate             │
│ - QA            │                  │ - Adaptive           │
└─────────────────┘                  └──────────────────────┘
        ↓                                      ↓
┌─────────────────┐                  ┌──────────────────────┐
│ Coordination    │  ────────────→   │ State Manager        │
│ Protocol        │                  │ - Track progress     │
│ - Claim tasks   │                  │ - Checkpoints        │
│ - Log work      │                  │ - Recovery           │
│ - Commit often  │                  └──────────────────────┘
└─────────────────┘                           ↓
        ↓                          ┌──────────────────────┐
┌─────────────────┐                │ HITL Controller      │
│ 4-Layer         │  ────────────→ │ - Approval gates     │
│ Hierarchy       │                │ - Human review       │
│ L1 → L2 → L3    │                └──────────────────────┘
│      → L4       │
└─────────────────┘
```

---

## Integration Points

### 1. Agent Roles → Workflow Agents

**From agents.md:**
```markdown
**Agent-Database (Database Specialist)**
- Focus: L1 config, L2 database helpers, L3 data models
- Skills: Supabase, SQL, data modeling, RLS policies
```

**In Orchestration Framework:**
```python
from tools.L4_synthesis.agno_integration import get_agno_agent
from tools.L2_foundation.agent_helpers import AgentRole

# Get the Database agent defined in agents.md
db_agent = get_agno_agent(AgentRole.DATABASE)

# Use in workflow
workflow.add_step("design_schema", db_agent, "Design users table")
```

### 2. Coordination Protocol → State Management

**From agents.md:**
```markdown
### Coordination Protocol
1. Before starting: Run ./onboard.sh
2. Claim task: Mark [/] in task.md
3. Log work: Use structured logging
4. Commit often: Use role prefix
5. Mark complete: Update task.md to [x]
```

**In Orchestration Framework:**
```python
# Automatically handles coordination
workflow = WorkflowBuilder("Build Feature")
    .add_step("step1", agent1, task1)  # Auto-claims in task.md
    .add_step("step2", agent2, task2)  # Auto-logs progress
    .build()

result = workflow.execute()  # Auto-commits, auto-marks complete
```

### 3. 4-Layer Hierarchy → Workflow Structure

**From agents.md:**
```markdown
## 3. DOMAIN: THE 4-LAYER HIERARCHY
L1 Configuration → L2 Foundation → L3 Analysis → L4 Synthesis
```

**In Orchestration Framework:**
```python
# Workflow respects layer boundaries
workflow = (
    WorkflowBuilder("Build Auth System")
    .add_step("config", AgentRole.DATABASE, "L1: Define auth config")
    .add_step("validation", AgentRole.DATABASE, "L2: Create validators")
    .add_step("logic", AgentRole.AI, "L3: Implement auth logic")
    .add_step("api", AgentRole.API, "L4: Create auth endpoints")
    .build()
)
```

---

## Concrete Use Cases with Your Setup

### Use Case 1: Build a Complete Feature (E-Commerce Product Catalog)

**Goal:** Build a product catalog system from scratch

**Agents Involved (from agents.md):**
- Agent-Database: Schema design
- Agent-AI: Search and recommendations
- Agent-API: REST endpoints
- Agent-QA: Testing

**Orchestration:**

```python
from tools.L4_synthesis.workflow_builder import WorkflowBuilder
from tools.L2_foundation.agent_helpers import AgentRole

# Sequential workflow following 4-Layer Hierarchy
workflow = (
    WorkflowBuilder("Build Product Catalog")
    
    # L1: Configuration
    .add_step(
        "define_config",
        AgentRole.DATABASE,
        """Define product catalog configuration:
        - Product fields (name, description, price, images)
        - Category taxonomy
        - Search requirements
        """
    )
    
    # L2: Foundation (Database)
    .add_step(
        "design_schema",
        AgentRole.DATABASE,
        """Design Supabase schema:
        - products table
        - categories table
        - product_images table
        - RLS policies for access control
        """,
        depends_on=["define_config"]
    )
    
    # L2: Foundation (Validation)
    .add_step(
        "create_validators",
        AgentRole.DATABASE,
        """Create Pydantic models:
        - ProductCreate
        - ProductUpdate
        - ProductResponse
        - Input validation rules
        """,
        depends_on=["design_schema"]
    )
    
    # L3: Analysis (AI Features)
    .add_step(
        "implement_search",
        AgentRole.AI,
        """Implement semantic search:
        - Generate product embeddings
        - Create vector search function
        - Implement similarity ranking
        """,
        depends_on=["create_validators"]
    )
    
    # L4: Synthesis (API)
    .add_step(
        "create_endpoints",
        AgentRole.API,
        """Create FastAPI endpoints:
        - POST /products (create)
        - GET /products (list with search)
        - GET /products/{id} (get one)
        - PUT /products/{id} (update)
        - DELETE /products/{id} (delete)
        """,
        depends_on=["implement_search"]
    )
    
    # Testing
    .add_step(
        "write_tests",
        AgentRole.QA,
        """Write comprehensive tests:
        - Unit tests for validators
        - Integration tests for API
        - Test search functionality
        - Test RLS policies
        """,
        depends_on=["create_endpoints"]
    )
    
    # Human review before deployment
    .add_approval_gate(
        "review",
        "Review all code and tests before deployment"
    )
    
    .build()
)

# Execute the workflow
result = workflow.execute()

# Results are automatically:
# - Logged to structured logs
# - Committed to git with [DB], [AI], [API], [QA] prefixes
# - Tracked in task.md
# - Stored in Supabase for audit trail
```

**Output:**
```
✅ L1 Config: Product catalog configuration defined
✅ L2 Schema: Supabase tables created with RLS
✅ L2 Validators: Pydantic models created
✅ L3 Search: Semantic search implemented
✅ L4 API: FastAPI endpoints created
✅ QA Tests: 47 tests written, all passing
⏸️  Awaiting human review...
```

---

### Use Case 2: Research-Driven Development (New Technology Evaluation)

**Goal:** Research and evaluate whether to adopt a new technology

**Agents Involved:**
- OpenManus: Web research
- Agent-AI: Analysis and synthesis
- Agent-Database: Impact assessment
- Agent-API: Integration planning

**Orchestration:**

```python
from tools.L4_synthesis.patterns import ParallelWorkflow, DebateWorkflow
from tools.L4_synthesis.openmanus_integration import get_openmanus

# Phase 1: Parallel research on multiple aspects
research_workflow = ParallelWorkflow([
    (
        "technical_research",
        get_openmanus(),
        "Research technical capabilities of GraphQL vs REST"
    ),
    (
        "performance_research",
        get_openmanus(),
        "Research performance benchmarks GraphQL vs REST"
    ),
    (
        "adoption_research",
        get_openmanus(),
        "Research industry adoption and best practices"
    ),
    (
        "migration_research",
        get_openmanus(),
        "Research migration strategies from REST to GraphQL"
    ),
], aggregator=synthesize_research)

research_results = research_workflow.execute()

# Phase 2: Debate pattern for decision making
decision_workflow = DebateWorkflow(
    question="Should we migrate from REST to GraphQL?",
    context=research_results.synthesis,
    agents=[
        get_agno_agent(AgentRole.API),      # Pro-migration
        get_agno_agent(AgentRole.DATABASE), # Database impact
        get_agno_agent(AgentRole.QA),       # Testing concerns
    ],
    rounds=3,
    synthesizer=get_agno_agent(AgentRole.ORCHESTRATOR)
)

decision = decision_workflow.execute()

# Phase 3: If approved, create implementation plan
if decision.conclusion == "APPROVE":
    implementation_workflow = (
        WorkflowBuilder("GraphQL Migration Plan")
        .add_step("assess_impact", AgentRole.DATABASE, 
                  "Assess database query impact")
        .add_step("design_schema", AgentRole.API,
                  "Design GraphQL schema")
        .add_step("migration_plan", AgentRole.API,
                  "Create phased migration plan")
        .add_step("test_strategy", AgentRole.QA,
                  "Define testing strategy")
        .build()
    )
    
    plan = implementation_workflow.execute()
```

**Output:**
```
📊 Research Phase:
  ✅ Technical: GraphQL offers flexible querying
  ✅ Performance: 30% reduction in over-fetching
  ✅ Adoption: Used by GitHub, Shopify, Netflix
  ✅ Migration: Gradual migration recommended

🤔 Debate Phase (3 rounds):
  Agent-API: "GraphQL reduces API endpoints and improves DX"
  Agent-Database: "Concern: Complex queries may impact DB performance"
  Agent-QA: "Concern: Testing complexity increases"
  
  Synthesis: "APPROVE with conditions: Implement query complexity limits,
              gradual migration, comprehensive testing"

📋 Implementation Plan:
  ✅ Impact Assessment: 23 endpoints affected
  ✅ Schema Design: GraphQL schema created
  ✅ Migration Plan: 4-phase rollout over 8 weeks
  ✅ Test Strategy: Integration + performance tests
```

---

### Use Case 3: Autonomous Code Generation (CRUD API Generator)

**Goal:** Generate a complete CRUD API from a simple description

**Agents Involved:**
- Agent-AI: Understand requirements
- Agent-Database: Generate schema
- Agent-API: Generate endpoints
- Agent-QA: Generate tests

**Orchestration:**

```python
from tools.L4_synthesis.patterns import AdaptiveWorkflow

# Adaptive workflow - agents collaborate dynamically
workflow = AdaptiveWorkflow(
    goal="""Generate a complete CRUD API for a blog system with:
    - Users (authentication)
    - Posts (with rich text)
    - Comments (nested)
    - Tags (many-to-many)
    - Full-text search
    """,
    
    orchestrator=get_agno_agent(AgentRole.ORCHESTRATOR),
    
    specialists={
        "requirements": get_agno_agent(AgentRole.AI),
        "database": get_agno_agent(AgentRole.DATABASE),
        "api": get_agno_agent(AgentRole.API),
        "testing": get_agno_agent(AgentRole.QA),
    },
    
    # Orchestrator dynamically decides the workflow
    max_iterations=10
)

result = workflow.execute()

# Generated code is automatically:
# - Organized by 4-Layer Hierarchy
# - Committed to git
# - Documented
# - Tested
```

**What Happens:**

```
Iteration 1: Orchestrator → Requirements Agent
  "Break down blog system requirements"
  
Iteration 2: Orchestrator → Database Agent
  "Design schema for users, posts, comments, tags"
  
Iteration 3: Database Agent → Orchestrator
  "Schema designed, need approval for RLS policies"
  
Iteration 4: Orchestrator → Database Agent
  "Implement RLS policies for multi-tenant blog"
  
Iteration 5: Orchestrator → API Agent
  "Generate FastAPI endpoints for all entities"
  
Iteration 6: API Agent → Database Agent
  "Need help with complex search query"
  
Iteration 7: Database Agent → API Agent
  "Here's the optimized search query with indexes"
  
Iteration 8: Orchestrator → Testing Agent
  "Generate comprehensive test suite"
  
Iteration 9: Testing Agent → Orchestrator
  "Tests generated, found 3 edge cases to handle"
  
Iteration 10: Orchestrator → API Agent
  "Fix edge cases identified by testing"
  
✅ Complete blog API generated with 47 files, 2,341 lines of code
```

---

### Use Case 4: Daily Automated Workflows (Data Pipeline)

**Goal:** Run daily data analysis and reporting

**Agents Involved:**
- Agent-Database: Data extraction
- Agent-AI: Analysis and insights
- Agent-API: Report generation

**Orchestration:**

```python
from tools.L4_synthesis.workflow_builder import WorkflowBuilder
import schedule

# Define the daily workflow
daily_workflow = (
    WorkflowBuilder("Daily Analytics Report")
    
    # Extract data
    .add_step(
        "extract_data",
        AgentRole.DATABASE,
        """Extract yesterday's data:
        - User signups
        - Product views
        - Purchases
        - Search queries
        """
    )
    
    # Parallel analysis
    .add_parallel_steps([
        ("user_analysis", AgentRole.AI, "Analyze user behavior patterns"),
        ("product_analysis", AgentRole.AI, "Analyze product performance"),
        ("search_analysis", AgentRole.AI, "Analyze search trends"),
    ])
    
    # Synthesize insights
    .add_step(
        "generate_insights",
        AgentRole.AI,
        "Synthesize insights and recommendations",
        depends_on=["user_analysis", "product_analysis", "search_analysis"]
    )
    
    # Generate report
    .add_step(
        "create_report",
        AgentRole.API,
        "Generate PDF report and send to stakeholders",
        depends_on=["generate_insights"]
    )
    
    .build()
)

# Schedule to run daily at 6 AM
schedule.every().day.at("06:00").do(daily_workflow.execute)

# Run scheduler
while True:
    schedule.run_pending()
    time.sleep(60)
```

---

### Use Case 5: Human-in-the-Loop Approval Workflow

**Goal:** Deploy code to production with human oversight

**Agents Involved:**
- Agent-QA: Run tests
- Agent-API: Build and package
- Human: Review and approve
- Agent-API: Deploy

**Orchestration:**

```python
deployment_workflow = (
    WorkflowBuilder("Production Deployment")
    
    # Automated testing
    .add_step(
        "run_tests",
        AgentRole.QA,
        "Run full test suite (unit, integration, e2e)"
    )
    
    # Build
    .add_step(
        "build",
        AgentRole.API,
        "Build production bundle and Docker image",
        depends_on=["run_tests"]
    )
    
    # Security scan
    .add_step(
        "security_scan",
        AgentRole.QA,
        "Run security vulnerability scan",
        depends_on=["build"]
    )
    
    # HUMAN APPROVAL GATE
    .add_approval_gate(
        "review_deployment",
        """Review before production deployment:
        - All tests passed?
        - No security vulnerabilities?
        - Release notes complete?
        - Rollback plan ready?
        """,
        timeout_hours=24,
        required_approvers=["tech_lead", "product_manager"]
    )
    
    # Deploy to staging
    .add_step(
        "deploy_staging",
        AgentRole.API,
        "Deploy to staging environment"
    )
    
    # Smoke tests
    .add_step(
        "smoke_tests",
        AgentRole.QA,
        "Run smoke tests on staging",
        depends_on=["deploy_staging"]
    )
    
    # ANOTHER APPROVAL GATE
    .add_approval_gate(
        "approve_production",
        "Approve production deployment after staging verification"
    )
    
    # Deploy to production
    .add_step(
        "deploy_production",
        AgentRole.API,
        "Deploy to production with blue-green strategy"
    )
    
    # Monitor
    .add_step(
        "monitor",
        AgentRole.QA,
        "Monitor production for 1 hour, auto-rollback if errors",
        depends_on=["deploy_production"]
    )
    
    .build()
)

# Execute with notifications
result = deployment_workflow.execute(
    notify_on_approval=True,  # Send Slack/email when approval needed
    notify_on_complete=True,
    notify_on_error=True
)
```

---

## Summary: How agents.md Powers the Framework

| agents.md Defines | Orchestration Framework Uses |
|-------------------|------------------------------|
| Agent Roles (DB, AI, API, QA) | Assigns tasks to correct agents |
| Coordination Protocol | Automates task claiming, logging, commits |
| 4-Layer Hierarchy | Enforces proper layer dependencies |
| Self-Annealing | Implements error recovery |
| PTMRO Engine | Guides agent decision-making |
| Quality Rubric | Validates outputs |

**The Result:**
- ✅ Agents know their roles (agents.md)
- ✅ Framework orchestrates their collaboration
- ✅ Workflows are declarative and reusable
- ✅ Human oversight when needed
- ✅ Full observability and cost tracking
- ✅ Production-ready reliability

You can now build complete applications by just defining workflows - the agents handle the rest!
