# 🤝 Multi-Agent Team Collaboration Guide

## Overview

This guide explains how **multiple people** (or multiple Antigravity sessions) can work together on the same project, coordinating as different agent roles.

---

## 🎯 Two Collaboration Models

### Model 1: Single Person, Multiple Agent Roles (Simulated Multi-Agent)
**Use case:** You working alone, but simulating different agent specializations

**How it works:**
- One workspace (your local machine)
- One Antigravity session
- You direct work using `@Agent-Database`, `@Agent-AI`, etc. in prompts
- Git is used for version control and checkpoints

### Model 2: Multiple People, Distributed Team (True Multi-Agent)
**Use case:** Team of developers/AI users working together

**How it works:**
- Multiple workspaces (different machines/people)
- Multiple Antigravity sessions (one per person)
- Git is the **coordination layer** for sharing work
- Each person takes on one or more agent roles

---

## 🔄 Git as the Coordination Layer

**YES, Git is the primary mechanism for multi-agent team collaboration!**

### Why Git?

Git provides:
- ✅ **Shared source of truth** - Everyone sees the same code
- ✅ **Conflict resolution** - Handles when two agents modify the same file
- ✅ **Audit trail** - See who did what and when
- ✅ **Branching** - Parallel work without interference
- ✅ **Remote collaboration** - Works across different locations

### Your Git Setup

```bash
# Already configured!
origin  https://github.com/camberofran5-afk/ANTIGRAVITY.git
```

You're on the `dev` branch with remote tracking set up.

---

## 🏗️ Team Collaboration Workflow

### Step 1: Define Agent Roles for Team Members

Assign each team member (or yourself in different sessions) a primary role:

| Team Member | Agent Role | Focus Areas | Commit Prefix |
|-------------|------------|-------------|---------------|
| Person A | Agent-Database | L1-L3 DB/schema | `[DB]` |
| Person B | Agent-AI | L2-L3 LLM/AI | `[AI]` |
| Person C | Agent-API | L4 endpoints | `[API]` |
| Person D | Agent-QA | Tests/docs | `[QA]` |

**For solo work:** You can be all roles, just use the prefixes to organize work.

---

### Step 2: Establish the Git Workflow

#### Option A: Feature Branch Workflow (Recommended for Teams)

```bash
# Each agent works on their own branch
git checkout -b agent-database/user-schema
git checkout -b agent-ai/recommendation-engine
git checkout -b agent-api/rest-endpoints
```

**Benefits:**
- No conflicts between agents
- Can review each other's work via Pull Requests
- Safe experimentation

**Workflow:**
```bash
# 1. Create feature branch
git checkout -b agent-name/feature-name

# 2. Do work, commit often
git add .
git commit -m "[DB] Add user authentication schema"

# 3. Push to remote
git push origin agent-name/feature-name

# 4. Create Pull Request on GitHub
# 5. Other agents review
# 6. Merge to main/dev
```

#### Option B: Direct to Dev Branch (For Solo or Tight Coordination)

```bash
# Pull latest before starting
git pull origin dev

# Do work
git add .
git commit -m "[AI] Add recommendation engine"

# Push immediately
git push origin dev
```

**Benefits:**
- Faster iteration
- Less overhead

**Risks:**
- Potential merge conflicts
- Less review

---

### Step 3: Communication Mechanisms

#### 1. **Git Commits** (Asynchronous)
```bash
git commit -m "[DB] Created users table with RLS policies

- Added email, password_hash, created_at columns
- Implemented Row Level Security
- Added indexes for performance
- Next: Agent-AI can now build auth validator"
```

**Use for:** Documenting what was done and what's next

#### 2. **task.md** (Shared Task Tracker)
```markdown
## In Progress
- [/] Agent-Database: User authentication schema (L2/L3)
  - [x] Create users table
  - [/] Implement RLS policies
  - [ ] Add session tokens table

## Blocked
- [ ] Agent-API: Login endpoint (L4)
  - Waiting on: Agent-Database to finish session tokens

## Available
- [ ] Agent-AI: Password strength validator
- [ ] Agent-QA: Write integration tests
```

**Use for:** Real-time coordination, claiming tasks, showing blockers

#### 3. **Structured Logs** (Runtime Communication)
```python
from tools.L1_config import get_logger

logger = get_logger(__name__)
logger.info(
    "database_schema_ready",
    agent="Agent-Database",
    table="users",
    next_agent="Agent-AI",
    message="User schema complete, ready for auth validator"
)
```

**Use for:** Runtime events, debugging, audit trail

#### 4. **GitHub Issues/Discussions** (Planning)
Create issues for:
- Feature requests
- Bugs
- Architecture decisions
- Questions

**Use for:** Long-form discussion, planning, documentation

---

## 🌐 Remote Workspace Coordination

### Scenario: Two People Working Together

**Person A (Agent-Database):**
```bash
# Morning - Start work
cd /Users/personA/Anitgravity
./onboard.sh
git pull origin dev

# Check task.md
cat task.md
# See: [ ] Agent-Database: Create product catalog schema

# Claim task (edit task.md)
# Change to: [/] Agent-Database: Create product catalog schema

# Commit task claim
git add task.md
git commit -m "[DB] Claiming product catalog schema task"
git push origin dev

# Do the work
# ... create schema files ...

# Commit work
git add tools/L3_analysis/product_schema.py
git commit -m "[DB] Add product catalog schema with categories"
git push origin dev

# Update task.md
# Change to: [x] Agent-Database: Create product catalog schema
git add task.md
git commit -m "[DB] Completed product catalog schema"
git push origin dev
```

**Person B (Agent-AI) - Working simultaneously:**
```bash
# Morning - Start work
cd /Users/personB/Anitgravity
./onboard.sh
git pull origin dev

# See Person A's task claim
cat task.md
# See: [/] Agent-Database: Create product catalog schema
#      [ ] Agent-AI: Build product recommendation engine

# Claim different task
# Change to: [/] Agent-AI: Build product recommendation engine

git add task.md
git commit -m "[AI] Claiming recommendation engine task"
git push origin dev

# Do the work
# ... build recommendation engine ...

# Commit work
git add tools/L3_analysis/recommendation_engine.py
git commit -m "[AI] Add collaborative filtering recommendation engine"
git push origin dev
```

**Key Points:**
- Both pull latest changes before starting
- Both claim tasks in `task.md` to avoid duplication
- Both push regularly to keep others informed
- Git handles merging their changes automatically (since they're working on different files)

---

## 🔀 Handling Merge Conflicts

When two agents modify the same file:

```bash
# Person A pushes first
git push origin dev
# ✅ Success

# Person B tries to push
git push origin dev
# ❌ Error: Updates were rejected

# Person B resolves
git pull origin dev
# Git shows conflict in file

# Edit the file, resolve conflicts
# Look for <<<<<<< HEAD markers

# Mark as resolved
git add conflicted_file.py
git commit -m "[AI] Merge conflict resolved with Agent-Database changes"
git push origin dev
# ✅ Success
```

**Prevention:**
- Use feature branches
- Work on different layers/files when possible
- Communicate in `task.md`
- Pull frequently

---

## 📋 Complete Team Workflow Example

### Scenario: Building User Authentication System

**Sprint Planning (All Agents):**
Create `task.md`:
```markdown
# Sprint: User Authentication

## Architecture
- L1: Configuration (API keys, constants)
- L2: Validation (email format, password strength)
- L3: Business logic (auth, sessions)
- L4: API endpoints

## Tasks

### Agent-Database
- [ ] Create users table schema
- [ ] Create sessions table schema
- [ ] Implement RLS policies
- [ ] Add database indexes

### Agent-AI
- [ ] Build password strength validator (Gemini)
- [ ] Build email verification logic
- [ ] Add fraud detection (optional)

### Agent-API
- [ ] Create /register endpoint
- [ ] Create /login endpoint
- [ ] Create /logout endpoint
- [ ] Add rate limiting

### Agent-QA
- [ ] Write unit tests for auth logic
- [ ] Write integration tests for API
- [ ] Create security audit checklist
- [ ] Update documentation
```

**Day 1 - Agent-Database:**
```bash
git checkout -b agent-db/auth-schema
# Create schema files
git commit -m "[DB] Add users and sessions tables"
git push origin agent-db/auth-schema
# Create PR, mark tasks [x] in task.md
```

**Day 1 - Agent-AI (parallel):**
```bash
git checkout -b agent-ai/password-validator
# Build validator
git commit -m "[AI] Add Gemini-powered password strength validator"
git push origin agent-ai/password-validator
# Create PR
```

**Day 2 - Agent-API (depends on DB):**
```bash
git checkout dev
git pull origin dev  # Get merged DB changes
git checkout -b agent-api/auth-endpoints
# Build endpoints using DB schema
git commit -m "[API] Add register and login endpoints"
git push origin agent-api/auth-endpoints
# Create PR
```

**Day 2 - Agent-QA (parallel):**
```bash
git checkout dev
git pull origin dev  # Get all changes
git checkout -b agent-qa/auth-tests
# Write tests
git commit -m "[QA] Add comprehensive auth tests"
git push origin agent-qa/auth-tests
# Create PR
```

**Day 3 - Merge Everything:**
```bash
# Review all PRs
# Merge in order: DB → AI → API → QA
# All agents pull latest
git checkout dev
git pull origin dev
# Sprint complete!
```

---

## 🛠️ Tools for Remote Coordination

### 1. GitHub (Already Set Up)
- **Code hosting:** https://github.com/camberofran5-afk/ANTIGRAVITY
- **Pull Requests:** For code review
- **Issues:** For task tracking
- **Discussions:** For architecture decisions

### 2. Supabase (Already Integrated)
- **Shared database:** All agents read/write to same DB
- **Realtime:** Can subscribe to changes
- **Potential use:** Agent coordination table

Example coordination table:
```sql
CREATE TABLE agent_sessions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  agent_name TEXT NOT NULL,
  status TEXT NOT NULL,  -- 'active', 'idle', 'offline'
  current_task TEXT,
  last_heartbeat TIMESTAMP DEFAULT NOW()
);
```

Agents can:
- Register when they start work
- Update their current task
- See what other agents are doing
- Detect conflicts in real-time

### 3. Structured Logging (Already Implemented)
All agents log to `logs/app.log`:
```bash
# Agent A can see what Agent B did
tail -f logs/app.log | jq 'select(.agent == "Agent-Database")'
```

---

## 🚀 Quick Start for Team Members

### New Team Member Onboarding

**Step 1: Clone the repository**
```bash
git clone https://github.com/camberofran5-afk/ANTIGRAVITY.git
cd ANTIGRAVITY
```

**Step 2: Run setup**
```bash
./onboard.sh
```

**Step 3: Configure environment**
```bash
# Copy .env.example to .env
cp .env.example .env

# Add your credentials (get from team lead)
nano .env
```

**Step 4: Verify setup**
```bash
source venv/bin/activate
python tools/test_supabase_integration.py
python tools/test_llm_integration.py
```

**Step 5: Read the docs**
- `START_HERE.md` - Startup guide
- `agents.md` - System constitution
- `task.md` - Current work
- `docs/TEAM_COLLABORATION.md` - This file!

**Step 6: Claim your role**
Edit `task.md` and claim a task with your agent role.

**Step 7: Start working**
Follow the git workflow above!

---

## 🎯 Best Practices

### ✅ DO:
- **Pull before starting work** - Always `git pull origin dev`
- **Commit frequently** - Small, atomic commits
- **Use descriptive messages** - Include `[ROLE]` prefix
- **Update task.md** - Keep team informed
- **Work on different layers** - Minimize conflicts
- **Communicate blockers** - Mark tasks as blocked in task.md
- **Review others' code** - Learn and maintain quality

### ❌ DON'T:
- **Push broken code** - Run tests first
- **Work on claimed tasks** - Check task.md first
- **Ignore conflicts** - Resolve immediately
- **Skip documentation** - Update docs as you go
- **Work in isolation** - Communicate progress
- **Violate 4-Layer Hierarchy** - Respect architecture

---

## 🔍 Monitoring Team Activity

### See what everyone is doing:

```bash
# Recent commits by agent
git log --oneline --all --grep="\[DB\]" -10
git log --oneline --all --grep="\[AI\]" -10
git log --oneline --all --grep="\[API\]" -10

# Current branches
git branch -a

# Who's working on what (from task.md)
grep "\[/\]" task.md

# Recent activity in logs
tail -50 logs/app.log | jq 'select(.agent != null)'
```

---

## 🆘 Troubleshooting

### "I don't know what to work on"
→ Check `task.md` for `[ ]` (available) tasks
→ Ask in GitHub Discussions

### "Someone is working on my task"
→ Check `task.md` for `[/]` (in progress)
→ Coordinate via GitHub Issues or direct communication

### "My push was rejected"
→ Run `git pull origin dev`
→ Resolve any conflicts
→ Push again

### "I broke something"
→ Use Self-Annealing Protocol
→ Create issue in GitHub
→ Ask Agent-QA for help

---

## 📊 Summary: Agent Interaction Methods

| Method | Sync/Async | Use Case | Tool |
|--------|------------|----------|------|
| Git commits | Async | Code sharing | Git |
| task.md | Sync | Task coordination | Git + text file |
| Logs | Async | Runtime events | structlog |
| GitHub Issues | Async | Planning, bugs | GitHub |
| Supabase | Sync | Shared data | Supabase |
| Pull Requests | Async | Code review | GitHub |

---

## 🎉 You're Ready for Team Collaboration!

**For solo work:**
- Use git for version control
- Simulate agent roles with `@Agent-X` prompts
- Update `task.md` to track your own work

**For team work:**
- Use git for coordination
- Each person takes agent role(s)
- Communicate via commits, task.md, and GitHub

**The infrastructure is already in place - just start collaborating!** 🚀
