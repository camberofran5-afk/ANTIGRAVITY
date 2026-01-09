# ⚡ QUICK REFERENCE CARD

**Print this or keep it visible when working with Antigravity**

---

## 🚀 EVERY SESSION STARTUP

### 1. Technical Setup (30 seconds)
```bash
cd /Users/franciscocambero/Anitgravity
./onboard.sh
```

### 2. Load Context in Antigravity (Copy-Paste)
```
I'm starting a new session on the Antigravity project.

Context needed:
1. Read agents.md to understand the system architecture
2. Check task.md for current work status
3. Review recent git commits (last 10)
4. Check logs/app.log for recent activity

My goal for this session: [YOUR GOAL]

Please help me:
- Understand what's been done recently
- Identify any blockers or issues
- Suggest next steps
```

---

## 🎯 5 PROMPTING PATTERNS

### Pattern 1: Single-Agent Task
```
I need to [GOAL].

Please work as Agent-[Database/AI/API/QA]:
- Analyze current state
- Propose implementation plan
- Execute changes
- Verify everything works
```

### Pattern 2: Multi-Agent Parallel
```
I need to build [FEATURE].

@Agent-Database: [DB tasks]
@Agent-AI: [AI tasks]
@Agent-API: [API tasks]

Create task.md to track progress.
```

### Pattern 3: Discovery & Planning
```
I want to [GOAL], but not sure how.

Please:
1. Research codebase
2. Propose 2-3 options
3. Recommend best approach
4. Create implementation plan

Don't code yet - I'll review first.
```

### Pattern 4: Quality Assurance
```
Please act as Agent-QA:
1. Review [AREA/FILES]
2. Check Quality Rubric
3. Run tests
4. Create quality report
```

### Pattern 5: Self-Annealing (Bug Fixes)
```
I'm experiencing [PROBLEM].

Use Self-Annealing Protocol:
1. Detect: Analyze error
2. Diagnose: Root cause
3. Fix: Implement solution
4. Anneal: Prevent recurrence
```

---

## 🏗️ 4-LAYER HIERARCHY

```
L4: Synthesis    → API endpoints, integrations
L3: Analysis     → Business logic
L2: Foundation   → Validation, data quality
L1: Configuration → Constants, config
```

**Data flows UPWARD only. No circular dependencies.**

---

## 👥 AGENT ROLES

| Role | Focus | Commits |
|------|-------|---------|
| Agent-Database | L1-L3 DB/schema | `[DB]` |
| Agent-AI | L2-L3 LLM/AI | `[AI]` |
| Agent-API | L4 endpoints | `[API]` |
| Agent-QA | Tests/docs | `[QA]` |

---

## 📋 TASK NOTATION

- `[ ]` = Available
- `[/]` = In Progress
- `[x]` = Complete

---

## ✅ 10 COMMANDMENTS (Quality Rubric)

1. SOLID Architecture
2. Code Hygiene (PEP 8, type hints)
3. Cyclomatic Complexity (<50 lines/function)
4. Security (OWASP, input validation)
5. Agentic Optimizations
6. Observability (structured logging)
7. Performance (Big O analysis)
8. Database Efficiency (no N+1)
9. Resilience (retry logic)
10. Test Coverage

---

## 🔑 KEY COMMANDS

```bash
# Activate environment
source venv/bin/activate

# Check tasks
cat task.md

# Recent commits
git log --oneline -10

# Check logs
tail -20 logs/app.log | jq '.'

# Run tests
pytest

# Type check
mypy tools/
```

---

## 🎯 DECISION TREE

```
Have specific goal?
├─ YES
│  ├─ New feature? → Pattern 1 or 2
│  ├─ Bug/issue? → Pattern 5
│  ├─ Quality check? → Pattern 4
│  └─ Not sure how? → Pattern 3
└─ NO → Pattern 3 (Discovery)
```

---

## 📚 QUICK LINKS

- **Full Guide:** [`START_HERE.md`](file:///Users/franciscocambero/Anitgravity/START_HERE.md)
- **Constitution:** [`agents.md`](file:///Users/franciscocambero/Anitgravity/agents.md)
- **Architecture:** [`README.md`](file:///Users/franciscocambero/Anitgravity/README.md)
- **Onboarding:** [`docs/WORKSPACE_ONBOARDING.md`](file:///Users/franciscocambero/Anitgravity/docs/WORKSPACE_ONBOARDING.md)

---

**REMEMBER:**
- ✅ Be specific with goals
- ✅ Reference the architecture
- ✅ Use task.md for tracking
- ✅ Request planning before execution
- ✅ Leverage multi-agent coordination

---

**PRINT THIS AND KEEP IT VISIBLE! 📌**
