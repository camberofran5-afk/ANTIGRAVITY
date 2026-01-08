# 🚀 NEW WORKSPACE ONBOARDING WORKFLOW

## WHEN TO USE THIS
- Opening Antigravity for a new session
- Switching to a different project
- New team member joining the project
- After being away from the project for a while

---

## 📋 THE 5-MINUTE ONBOARDING CHECKLIST

### ✅ STEP 1: Navigate to Project Directory
```bash
cd /Users/franciscocambero/Anitgravity
```

**Why:** Ensures Antigravity recognizes the correct workspace

---

### ✅ STEP 2: Activate Virtual Environment
```bash
source venv/bin/activate
```

**Why:** Loads the correct Python packages for this project

**Verify:** Your terminal should show `(venv)` prefix

---

### ✅ STEP 3: Pull Latest Changes
```bash
git pull origin main
```

**Why:** Gets the latest code from other agents/sessions

**What to look for:**
- "Already up to date" = Good, you're current
- Files updated = Review what changed

---

### ✅ STEP 4: Read the Constitution
```bash
cat agents.md
```

**Why:** Reminds you of the system architecture and rules

**Key sections to review:**
- System architecture (4-Layer Hierarchy)
- Quality rubric (10 commandments)
- Workflow rules

**Time:** 2 minutes

---

### ✅ STEP 5: Check Current Task Status
```bash
cat task.md  # If you have this file
```

**Why:** See what's in progress, what's blocked, what's available

**Look for:**
- `[/]` = In progress (someone is working on this)
- `[ ]` = Available (you can claim this)
- `[x]` = Complete (done)

**Action:** Pick an available task or create a new one

---

### ✅ STEP 6: Review Recent Activity
```bash
# See recent commits
git log --oneline -10

# See recent logs
tail -20 logs/app.log | jq '.'
```

**Why:** Understand what other agents did recently

**What to look for:**
- Which layers were modified (L1, L2, L3, L4)
- Any errors or warnings in logs
- Patterns of work

**Time:** 1 minute

---

### ✅ STEP 7: Announce Your Presence (Optional but Recommended)
```python
from tools.L1_config import get_logger

logger = get_logger(__name__)
logger.info(
    "agent_session_started",
    agent="your_name",
    session_id="session_001",
    planned_work="Add user authentication"
)
```

**Why:** Creates audit trail of who's working when

**Benefit:** Other agents can see activity in logs

---

### ✅ STEP 8: Update Task Tracker
Edit `task.md` or create if it doesn't exist:

```markdown
## In Progress
- [/] YOUR_NAME: Add user authentication (L3)
  - [ ] Define auth logic
  - [ ] Implement password hashing
  - [ ] Add session management
```

**Why:** Prevents duplicate work, shows progress

---

## 🎯 QUICK START PROMPT FOR ANTIGRAVITY

**Copy and paste this when you open Antigravity:**

```
I'm starting a new session on the Antigravity project.

Context needed:
1. Read agents.md to understand the system architecture
2. Check task.md for current work status
3. Review recent git commits (last 10)
4. Check logs/app.log for recent activity

My goal for this session: [DESCRIBE YOUR GOAL]

Please help me:
- Understand what's been done recently
- Identify any blockers or issues
- Suggest next steps based on task.md
```

---

## 🤝 AGENT-TO-AGENT COMMUNICATION PROTOCOL

### When Starting Work:

**1. Check for Conflicts**
```bash
# See who's working on what
grep "\[/\]" task.md

# See recent commits
git log --oneline -5
```

**2. Claim Your Task**
```markdown
# In task.md
- [/] Agent_Name: Your task description
```

**3. Create Feature Branch**
```bash
git checkout -b agent-name/feature-name
```

### During Work:

**4. Log Your Progress**
```python
logger.info(
    "progress_update",
    agent="your_name",
    task="user_auth",
    status="50_percent_complete",
    next_step="implement_password_hashing"
)
```

**5. Commit Frequently**
```bash
git add .
git commit -m "[L3] Add password hashing function"
```

### When Finishing:

**6. Mark Complete**
```markdown
# In task.md
- [x] Agent_Name: Your task description
```

**7. Log Completion**
```python
logger.info(
    "task_completed",
    agent="your_name",
    task="user_auth",
    files_modified=["tools/L3_analysis/auth.py"],
    tests_passing=True
)
```

**8. Push Changes**
```bash
git push origin agent-name/feature-name
```

---

## 📖 READING THE PROJECT STATE

### Quick Health Check:
```bash
# 1. Check Python environment
python --version  # Should be 3.11.x

# 2. Check dependencies
pip list | grep -E "supabase|google-generativeai|openai|structlog"

# 3. Test database connection
./venv/bin/python tools/test_supabase_integration.py

# 4. Test LLM integration
./venv/bin/python tools/test_llm_integration.py

# 5. Check logs for errors
grep "error" logs/app.log | tail -10
```

---

## 🎓 TRAINING: Your First Multi-Agent Session

### Scenario: You're Agent 2, continuing work from Agent 1

**Agent 1 did:** Created database schema for users table

**Your task:** Build API endpoint for user registration

**Step-by-step:**

```bash
# 1. Navigate and activate
cd /Users/franciscocambero/Anitgravity
source venv/bin/activate

# 2. Pull Agent 1's changes
git pull origin main

# 3. Read what Agent 1 did
git log --oneline -5
# Output: "abc123 [L3] Add user database schema"

# 4. Check task.md
cat task.md
# See: [x] Agent 1: Create user schema
#      [ ] Agent 2: Build user registration API

# 5. Claim your task
# Edit task.md:
# [/] Agent 2: Build user registration API

# 6. Create branch
git checkout -b agent2/user-registration-api

# 7. Start work
# Create tools/L4_synthesis/user_api.py

# 8. Log progress
python -c "
from tools.L1_config import get_logger
logger = get_logger('agent2')
logger.info('api_development_started', endpoint='user_registration')
"

# 9. Commit when done
git add tools/L4_synthesis/user_api.py
git commit -m "[L4] Add user registration API endpoint"

# 10. Mark complete in task.md
# [x] Agent 2: Build user registration API

# 11. Push
git push origin agent2/user-registration-api
```

---

## 🚨 TROUBLESHOOTING

### "I don't know what to work on"
→ Check `task.md` for `[ ]` (available) tasks
→ Ask in Antigravity: "What tasks are available based on task.md?"

### "Someone else is working on my task"
→ Check `task.md` for `[/]` (in progress) tasks
→ Pick a different task or coordinate

### "I don't understand what was done before"
→ Read git log: `git log --oneline -20`
→ Read logs: `tail -50 logs/app.log`
→ Ask in Antigravity: "Summarize recent changes from git log"

### "My environment isn't working"
→ Check venv is activated: `which python`
→ Reinstall dependencies: `pip install -r requirements.txt`
→ Check .env file exists and has correct keys

---

## ✅ CHECKLIST: Am I Ready to Start?

- [ ] In correct directory (`pwd` shows Antigravity)
- [ ] Virtual environment activated (see `(venv)` in terminal)
- [ ] Latest changes pulled (`git pull`)
- [ ] Read `agents.md` (understand architecture)
- [ ] Checked `task.md` (know what's available)
- [ ] Reviewed recent activity (git log, logs)
- [ ] Claimed a task (marked `[/]` in task.md)
- [ ] Created feature branch (`git checkout -b ...`)

**If all checked → START CODING! 🚀**

---

## 🎯 COPY-PASTE ONBOARDING SCRIPT

Save this as `onboard.sh` in your project:

```bash
#!/bin/bash
echo "🚀 Antigravity Workspace Onboarding"
echo "=================================="
echo ""

# Check directory
echo "📁 Current directory: $(pwd)"
echo ""

# Activate venv
echo "🐍 Activating virtual environment..."
source venv/bin/activate
echo "✅ Python: $(python --version)"
echo ""

# Pull changes
echo "📥 Pulling latest changes..."
git pull origin main
echo ""

# Show constitution
echo "📜 System Constitution (agents.md):"
echo "-----------------------------------"
head -20 agents.md
echo "... (see full file for complete constitution)"
echo ""

# Show tasks
echo "📋 Current Tasks (task.md):"
echo "----------------------------"
if [ -f "task.md" ]; then
    cat task.md
else
    echo "⚠️  task.md not found. Create it to track work."
fi
echo ""

# Show recent activity
echo "📊 Recent Activity:"
echo "-------------------"
echo "Last 5 commits:"
git log --oneline -5
echo ""

echo "Last 10 log entries:"
tail -10 logs/app.log 2>/dev/null || echo "No logs yet"
echo ""

echo "✅ Onboarding complete! Ready to work."
echo ""
echo "Next steps:"
echo "1. Review task.md and claim a task"
echo "2. Create feature branch: git checkout -b your-name/feature"
echo "3. Start coding!"
```

**Usage:**
```bash
chmod +x onboard.sh
./onboard.sh
```

---

**YOU'RE NOW READY TO WORK IN MULTI-AGENT MODE! 🎉**

Every time you open Antigravity, run through this workflow and you'll always be in sync with other agents.
