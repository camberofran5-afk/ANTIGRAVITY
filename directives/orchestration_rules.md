# Orchestration Rules

## Core Principles

### 1. Communication Protocol
- **Standard Format**: All agent messages must use JSON structure
- **Message Schema**:
  ```json
  {
    "agent_id": "unique_agent_identifier",
    "timestamp": "ISO 8601 timestamp",
    "message_type": "request|response|error|status",
    "payload": {},
    "metadata": {
      "priority": "high|medium|low",
      "retry_count": 0
    }
  }
  ```

### 2. Error Handling Hierarchy
1. **Agent-Level**: Agent attempts self-correction (max 3 retries)
2. **Orchestrator-Level**: Orchestrator reroutes or provides fallback
3. **System-Level**: Log error, trigger self-annealing protocol
4. **Human Escalation**: Critical failures requiring manual intervention

### 3. Escalation Rules
- **Automatic Escalation Triggers**:
  - 3 consecutive failures on same task
  - Data quality below threshold (defined in L2)
  - Security/authentication errors
  - Resource exhaustion (timeout, memory)

### 4. Priority System
- **High Priority**: Real-time user requests, critical data updates
- **Medium Priority**: Scheduled tasks, batch processing
- **Low Priority**: Background maintenance, optimization tasks

### 5. Dependency Management
- Agents MUST declare dependencies in their directives
- Orchestrator validates dependency graph before execution
- Circular dependencies are **FORBIDDEN**
- Failed dependencies trigger graceful degradation

### 6. Data Flow Rules
- Data flows **UPWARD** through layers (L1 → L2 → L3 → L4)
- Cross-layer communication only through orchestrator
- No direct agent-to-agent communication (star topology)

### 7. Parallel Processing Guidelines
- Independent tasks execute in parallel by default
- Orchestrator manages thread pool/async execution
- Maximum concurrent agents: [configurable in system_config]
- Resource limits enforced per agent

### 8. State Management
- Agents are **stateless** (no persistent memory between calls)
- State stored in Supabase via MCP
- Orchestrator maintains execution context
- Temp folder for intermediate files (auto-cleanup after 24h)

### 9. Logging Requirements
- All agent actions logged with structured format
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Logs stored in: `/temp/logs/[date]/[agent_id].log`
- Retention: 30 days

### 10. Self-Annealing Protocol
When errors occur:
1. **Detect**: Capture full stack trace and context
2. **Diagnose**: Analyze error pattern and root cause
3. **Fix**: Apply immediate workaround if available
4. **Anneal**: Update directive or execution script to prevent recurrence
5. **Document**: Log the fix in `/docs/ANNEALING_LOG.md`

## Orchestrator Responsibilities
- Route tasks to appropriate agents based on directives
- Monitor agent health and performance
- Enforce timeout limits
- Manage retry logic
- Aggregate results from multiple agents
- Trigger self-annealing when patterns detected

## Agent Responsibilities
- Follow directive specifications exactly
- Return structured outputs
- Report errors with full context
- Validate inputs before processing
- Clean up temporary resources
