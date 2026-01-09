# 🚀 START HERE - New Workspace Startup Guide

**Every time you open Antigravity, follow this guide to get oriented and productive quickly.**

---

## ⚡ QUICK START (5 Minutes)

### Step 1: Run the Onboarding Script
```bash
cd /Users/franciscocambero/Anitgravity
./onboard.sh
```

**What this does:**
- ✅ Activates virtual environment
- ✅ Pulls latest changes from git
- ✅ Shows system constitution
- ✅ Displays current tasks
- ✅ Shows recent activity

---

### Step 2: Use This Initial Prompt with Antigravity

**Copy and paste this into Antigravity:**

```
I'm starting a new session on the Antigravity project.

Context needed:
1. Read agents.md to understand the system architecture
2. Check task.md for current work status (if it exists)
3. Review recent git commits (last 10)
4. Check logs/app.log for recent activity

My goal for this session: [DESCRIBE YOUR GOAL HERE]

Please help me:
- Understand what's been done recently
- Identify any blockers or issues
- Suggest next steps based on the current state
```

**Replace `[DESCRIBE YOUR GOAL HERE]` with what you want to accomplish.**

---

## 🎯 HOW TO DIRECT THE PROJECT (After Setup)

Once Antigravity has loaded the context, use these prompting patterns to direct work effectively:

### Pattern 1: Single-Agent Task Assignment
**Use when:** You want to focus on one specific area

```
I need to [SPECIFIC GOAL].

Please work as Agent-[ROLE]:
- Analyze the current state
- Propose an implementation plan
- Execute the changes
- Verify everything works

Follow the 4-Layer Hierarchy and Quality Rubric.
```

**Example:**
```
I need to add user authentication to the system.

Please work as Agent-Database:
- Analyze the current database schema
- Propose a user authentication schema
- Execute the changes in L2/L3 layers
- Verify with test scripts

Follow the 4-Layer Hierarchy and Quality Rubric.
```

---

### Pattern 2: Multi-Agent Parallel Work
**Use when:** You have a complex feature requiring multiple specializations

```
I need to build [FEATURE NAME].

Please coordinate as multiple agents:

@Agent-Database: [Database-related tasks]
@Agent-AI: [AI/LLM-related tasks]
@Agent-API: [API/Integration tasks]

Create task.md to track progress.
Work in parallel where possible.
Coordinate via structured logging.
```

**Example:**
```
I need to build a product recommendation system.

Please coordinate as multiple agents:

@Agent-Database: Create product catalog schema, user preferences table
@Agent-AI: Build recommendation engine using Gemini embeddings
@Agent-API: Create REST endpoints for recommendations

Create task.md to track progress.
Work in parallel where possible.
Coordinate via structured logging.
```

---

### Pattern 3: Discovery & Planning Mode
**Use when:** You're not sure how to approach something

```
I want to [GOAL], but I'm not sure of the best approach.

Please:
1. Research the current codebase
2. Review agents.md architecture
3. Propose 2-3 implementation options
4. Recommend the best approach with rationale
5. Create an implementation plan

Don't start coding yet - I want to review the plan first.
```

**Example:**
```
I want to add real-time notifications, but I'm not sure of the best approach.

Please:
1. Research the current codebase
2. Review agents.md architecture
3. Propose 2-3 implementation options (Supabase Realtime, webhooks, polling)
4. Recommend the best approach with rationale
5. Create an implementation plan in docs/

Don't start coding yet - I want to review the plan first.
```

---

### Pattern 4: Quality Assurance & Review
**Use when:** You want to ensure code quality

```
Please act as Agent-QA:

1. Review recent changes in [AREA/FILES]
2. Check against the 10 Commandments Quality Rubric
3. Run all tests
4. Identify any issues or improvements
5. Create a quality report

Focus on: [SPECIFIC CONCERNS]
```

**Example:**
```
Please act as Agent-QA:

1. Review recent changes in tools/L3_analysis/
2. Check against the 10 Commandments Quality Rubric
3. Run all tests
4. Identify any issues or improvements
5. Create a quality report in docs/

Focus on: Type safety, error handling, and test coverage
```

---

### Pattern 5: Self-Annealing & Bug Fixes
**Use when:** Something broke or isn't working

```
I'm experiencing [PROBLEM DESCRIPTION].

Please use the Self-Annealing Protocol:
1. Detect: Analyze the error
2. Diagnose: Identify root cause
3. Fix: Implement solution
4. Anneal: Update directives/code to prevent recurrence

Show me the error logs and your reasoning.
```

**Example:**
```
I'm experiencing API timeouts when querying Supabase.

Please use the Self-Annealing Protocol:
1. Detect: Analyze the error in logs/app.log
2. Diagnose: Identify root cause (query efficiency, rate limits, etc.)
3. Fix: Implement solution
4. Anneal: Update directives/code to prevent recurrence

Show me the error logs and your reasoning.
```

---

## 📋 DECISION TREE: What Should I Work On?

```
┌─────────────────────────────────────┐
│  Do you have a specific goal?      │
└──────────┬──────────────────────────┘
           │
    ┌──────┴──────┐
    │             │
   YES           NO
    │             │
    │             └──> Use Pattern 3 (Discovery Mode)
    │                  Ask: "What are the highest priority tasks?"
    │
    ├─> Is it a new feature?
    │   └──> Use Pattern 1 or 2 (depending on complexity)
    │
    ├─> Is it a bug/issue?
    │   └──> Use Pattern 5 (Self-Annealing)
    │
    ├─> Is it quality/testing?
    │   └──> Use Pattern 4 (QA Review)
    │
    └─> Not sure how to approach?
        └──> Use Pattern 3 (Discovery & Planning)
```

---

## 🎓 EXAMPLE SESSION FLOW

### Scenario: Starting Fresh on a New Day

**1. Technical Setup (2 min)**
```bash
cd /Users/franciscocambero/Anitgravity
./onboard.sh
```

**2. Context Loading (1 min)**
```
I'm starting a new session on the Antigravity project.

Context needed:
1. Read agents.md to understand the system architecture
2. Check task.md for current work status
3. Review recent git commits (last 10)
4. Check logs/app.log for recent activity

My goal for this session: Continue building the analytics dashboard

Please help me:
- Understand what's been done recently
- Identify any blockers or issues
- Suggest next steps based on task.md
```

**3. Review Antigravity's Response**
- Read the summary of recent work
- Check for any blockers
- Review suggested next steps

**4. Direct the Work**
```
Based on your analysis, let's continue with the analytics dashboard.

Please work as Agent-API:
- Create the /analytics/dashboard endpoint in L4
- Integrate with the data aggregation from L3
- Add proper error handling and logging
- Write tests for the endpoint

Follow the Quality Rubric and commit with [API] prefix.
```

**5. Monitor Progress**
- Watch for structured logs
- Review code as it's created
- Ask questions if needed

**6. Wrap Up**
```
Please create a summary of what was accomplished today:
- Files modified
- Features completed
- Tests passing
- Next steps for tomorrow

Update task.md accordingly.
```

---

## 🔑 KEY PRINCIPLES FOR DIRECTING WORK

### 1. **Be Specific About Goals**
❌ Bad: "Make the app better"  
✅ Good: "Add user authentication with email/password and session management"

### 2. **Reference the Architecture**
Always mention:
- Which layer (L1, L2, L3, L4)
- Which agent role (Database, AI, API, QA)
- Quality requirements (from the 10 Commandments)

### 3. **Use the Task Tracker**
- Always ask to update `task.md`
- Use `[ ]`, `[/]`, `[x]` notation
- Track dependencies between tasks

### 4. **Request Planning Before Execution**
For complex work:
1. Ask for a plan first
2. Review the plan
3. Approve or adjust
4. Then execute

### 5. **Leverage Multi-Agent Coordination**
For big features, dispatch to multiple agent roles simultaneously:
```
@Agent-Database: [DB tasks]
@Agent-AI: [AI tasks]
@Agent-API: [API tasks]
```

---

## 📚 REFERENCE DOCUMENTS

Keep these open for quick reference:

1. **[`agents.md`](file:///Users/franciscocambero/Anitgravity/agents.md)** - System constitution & agent roles
2. **[`README.md`](file:///Users/franciscocambero/Anitgravity/README.md)** - Architecture overview & quality rubric
3. **[`task.md`](file:///Users/franciscocambero/Anitgravity/task.md)** - Current work tracker (create if missing)
4. **[`docs/WORKSPACE_ONBOARDING.md`](file:///Users/franciscocambero/Anitgravity/docs/WORKSPACE_ONBOARDING.md)** - Detailed onboarding workflow

---

## ⚠️ COMMON PITFALLS TO AVOID

### ❌ Don't: Give Vague Instructions
```
"Fix the database"
"Make it faster"
"Add AI features"
```

### ✅ Do: Be Specific and Structured
```
"Optimize the Supabase query in tools/L3_analysis/user_analytics.py to reduce N+1 queries"
"Add caching to the Gemini API calls in tools/L2_foundation/llm_helper.py"
"Build a product recommendation engine using embeddings in L3"
```

### ❌ Don't: Skip Planning for Complex Work
Starting to code immediately without understanding the architecture

### ✅ Do: Request Analysis First
```
"Before we start, please:
1. Analyze the current architecture
2. Propose 2-3 approaches
3. Recommend the best option
4. Create an implementation plan"
```

### ❌ Don't: Ignore the 4-Layer Hierarchy
Putting business logic in L1 or database code in L4

### ✅ Do: Respect the Architecture
```
"Create this in the correct layer:
- L1: Configuration only
- L2: Validation and data quality
- L3: Business logic
- L4: Integration and synthesis"
```

---

## 🎯 QUICK COMMAND REFERENCE

```bash
# Activate environment
source venv/bin/activate

# Run onboarding
./onboard.sh

# Check task status
cat task.md

# View recent commits
git log --oneline -10

# Check logs
tail -20 logs/app.log | jq '.'

# Run tests
pytest

# Type check
mypy tools/

# Create new branch
git checkout -b agent-name/feature-name
```

---

## ✅ STARTUP CHECKLIST

Before starting work, ensure:

- [ ] In correct directory (`/Users/franciscocambero/Anitgravity`)
- [ ] Virtual environment activated (see `(venv)` in terminal)
- [ ] Latest changes pulled (`git pull`)
- [ ] Read `agents.md` (understand architecture)
- [ ] Checked `task.md` (know current state)
- [ ] Reviewed recent activity (git log, logs)
- [ ] Loaded context in Antigravity (used initial prompt)
- [ ] Clear goal defined for this session

**If all checked → START DIRECTING! 🚀**

---

## 🆘 NEED HELP?

**If you're stuck, ask Antigravity:**

```
I'm not sure what to do next. Please:
1. Review the current state of the project
2. Check task.md for priorities
3. Suggest 3 high-value tasks I could work on
4. Explain the rationale for each

Help me decide what to focus on.
```

---

**YOU'RE NOW READY TO BE PRODUCTIVE! 🎉**

Every session, follow this guide and you'll always know exactly how to direct the project effectively.
