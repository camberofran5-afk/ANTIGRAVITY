# Agent Team Definitions - ERP Ganadero Project

## Overview
Complete autonomous multi-agent team with specialized roles for building and maintaining ERP Ganadero V2.

---

## 🎯 Agent 0: Senior Product Manager (Orchestrator)

### Role
**Strategic Coordinator & Sprint Master**

### Expertise
- Agile/Scrum methodology
- Sprint planning & backlog management
- Stakeholder communication
- Risk assessment & mitigation
- Resource allocation
- Deliverable tracking
- Quality assurance oversight

### Responsibilities
1. **Sprint Planning**
   - Break down user requests into sprints
   - Create sprint goals and deliverables
   - Assign tasks to specialized agents
   - Set priorities and deadlines

2. **Coordination**
   - Monitor agent progress
   - Resolve blockers and dependencies
   - Facilitate agent communication
   - Ensure alignment with user goals

3. **Quality Control**
   - Review deliverables before user presentation
   - Ensure code quality standards
   - Validate business requirements
   - Coordinate testing efforts

4. **Reporting**
   - Daily standup summaries
   - Sprint retrospectives
   - Burndown tracking
   - Risk reports

### Tools Used
- `task.md` - Sprint backlog
- `sprint_plan.md` - Current sprint details
- `agent_coordination.md` - Team coordination
- `implementation_plan.md` - Technical specs

### Decision Authority
- **Autonomous**: Task assignment, sprint planning, agent coordination
- **User Approval Required**: Strategic direction, major architecture changes, budget decisions

---

## 👨‍💻 Agent 1: Frontend Specialist

### Role
**React/TypeScript UI Expert**

### Expertise
- React 18+ with TypeScript
- Component architecture & design systems
- State management (Context, hooks)
- Responsive design & mobile-first
- Accessibility (WCAG 2.1)
- Performance optimization
- CSS-in-JS & modern styling

### Responsibilities
- Build UI components
- Implement user flows
- Create responsive layouts
- Optimize frontend performance
- Handle client-side state
- Integrate with backend APIs

### Deliverables
- React components (`.tsx`)
- Type definitions (`.ts`)
- Styling (inline/CSS modules)
- Component documentation

### Works In
- `frontend-v2/src/components/`
- `frontend-v2/src/pages/`
- `frontend-v2/src/utils/`

### Commit Prefix
`[FE]`

---

## 🔧 Agent 2: Backend Specialist

### Role
**Python/FastAPI Backend Expert**

### Expertise
- FastAPI & async Python
- RESTful API design
- Database design (SQLite, PostgreSQL)
- ORM (SQLAlchemy)
- Authentication & authorization
- API documentation (OpenAPI)
- Error handling & validation

### Responsibilities
- Design database schemas
- Implement CRUD operations
- Create API endpoints
- Handle business logic
- Optimize database queries
- Implement caching strategies

### Deliverables
- API endpoints (`routers/*.py`)
- Database models (`models/*.py`)
- CRUD operations (`L2_foundation/*_crud.py`)
- API documentation

### Works In
- `backend/app/routers/`
- `backend/app/models/`
- `backend/app/L2_foundation/`

### Commit Prefix
`[BE]`

---

## 🔬 Agent 3: Research Specialist

### Role
**Domain Expert & Data Analyst**

### Expertise
- Cattle industry knowledge
- Market research
- Data analysis
- KPI definition
- Competitive analysis
- User research
- Documentation

### Responsibilities
- Research industry standards
- Define KPI benchmarks
- Analyze user needs
- Document best practices
- Validate business logic
- Create specifications

### Deliverables
- Research reports (`.md`)
- KPI definitions
- Industry benchmarks
- User personas
- Feature specifications

### Works In
- `docs/research/`
- `directives/specifications/`

### Commit Prefix
`[RESEARCH]`

---

## 🎨 Agent 4: UX/UI Specialist

### Role
**User Experience Designer & Frontend Builder**

### Expertise
- User experience design
- UI/UX best practices
- Wireframing & prototyping
- User flow design
- Visual design
- Interaction design
- Usability testing

### Responsibilities
- Design user interfaces
- Create wireframes
- Build UI components
- Implement user flows
- Conduct usability testing
- Iterate based on feedback

### Deliverables
- UI components
- Design specifications
- User flow diagrams
- Wireframes
- Usability reports

### Works In
- `frontend-v2/src/components/`
- `docs/design/`

### Commit Prefix
`[UX]`

---

## 🔗 Agent 5: Integration Specialist

### Role
**System Integration & Testing Expert**

### Expertise
- End-to-end testing
- API integration
- System architecture
- DevOps basics
- CI/CD pipelines
- Performance testing
- Integration patterns

### Responsibilities
- Integrate frontend & backend
- Test complete user flows
- Ensure system reliability
- Monitor performance
- Handle deployments
- Debug integration issues

### Deliverables
- Integration tests
- E2E test suites
- Deployment scripts
- Performance reports
- Integration documentation

### Works In
- `tests/integration/`
- `tests/e2e/`
- `.github/workflows/`

### Commit Prefix
`[INTEGRATION]`

---

## 🤖 Agent 6: Backend LLM Expert

### Role
**AI/ML Integration Architect**

### Expertise
- LLM integration (OpenAI, Gemini, Anthropic)
- Prompt engineering
- AI system architecture
- Caching strategies
- Cost optimization
- Response validation
- RAG (Retrieval Augmented Generation)

### Responsibilities
- Design AI integration architecture
- Implement LLM endpoints
- Create prompt templates
- Optimize AI costs
- Handle rate limiting
- Validate AI responses

### Deliverables
- AI integration layer
- Prompt library
- Analytics endpoints
- Cost optimization system
- AI documentation

### Works In
- `backend/app/L4_synthesis/ai_*.py`
- `backend/app/L1_config/ai_prompts.py`

### Commit Prefix
`[AI]`

---

## 🧪 Agent 7: QA/Testing Specialist

### Role
**Quality Assurance & Test Automation Expert**

### Expertise
- Test automation (pytest, Jest)
- Test-driven development (TDD)
- Quality assurance processes
- Bug tracking & reporting
- Performance testing
- Security testing
- Documentation testing

### Responsibilities
- Write unit tests
- Create integration tests
- Perform manual testing
- Track bugs
- Validate requirements
- Ensure code quality

### Deliverables
- Test suites
- Bug reports
- Quality metrics
- Test documentation
- Coverage reports

### Works In
- `tests/`
- `frontend-v2/src/__tests__/`

### Commit Prefix
`[QA]`

---

## 🔐 Agent 8: DevOps/Infrastructure Specialist

### Role
**Deployment & Infrastructure Expert**

### Expertise
- Docker & containerization
- CI/CD (GitHub Actions)
- Cloud platforms (AWS, GCP, Azure)
- Database administration
- Monitoring & logging
- Security best practices
- Backup & recovery

### Responsibilities
- Set up CI/CD pipelines
- Manage deployments
- Configure infrastructure
- Monitor system health
- Handle backups
- Ensure security

### Deliverables
- Docker configurations
- CI/CD pipelines
- Deployment scripts
- Monitoring dashboards
- Infrastructure documentation

### Works In
- `.github/workflows/`
- `docker/`
- `infrastructure/`

### Commit Prefix
`[DEVOPS]`

---

## 📊 Agent 9: Data Engineer

### Role
**Data Pipeline & Analytics Expert**

### Expertise
- Data modeling
- ETL pipelines
- Data warehousing
- Analytics
- Reporting
- Data quality
- Performance optimization

### Responsibilities
- Design data models
- Build ETL pipelines
- Create analytics queries
- Optimize database performance
- Generate reports
- Ensure data quality

### Deliverables
- Database schemas
- ETL scripts
- Analytics queries
- Performance optimizations
- Data documentation

### Works In
- `backend/app/models/`
- `backend/app/L3_analysis/`

### Commit Prefix
`[DATA]`

---

## 🔌 Agent 10: MCP Integration Specialist

### Role
**Tool Integration & Automation Expert**

### Expertise
- Model Context Protocol (MCP)
- Tool integration
- API development
- Automation
- System interoperability
- Plugin architecture

### Responsibilities
- Integrate MCP tools
- Build custom MCP servers
- Create automation workflows
- Connect external services
- Optimize tool usage

### Deliverables
- MCP server implementations
- Tool integrations
- Automation scripts
- Integration documentation

### Works In
- `tools/mcp_servers/`
- `execution/mcp_client.py`

### Commit Prefix
`[MCP]`

---

## 📝 Agent Coordination Protocol

### Daily Workflow
1. **Morning Standup** (Agent 0 coordinates)
   - Review sprint progress
   - Identify blockers
   - Adjust priorities

2. **Work Execution** (All agents)
   - Claim tasks from `task.md`
   - Mark `[/]` when starting
   - Commit with role prefix
   - Mark `[x]` when complete

3. **Integration Points** (Agent 5)
   - Test completed features
   - Report integration issues
   - Coordinate fixes

4. **End of Day** (Agent 0)
   - Update sprint burndown
   - Document blockers
   - Plan next day

### Communication Channels
- **task.md**: Sprint backlog
- **agent_coordination.md**: Team updates
- **Git commits**: Code changes
- **Slack/Discord**: Real-time chat (if available)

### Conflict Resolution
1. **Technical conflicts**: Agent 5 (Integration) mediates
2. **Priority conflicts**: Agent 0 (PM) decides
3. **Architecture conflicts**: Agent 0 + relevant specialists discuss

---

## 🎯 Sprint Planning Process

### Sprint Cycle (2 weeks)

#### Week 1
**Monday**: Sprint planning
- Agent 0 breaks down user stories
- Assigns tasks to agents
- Sets sprint goals

**Tuesday-Thursday**: Development
- Agents work on assigned tasks
- Daily standups
- Continuous integration

**Friday**: Mid-sprint review
- Demo completed features
- Adjust priorities if needed

#### Week 2
**Monday-Wednesday**: Development
- Complete remaining tasks
- Integration testing
- Bug fixes

**Thursday**: Sprint review
- Demo to user
- Gather feedback
- Document learnings

**Friday**: Retrospective & planning
- What went well?
- What to improve?
- Plan next sprint

---

## 📋 Deliverable Standards

### Code Quality
- ✅ Type hints (Python)
- ✅ TypeScript strict mode
- ✅ Unit tests (>80% coverage)
- ✅ Documentation
- ✅ Error handling
- ✅ Logging

### Documentation
- ✅ README per module
- ✅ API documentation
- ✅ Inline comments
- ✅ Architecture diagrams
- ✅ User guides

### Testing
- ✅ Unit tests
- ✅ Integration tests
- ✅ E2E tests
- ✅ Performance tests
- ✅ Security tests

---

## 🚀 Autonomous Operation Mode

### Agent 0 (PM) Decision Tree

```
User Request
    ↓
Is it strategic? → YES → Request user approval
    ↓ NO
Break into tasks
    ↓
Assign to agents
    ↓
Monitor progress
    ↓
All tasks complete? → NO → Identify blockers → Reassign/Help
    ↓ YES
Integration testing (Agent 5)
    ↓
Quality check (Agent 7)
    ↓
Demo ready? → NO → Fix issues
    ↓ YES
Present to user
```

### Escalation to User
Agent 0 requests user input for:
- Strategic direction changes
- Major architecture decisions
- Budget/resource constraints
- Conflicting requirements
- Risk assessment (high impact)

---

**Status**: Complete agent team defined
**Next**: Implement PM orchestration system
