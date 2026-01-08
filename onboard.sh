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
echo "📋 Current Tasks:"
echo "----------------------------"
if [ -f "task.md" ]; then
    cat task.md
else
    echo "⚠️  task.md not found in project root."
    echo "Creating from artifact..."
    if [ -f ".gemini/antigravity/brain/582a2d0d-0f8c-4e2e-b7bf-dfbbfbbcf8b1/task.md" ]; then
        cp .gemini/antigravity/brain/582a2d0d-0f8c-4e2e-b7bf-dfbbfbbcf8b1/task.md ./task.md
        cat task.md
    fi
fi
echo ""

# Show recent activity
echo "📊 Recent Activity:"
echo "-------------------"
echo "Last 5 commits:"
git log --oneline -5 2>/dev/null || echo "No git history yet"
echo ""

echo "Last 10 log entries:"
tail -10 logs/app.log 2>/dev/null || echo "No logs yet"
echo ""

echo "✅ Onboarding complete! Ready to work."
echo ""
echo "Next steps:"
echo "1. Review task status above"
echo "2. Create feature branch: git checkout -b your-name/feature"
echo "3. Start coding!"
