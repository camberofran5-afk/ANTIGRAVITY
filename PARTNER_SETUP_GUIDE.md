# 🚀 Partner Setup Guide - Complete Manual

**For:** New team members joining the Antigravity project  
**Time Required:** 30-45 minutes  
**Difficulty:** Beginner-friendly

---

## 📋 What You'll Need Before Starting

### Required Information (Get from Project Lead):

1. **GitHub Repository URL**
   - The project is at: https://github.com/camberofran5-afk/ANTIGRAVITY

2. **GitHub Access**
   - You need to be added as a collaborator to the repository
   - Ask the project lead to invite you via GitHub

3. **Environment Credentials** (Will be provided separately)
   - Supabase URL
   - Supabase API Key
   - Gemini API Key (optional)
   - OpenAI/Perplexity API Key (optional)

4. **Your Computer Requirements**
   - Mac, Linux, or Windows with WSL
   - At least 2GB free disk space
   - Internet connection

---

## 🎯 PART 1: Getting GitHub Access

### Step 1: Create a GitHub Account (If You Don't Have One)

1. Go to https://github.com in your web browser
2. Click the "Sign up" button in the top-right corner
3. Enter your email address
4. Create a password (make it strong!)
5. Choose a username (this will be your GitHub identity)
6. Complete the verification puzzle
7. Check your email and click the verification link
8. Your GitHub account is now created!

### Step 2: Get Added to the Project

1. **Send your GitHub username to the project lead**
   - Example: "My GitHub username is: john-doe-dev"

2. **Wait for the invitation email**
   - You'll receive an email from GitHub saying you've been invited to collaborate
   - Subject line will be something like: "You've been invited to collaborate on camberofran5-afk/ANTIGRAVITY"

3. **Accept the invitation**
   - Click the link in the email
   - Or go to https://github.com/camberofran5-afk/ANTIGRAVITY
   - You'll see a banner at the top saying "You've been invited"
   - Click "Accept invitation"

4. **Verify you have access**
   - Go to https://github.com/camberofran5-afk/ANTIGRAVITY
   - You should now see the repository files
   - If you see a "404 - Not Found" error, you don't have access yet

---

## 🎯 PART 2: Setting Up Your Computer

### Step 1: Install Git

**On Mac:**
1. Open Terminal (press Command + Space, type "Terminal", press Enter)
2. Type: git --version
3. If you see a version number, Git is already installed - skip to Step 2
4. If not, you'll be prompted to install Xcode Command Line Tools - click "Install"
5. Wait for installation to complete (5-10 minutes)
6. Type git --version again to verify

**On Windows:**
1. Download Git from: https://git-scm.com/download/win
2. Run the installer
3. Use all default options (just keep clicking "Next")
4. Open "Git Bash" from the Start menu
5. Type: git --version to verify

**On Linux:**
1. Open Terminal
2. Type: sudo apt-get install git (for Ubuntu/Debian)
3. Or: sudo yum install git (for Fedora/RedHat)
4. Type: git --version to verify

### Step 2: Configure Git with Your Identity

1. Open Terminal (or Git Bash on Windows)
2. Type: git config --global user.name "Your Name"
   - Replace "Your Name" with your actual name
   - Example: git config --global user.name "John Doe"
3. Type: git config --global user.email "your-email@example.com"
   - Use the same email you used for GitHub
   - Example: git config --global user.email "john@example.com"

### Step 3: Set Up GitHub Authentication

**Option A: Using Personal Access Token (Recommended)**

1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name like "Antigravity Project"
4. Set expiration to "No expiration" (or your preferred duration)
5. Check these permissions:
   - ✅ repo (all sub-options)
   - ✅ workflow
6. Scroll down and click "Generate token"
7. **IMPORTANT:** Copy the token immediately (it looks like: ghp_xxxxxxxxxxxx)
8. Save it somewhere safe - you'll need it when cloning the repository
9. You won't be able to see this token again!

**Option B: Using SSH (Advanced)**

If you prefer SSH, follow GitHub's guide at: https://docs.github.com/en/authentication/connecting-to-github-with-ssh

### Step 4: Install Python

**Check if Python is already installed:**
1. Open Terminal
2. Type: python3 --version
3. If you see "Python 3.11" or higher, you're good - skip to Step 5
4. If you see "Python 3.8" or lower, continue with installation

**On Mac:**
1. Install Homebrew first (if you don't have it):
   - Go to https://brew.sh
   - Copy the installation command and run it in Terminal
2. Type: brew install python@3.11
3. Wait for installation (5-10 minutes)
4. Type: python3 --version to verify

**On Windows:**
1. Go to https://www.python.org/downloads/
2. Download Python 3.11 or later
3. Run the installer
4. **IMPORTANT:** Check the box "Add Python to PATH"
5. Click "Install Now"
6. Open Command Prompt and type: python --version to verify

**On Linux:**
1. Type: sudo apt-get install python3.11 (Ubuntu/Debian)
2. Or follow your distribution's Python installation guide

---

## 🎯 PART 3: Getting the Project Files

### Step 1: Choose Where to Put the Project

1. Decide where you want the project folder on your computer
2. Common locations:
   - Mac: /Users/YourName/Projects/
   - Windows: C:\Users\YourName\Projects\
   - Linux: /home/YourName/Projects/

3. Create a Projects folder if you don't have one:
   - Open Terminal
   - Type: mkdir Projects
   - Type: cd Projects

### Step 2: Clone the Repository

1. Make sure you're in your Projects folder (or wherever you want the project)
2. Type: pwd (Mac/Linux) or cd (Windows) to see your current location
3. Go to https://github.com/camberofran5-afk/ANTIGRAVITY
4. Click the green "Code" button
5. Copy the HTTPS URL (should be: https://github.com/camberofran5-afk/ANTIGRAVITY.git)
6. In Terminal, type: git clone https://github.com/camberofran5-afk/ANTIGRAVITY.git
7. If prompted for username and password:
   - Username: Your GitHub username
   - Password: Paste your Personal Access Token (NOT your GitHub password!)
8. Wait for the download to complete (1-2 minutes)
9. You should see: "Cloning into 'ANTIGRAVITY'..."

### Step 3: Navigate into the Project

1. Type: cd ANTIGRAVITY
2. Type: ls (Mac/Linux) or dir (Windows) to see the files
3. You should see files like: README.md, agents.md, START_HERE.md, etc.

---

## 🎯 PART 4: Setting Up the Python Environment

### Step 1: Create a Virtual Environment

1. Make sure you're in the ANTIGRAVITY folder
2. Type: python3 -m venv venv
3. Wait for it to create the virtual environment (30 seconds)
4. You'll see a new folder called "venv" appear

### Step 2: Activate the Virtual Environment

**On Mac/Linux:**
1. Type: source venv/bin/activate
2. You should see (venv) appear at the start of your command line
3. Example: (venv) YourName@Computer ANTIGRAVITY %

**On Windows:**
1. Type: venv\Scripts\activate
2. You should see (venv) appear at the start of your command line

**Troubleshooting:**
- If you get a "permission denied" error on Windows, type: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
- Then try activating again

### Step 3: Install Required Packages

1. Make sure you see (venv) in your terminal
2. Type: pip install -r requirements.txt
3. Wait for all packages to install (2-5 minutes)
4. You'll see lots of text scrolling - this is normal
5. When it's done, you'll see "Successfully installed..." messages

### Step 4: Verify Installation

1. Type: python --version
   - Should show Python 3.11 or higher
2. Type: pip list
   - Should show a long list of installed packages
   - Look for: supabase, google-generativeai, openai, structlog, pytest

---

## 🎯 PART 5: Configuring Your Environment

### Step 1: Get Credentials from Project Lead

Ask the project lead for:
1. Supabase URL (looks like: https://xxxxx.supabase.co)
2. Supabase Anon Key (long string of characters)
3. Gemini API Key (optional, starts with: AIza...)
4. OpenAI/Perplexity API Key (optional, starts with: sk-...)

### Step 2: Create Your Environment File

1. In the ANTIGRAVITY folder, you'll see a file called: .env.example
2. Make a copy of this file and name it: .env
   - On Mac/Linux: type: cp .env.example .env
   - On Windows: type: copy .env.example .env
3. Open the .env file in a text editor:
   - Mac: type: nano .env (or use TextEdit)
   - Windows: type: notepad .env
   - Or use any code editor like VS Code

### Step 3: Fill in Your Credentials

1. You'll see placeholders like: YOUR_SUPABASE_URL_HERE
2. Replace each placeholder with the actual credentials:
   - NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
   - NEXT_PUBLIC_SUPABASE_ANON_KEY=your-actual-key-here
   - GEMINI_API_KEY=your-gemini-key-here (if you have one)
   - OPENAI_API_KEY=your-openai-key-here (if you have one)
3. Save the file
4. **IMPORTANT:** Never share this .env file or commit it to Git!

---

## 🎯 PART 6: Testing Your Setup

### Step 1: Run the Onboarding Script

1. Make sure you're in the ANTIGRAVITY folder
2. Make sure your virtual environment is activated (you see (venv))
3. Type: chmod +x onboard.sh (Mac/Linux only, to make it executable)
4. Type: ./onboard.sh (Mac/Linux) or: bash onboard.sh (Windows)
5. You should see:
   - Current directory displayed
   - Python version
   - Git status
   - System constitution preview
   - Recent activity

### Step 2: Test Supabase Connection

1. Type: python tools/test_supabase_integration.py
2. You should see:
   - "✅ Supabase client initialized successfully"
   - "✅ Database connection working"
3. If you see errors, check your .env file credentials

### Step 3: Test LLM Integration (Optional)

1. Type: python tools/test_llm_integration.py
2. You should see:
   - "✅ Gemini client initialized successfully"
   - "✅ Perplexity client initialized successfully"
3. If you don't have API keys, you'll see warnings - this is okay for now

---

## 🎯 PART 7: Opening Antigravity and Getting Started

### Step 1: Open Antigravity Application

1. Launch the Antigravity application on your computer
2. Make sure it recognizes your workspace:
   - The workspace should be: /path/to/your/ANTIGRAVITY folder
   - If not, navigate to the folder or set the workspace

### Step 2: Use the Initial Prompt

When you open Antigravity, copy and paste this prompt:

**Initial Context Loading Prompt:**

"I'm starting a new session on the Antigravity project.

Context needed:
1. Read agents.md to understand the system architecture
2. Check task.md for current work status
3. Review recent git commits (last 10)
4. Check logs/app.log for recent activity

My goal for this session: Get familiar with the project and understand the current state

Please help me:
- Understand what's been done recently
- Identify any blockers or issues
- Suggest next steps based on the current state"

### Step 3: Review the Response

Antigravity will:
1. Read the system architecture from agents.md
2. Show you recent commits and activity
3. Explain the current state of the project
4. Suggest what you can work on

### Step 4: Choose Your Agent Role

Based on the team's needs, you'll typically take on one of these roles:
- **Agent-Database:** Work on database schemas, data models (L1-L3)
- **Agent-AI:** Work on AI/LLM features, prompts (L2-L3)
- **Agent-API:** Work on API endpoints, integrations (L4)
- **Agent-QA:** Work on testing, documentation, quality assurance

Ask the project lead which role you should focus on.

---

## 🎯 PART 8: Your First Task

### Step 1: Check Available Tasks

1. In the ANTIGRAVITY folder, look for a file called: task.md
2. If it exists, open it and look for tasks marked with: [ ] (available)
3. Avoid tasks marked with: [/] (someone is already working on them)
4. Tasks marked with: [x] are complete

### Step 2: Claim a Task

1. Choose an available task that matches your agent role
2. Edit task.md and change [ ] to [/] for your task
3. Add your name: [/] YourName: Task description
4. Save the file
5. Commit this change to Git:
   - Type: git add task.md
   - Type: git commit -m "[YourRole] Claiming task: Task description"
   - Type: git push origin dev

### Step 3: Start Working

1. Use Antigravity to help you complete the task
2. Use prompts from START_HERE.md (Pattern 1-5)
3. Follow the 4-Layer Hierarchy (L1 → L2 → L3 → L4)
4. Commit your work frequently
5. When done, mark the task as [x] in task.md

---

## 🎯 PART 9: Daily Workflow

### Every Time You Start Working:

1. **Navigate to project folder**
   - Type: cd /path/to/ANTIGRAVITY

2. **Activate virtual environment**
   - Mac/Linux: source venv/bin/activate
   - Windows: venv\Scripts\activate

3. **Pull latest changes**
   - Type: git pull origin dev
   - This gets updates from other team members

4. **Run onboarding script (optional but recommended)**
   - Type: ./onboard.sh
   - Shows you recent activity and current state

5. **Open Antigravity and load context**
   - Use the initial prompt from Part 7, Step 2

6. **Check task.md**
   - See what's available, what's in progress

7. **Start working!**

### When You Finish Working:

1. **Commit your changes**
   - Type: git add .
   - Type: git commit -m "[YourRole] Description of what you did"
   - Type: git push origin dev

2. **Update task.md**
   - Mark tasks as complete [x] or still in progress [/]
   - Commit and push task.md

3. **Deactivate virtual environment**
   - Type: deactivate

---

## 🆘 Troubleshooting Common Issues

### "I can't clone the repository - Access Denied"
**Solution:** You haven't been added as a collaborator yet. Contact the project lead with your GitHub username.

### "pip install fails with permission errors"
**Solution:** Make sure your virtual environment is activated. You should see (venv) in your terminal.

### "Supabase test fails"
**Solution:** Check your .env file. Make sure the URL and keys are correct with no extra spaces.

### "I don't see (venv) in my terminal"
**Solution:** Activate the virtual environment again:
- Mac/Linux: source venv/bin/activate
- Windows: venv\Scripts\activate

### "Git push is rejected"
**Solution:** 
1. Type: git pull origin dev
2. Resolve any conflicts if they appear
3. Type: git push origin dev again

### "I'm not sure what to work on"
**Solution:** 
1. Check task.md for available tasks
2. Ask in the team chat or GitHub Discussions
3. Use Antigravity to ask: "What are the highest priority tasks I can work on?"

### "The onboard.sh script doesn't work"
**Solution:**
- Mac/Linux: Type: chmod +x onboard.sh first
- Windows: Type: bash onboard.sh instead of ./onboard.sh

---

## 📚 Important Files to Read

Once you're set up, read these files in order:

1. **START_HERE.md** - Your startup guide for every session
2. **QUICK_REFERENCE.md** - Printable cheat sheet
3. **agents.md** - System constitution and architecture
4. **README.md** - Project overview
5. **docs/TEAM_COLLABORATION.md** - How to work with the team
6. **docs/WORKSPACE_ONBOARDING.md** - Detailed onboarding info

---

## ✅ Setup Complete Checklist

Before you start working, make sure you've completed all these steps:

- [ ] Created GitHub account
- [ ] Accepted invitation to ANTIGRAVITY repository
- [ ] Installed Git on your computer
- [ ] Configured Git with your name and email
- [ ] Set up GitHub authentication (Personal Access Token)
- [ ] Installed Python 3.11 or higher
- [ ] Cloned the ANTIGRAVITY repository
- [ ] Created and activated virtual environment
- [ ] Installed all required packages (pip install -r requirements.txt)
- [ ] Created .env file with credentials
- [ ] Tested Supabase connection
- [ ] Ran onboarding script successfully
- [ ] Opened Antigravity and loaded context
- [ ] Read START_HERE.md and agents.md
- [ ] Chosen your agent role
- [ ] Ready to claim your first task!

---

## 🎉 You're Ready!

Congratulations! You're now fully set up and ready to collaborate on the Antigravity project.

**Next Steps:**
1. Check task.md for available work
2. Claim a task in your agent role
3. Use Antigravity to help you complete it
4. Commit and push your work
5. Communicate with the team via Git commits and task.md

**Remember:**
- Pull before you start working (git pull origin dev)
- Commit frequently
- Push when you're done
- Update task.md to keep the team informed
- Ask questions if you're stuck!

**Welcome to the team! 🚀**
