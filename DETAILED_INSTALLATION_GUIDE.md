# 🔧 DETAILED INSTALLATION GUIDE - Antigravity Project

**Complete Step-by-Step Instructions with Exact Commands**

**Estimated Time:** 45-60 minutes  
**Difficulty:** Beginner-friendly (no prior experience needed)

---

## 📋 PRE-INSTALLATION CHECKLIST

Before you begin, gather this information from the project lead:

### Required Information:
- [ ] GitHub username of project lead: **camberofran5-afk**
- [ ] Repository name: **ANTIGRAVITY**
- [ ] Your GitHub username (create one if you don't have it)
- [ ] Supabase URL (you'll get this later)
- [ ] Supabase Anon Key (you'll get this later)
- [ ] Gemini API Key (optional)
- [ ] OpenAI API Key (optional)

### Your Computer:
- [ ] Operating System: Mac, Windows, or Linux
- [ ] At least 2GB free disk space
- [ ] Administrator/sudo access
- [ ] Stable internet connection

---

## PHASE 1: GITHUB ACCOUNT & ACCESS

### Step 1.1: Create GitHub Account (Skip if you have one)

**Time: 5 minutes**

1. Open your web browser
2. Go to: **https://github.com**
3. Look at the top-right corner
4. Click the **"Sign up"** button
5. You'll see a form asking for your email

**Fill out the form:**
- Email: Enter your email address (example: yourname@gmail.com)
- Password: Create a strong password (at least 8 characters, mix of letters and numbers)
- Username: Choose a username (this will be public, example: john-developer)
- Email preferences: Choose "y" or "n" for marketing emails
- Click **"Continue"**

6. Complete the CAPTCHA puzzle (select images as requested)
7. Click **"Create account"**
8. GitHub will send a verification code to your email
9. Check your email inbox
10. Find the email from GitHub (subject: "Your GitHub launch code")
11. Copy the 6-digit code
12. Paste it into the GitHub verification page
13. You're now on GitHub!

**What you should see:**
- A welcome screen asking about your interests
- You can skip these questions or answer them
- Click **"Skip personalization"** or complete the survey

**Your GitHub username is now created!** Write it down, you'll need it.

---

### Step 1.2: Get Added as a Collaborator

**Time: 5-10 minutes (waiting for project lead)**

1. **Send this message to the project lead:**

"Hi! I'm ready to join the Antigravity project. 

My GitHub username is: [YOUR_USERNAME]

Please add me as a collaborator to the repository.

Thanks!"

2. **Wait for the project lead to add you**
   - They will go to: https://github.com/camberofran5-afk/ANTIGRAVITY/settings/access
   - They will click "Add people"
   - They will enter your GitHub username
   - They will click "Add [your-username] to this repository"

3. **Check your email**
   - You'll receive an email from GitHub
   - Subject: "[GitHub] camberofran5-afk has invited you to collaborate on the camberofran5-afk/ANTIGRAVITY repository"
   - This usually arrives within 1-2 minutes

4. **Accept the invitation**
   - Open the email
   - Click the green button: **"View invitation"**
   - You'll be taken to GitHub
   - Click the green button: **"Accept invitation"**

5. **Verify you have access**
   - Go to: **https://github.com/camberofran5-afk/ANTIGRAVITY**
   - You should see the repository files (README.md, agents.md, etc.)
   - If you see "404 - This is not the web page you are looking for", you don't have access yet

**Success indicator:** You can see the repository files and there's a green "Code" button.

---

### Step 1.3: Set Up GitHub Authentication

**Time: 5 minutes**

**Why you need this:** GitHub requires authentication to download (clone) and upload (push) code.

**Creating a Personal Access Token:**

1. Make sure you're logged into GitHub
2. Click your profile picture in the top-right corner
3. Click **"Settings"** from the dropdown menu
4. Scroll down the left sidebar
5. Click **"Developer settings"** (near the bottom)
6. Click **"Personal access tokens"**
7. Click **"Tokens (classic)"**
8. Click the button: **"Generate new token"**
9. Click **"Generate new token (classic)"**

10. **Fill out the token form:**
    - Note: Type "Antigravity Project Access"
    - Expiration: Select "No expiration" (or choose your preference)
    - Select scopes: Check these boxes:
      - ✅ **repo** (this will auto-check all sub-boxes)
      - ✅ **workflow**
    - Scroll to the bottom
    - Click **"Generate token"**

11. **CRITICAL - Save your token immediately:**
    - You'll see a green box with a token starting with "ghp_"
    - Example: ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    - Click the copy icon next to it
    - **Paste it into a text file on your computer RIGHT NOW**
    - Save the file as: github-token.txt
    - **You will NEVER see this token again!**
    - If you lose it, you'll have to create a new one

**What to save:**
Create a file called "antigravity-credentials.txt" and save:
- GitHub Username: [your-username]
- GitHub Token: ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
- Keep this file safe and private!

---

## PHASE 2: INSTALL REQUIRED SOFTWARE

### Step 2.1: Install Git

**What is Git?** Version control software that tracks changes to code.

---

#### FOR MAC USERS:

**Time: 10 minutes**

1. Open **Terminal**:
   - Press **Command (⌘) + Space** to open Spotlight
   - Type: **Terminal**
   - Press **Enter**
   - A white or black window will open

2. Check if Git is already installed:
   - Type exactly: **git --version**
   - Press **Enter**

3. **If you see a version number** (example: git version 2.39.0):
   - Git is already installed! Skip to Step 2.2
   
4. **If you see "command not found" or a popup appears:**
   - A popup will say: "The 'git' command requires the command line developer tools"
   - Click **"Install"**
   - Click **"Agree"** to the license
   - Wait 5-10 minutes for installation
   - When done, type: **git --version** again
   - You should now see a version number

**Success indicator:** Typing "git --version" shows a version number.

---

#### FOR WINDOWS USERS:

**Time: 10 minutes**

1. Open your web browser
2. Go to: **https://git-scm.com/download/win**
3. The download should start automatically
4. If not, click: **"Click here to download manually"**
5. Wait for the download (file name: Git-2.xx.x-64-bit.exe)

6. **Run the installer:**
   - Find the downloaded file (usually in Downloads folder)
   - Double-click it
   - Click **"Yes"** if Windows asks for permission

7. **Installation wizard - use these settings:**
   - Click **"Next"** (accept default location)
   - Click **"Next"** (accept default components)
   - Click **"Next"** (accept default Start Menu folder)
   - Default editor: Select **"Use Visual Studio Code"** or **"Use Notepad"**
   - Click **"Next"**
   - Branch name: Select **"Let Git decide"**
   - Click **"Next"**
   - PATH environment: Select **"Git from the command line and also from 3rd-party software"**
   - Click **"Next"**
   - SSH executable: Select **"Use bundled OpenSSH"**
   - Click **"Next"**
   - HTTPS transport: Select **"Use the OpenSSL library"**
   - Click **"Next"**
   - Line endings: Select **"Checkout Windows-style, commit Unix-style"**
   - Click **"Next"**
   - Terminal emulator: Select **"Use MinTTY"**
   - Click **"Next"**
   - Git pull behavior: Select **"Default (fast-forward or merge)"**
   - Click **"Next"**
   - Credential helper: Select **"Git Credential Manager"**
   - Click **"Next"**
   - Extra options: Check **"Enable file system caching"**
   - Click **"Next"**
   - Experimental options: Leave unchecked
   - Click **"Install"**
   - Wait 2-3 minutes
   - Click **"Finish"**

8. **Open Git Bash:**
   - Press **Windows key**
   - Type: **Git Bash**
   - Press **Enter**
   - A black terminal window will open

9. **Verify installation:**
   - Type: **git --version**
   - Press **Enter**
   - You should see: git version 2.xx.x

**Success indicator:** Git Bash opens and "git --version" shows a version number.

---

#### FOR LINUX USERS (Ubuntu/Debian):

**Time: 5 minutes**

1. Open **Terminal**:
   - Press **Ctrl + Alt + T**
   - Or search for "Terminal" in your applications

2. Type this command exactly:
   **sudo apt-get update**
   - Press **Enter**
   - Enter your password when prompted
   - Wait for it to finish

3. Type this command:
   **sudo apt-get install git**
   - Press **Enter**
   - Type **y** when asked "Do you want to continue?"
   - Press **Enter**
   - Wait for installation (2-3 minutes)

4. Verify installation:
   - Type: **git --version**
   - Press **Enter**
   - You should see: git version 2.xx.x

**Success indicator:** "git --version" shows a version number.

---

### Step 2.2: Configure Git

**Time: 2 minutes**

**This tells Git who you are for commit tracking.**

1. Open Terminal (Mac/Linux) or Git Bash (Windows)

2. Type this command (replace with YOUR name):
   **git config --global user.name "John Doe"**
   - Replace "John Doe" with your actual name
   - Keep the quotation marks
   - Press **Enter**

3. Type this command (replace with YOUR email):
   **git config --global user.email "john@example.com"**
   - Use the same email you used for GitHub
   - Keep the quotation marks
   - Press **Enter**

4. Verify your configuration:
   **git config --global --list**
   - Press **Enter**
   - You should see your name and email

**Success indicator:** You see "user.name=Your Name" and "user.email=your@email.com"

---

### Step 2.3: Install Python 3.11+

**What is Python?** The programming language this project uses.

---

#### FOR MAC USERS:

**Time: 15 minutes**

**Option A: Using Homebrew (Recommended)**

1. Check if you have Homebrew:
   - Open Terminal
   - Type: **brew --version**
   - Press **Enter**

2. **If you see a version number:** Skip to step 5

3. **If you see "command not found":** Install Homebrew:
   - Go to: **https://brew.sh**
   - Copy the installation command (starts with: /bin/bash -c)
   - Paste it into Terminal
   - Press **Enter**
   - Enter your Mac password when prompted
   - Press **Enter** when it says "Press RETURN to continue"
   - Wait 10-15 minutes for installation

4. Verify Homebrew:
   - Type: **brew --version**
   - You should see: Homebrew 4.x.x

5. Install Python:
   - Type: **brew install python@3.11**
   - Press **Enter**
   - Wait 5-10 minutes

6. Verify Python installation:
   - Type: **python3 --version**
   - Press **Enter**
   - You should see: Python 3.11.x

**Option B: Using Python.org installer**

1. Go to: **https://www.python.org/downloads/macos/**
2. Click: **"Download Python 3.11.x"**
3. Open the downloaded .pkg file
4. Click **"Continue"** through the installer
5. Click **"Install"**
6. Enter your Mac password
7. Wait for installation
8. Click **"Close"**
9. Open Terminal and type: **python3 --version**

**Success indicator:** "python3 --version" shows Python 3.11.x or higher.

---

#### FOR WINDOWS USERS:

**Time: 10 minutes**

1. Go to: **https://www.python.org/downloads/windows/**
2. Click: **"Download Python 3.11.x"** (get the latest 3.11 version)
3. Wait for download (file name: python-3.11.x-amd64.exe)

4. **Run the installer:**
   - Find the downloaded file
   - Double-click it
   - **CRITICAL:** Check the box: ✅ **"Add python.exe to PATH"**
   - Click **"Install Now"**
   - Click **"Yes"** if Windows asks for permission
   - Wait 5 minutes
   - Click **"Close"**

5. **Verify installation:**
   - Press **Windows key**
   - Type: **cmd**
   - Press **Enter** (opens Command Prompt)
   - Type: **python --version**
   - Press **Enter**
   - You should see: Python 3.11.x

**If you see "python is not recognized":**
- You forgot to check "Add python.exe to PATH"
- Uninstall Python (Control Panel → Programs)
- Reinstall and CHECK THE BOX this time

**Success indicator:** "python --version" shows Python 3.11.x or higher.

---

#### FOR LINUX USERS (Ubuntu/Debian):

**Time: 10 minutes**

1. Open Terminal (Ctrl + Alt + T)

2. Update package list:
   **sudo apt-get update**
   - Press **Enter**
   - Enter your password

3. Install Python 3.11:
   **sudo apt-get install python3.11 python3.11-venv python3-pip**
   - Press **Enter**
   - Type **y** when asked
   - Wait 5 minutes

4. Verify installation:
   **python3.11 --version**
   - Press **Enter**
   - You should see: Python 3.11.x

**Success indicator:** "python3.11 --version" or "python3 --version" shows 3.11.x or higher.

---

## PHASE 3: CLONE THE PROJECT

### Step 3.1: Choose Project Location

**Time: 2 minutes**

**Decide where to put the project on your computer.**

**Recommended locations:**
- Mac: **/Users/YourName/Projects/**
- Windows: **C:\Users\YourName\Projects\**
- Linux: **/home/YourName/Projects/**

**Create the Projects folder:**

1. Open Terminal (Mac/Linux) or Git Bash (Windows)

2. Type: **mkdir Projects**
   - Press **Enter**
   - This creates a "Projects" folder in your home directory

3. Move into the folder:
   **cd Projects**
   - Press **Enter**

4. Verify you're in the right place:
   **pwd** (Mac/Linux) or **cd** (Windows)
   - Press **Enter**
   - You should see a path ending in "/Projects" or "\Projects"

**Success indicator:** You're in the Projects folder.

---

### Step 3.2: Clone the Repository

**Time: 5 minutes**

**This downloads all the project files to your computer.**

1. Make sure you're in the Projects folder
   - Type: **pwd** (Mac/Linux) or **cd** (Windows)
   - Should show: /Users/YourName/Projects or C:\Users\YourName\Projects

2. Type this command exactly:
   **git clone https://github.com/camberofran5-afk/ANTIGRAVITY.git**
   - Press **Enter**

3. **You'll be asked for credentials:**
   - Username: Type your GitHub username
   - Press **Enter**
   - Password: **DO NOT type your GitHub password!**
   - Instead, paste your Personal Access Token (starts with ghp_)
   - Press **Enter**

**Note:** When you paste the token, you won't see anything appear - this is normal for security. Just paste and press Enter.

4. **Wait for cloning:**
   - You'll see: "Cloning into 'ANTIGRAVITY'..."
   - Progress will show: "Receiving objects: 100%"
   - This takes 1-2 minutes

5. **Verify the clone:**
   - Type: **ls** (Mac/Linux) or **dir** (Windows)
   - Press **Enter**
   - You should see a folder called "ANTIGRAVITY"

**Success indicator:** You see "ANTIGRAVITY" folder listed.

---

### Step 3.3: Navigate into the Project

**Time: 1 minute**

1. Type: **cd ANTIGRAVITY**
   - Press **Enter**

2. List the files:
   **ls** (Mac/Linux) or **dir** (Windows)
   - Press **Enter**

3. **You should see these files:**
   - README.md
   - agents.md
   - START_HERE.md
   - QUICK_REFERENCE.md
   - requirements.txt
   - .env.example
   - onboard.sh
   - Folders: docs, tools, tests, etc.

**Success indicator:** You see README.md, agents.md, and other project files.

---

## PHASE 4: SET UP PYTHON ENVIRONMENT

### Step 4.1: Create Virtual Environment

**Time: 2 minutes**

**What is a virtual environment?** An isolated Python installation just for this project.

1. Make sure you're in the ANTIGRAVITY folder
   - Type: **pwd** (Mac/Linux) or **cd** (Windows)
   - Should end with "/ANTIGRAVITY" or "\ANTIGRAVITY"

2. Create the virtual environment:
   
   **Mac/Linux:**
   **python3 -m venv venv**
   
   **Windows:**
   **python -m venv venv**
   
   - Press **Enter**
   - Wait 30-60 seconds
   - You won't see much output - this is normal

3. Verify creation:
   **ls** (Mac/Linux) or **dir** (Windows)
   - Press **Enter**
   - You should now see a new folder called "venv"

**Success indicator:** A "venv" folder appears in your project directory.

---

### Step 4.2: Activate Virtual Environment

**Time: 1 minute**

**This "turns on" the virtual environment.**

---

#### FOR MAC/LINUX:

1. Type exactly:
   **source venv/bin/activate**
   - Press **Enter**

2. **Success indicator:**
   - Your command prompt changes
   - You'll see **(venv)** at the beginning of your prompt
   - Example: **(venv) YourName@Computer ANTIGRAVITY %**

**If you see an error:**
- Make sure you're in the ANTIGRAVITY folder
- Check that the venv folder exists
- Try: **ls venv/bin/** to verify the activate script exists

---

#### FOR WINDOWS:

1. Type exactly:
   **venv\Scripts\activate**
   - Press **Enter**

2. **If you see an error about execution policy:**
   - Type: **Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser**
   - Press **Enter**
   - Type: **Y**
   - Press **Enter**
   - Try activating again: **venv\Scripts\activate**

3. **Success indicator:**
   - Your command prompt changes
   - You'll see **(venv)** at the beginning
   - Example: **(venv) C:\Users\YourName\Projects\ANTIGRAVITY>**

---

**IMPORTANT:** You must activate the virtual environment every time you open a new terminal window to work on this project.

---

### Step 4.3: Install Project Dependencies

**Time: 5 minutes**

**This installs all the Python packages the project needs.**

1. **Verify your virtual environment is activated:**
   - Look for **(venv)** at the start of your prompt
   - If you don't see it, go back to Step 4.2

2. Type this command:
   **pip install -r requirements.txt**
   - Press **Enter**

3. **What you'll see:**
   - Lots of text scrolling by
   - "Collecting [package name]..."
   - "Downloading [package name]..."
   - "Installing collected packages..."
   - This takes 3-5 minutes

4. **When it's done, you'll see:**
   - "Successfully installed [long list of packages]"
   - Your prompt returns

**If you see errors:**
- Make sure (venv) is showing in your prompt
- Make sure you're in the ANTIGRAVITY folder
- Try: **pip install --upgrade pip** first, then try again

**Success indicator:** You see "Successfully installed" with a list of packages.

---

### Step 4.4: Verify Installation

**Time: 2 minutes**

1. Check Python version:
   **python --version**
   - Press **Enter**
   - Should show: Python 3.11.x or higher

2. List installed packages:
   **pip list**
   - Press **Enter**
   - You should see a long list

3. **Verify these key packages are installed:**
   - Look for: **supabase**
   - Look for: **google-generativeai**
   - Look for: **openai**
   - Look for: **structlog**
   - Look for: **pytest**
   - Look for: **pydantic**

**Success indicator:** All key packages appear in the pip list.

---

## PHASE 5: CONFIGURE ENVIRONMENT

### Step 5.1: Get Credentials from Project Lead

**Time: 5 minutes (waiting for project lead)**

**Send this message to the project lead:**

"Hi! I've successfully cloned the ANTIGRAVITY repository and set up my Python environment.

I now need the following credentials to complete setup:

1. Supabase URL
2. Supabase Anon Key
3. Gemini API Key (if we're using it)
4. OpenAI/Perplexity API Key (if we're using it)

Please send these securely (not via public chat).

Thanks!"

**Wait for the project lead to send you:**
- Supabase URL (looks like: https://xxxxxxxxxxxxx.supabase.co)
- Supabase Anon Key (long string of random characters)
- Gemini API Key (starts with: AIza...)
- OpenAI API Key (starts with: sk-...)

**Save these in your antigravity-credentials.txt file.**

---

### Step 5.2: Create .env File

**Time: 3 minutes**

**The .env file stores your secret credentials.**

1. Make sure you're in the ANTIGRAVITY folder
2. Make sure your virtual environment is activated (see (venv) in prompt)

3. **Create the .env file:**

   **Mac/Linux:**
   **cp .env.example .env**
   
   **Windows:**
   **copy .env.example .env**
   
   - Press **Enter**

4. Verify the file was created:
   **ls -la** (Mac/Linux) or **dir** (Windows)
   - You should see both .env.example and .env

**Success indicator:** Both .env.example and .env files exist.

---

### Step 5.3: Edit .env File

**Time: 5 minutes**

**Fill in your actual credentials.**

1. **Open the .env file in a text editor:**

   **Mac:**
   **nano .env**
   - Press **Enter**
   
   **Windows:**
   **notepad .env**
   - Press **Enter**
   
   **Or use any code editor like VS Code, Sublime Text, etc.**

2. **You'll see placeholders like this:**
   - NEXT_PUBLIC_SUPABASE_URL=YOUR_SUPABASE_URL_HERE
   - NEXT_PUBLIC_SUPABASE_ANON_KEY=YOUR_SUPABASE_ANON_KEY_HERE
   - GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
   - OPENAI_API_KEY=YOUR_OPENAI_API_KEY_HERE

3. **Replace each placeholder with your actual credentials:**
   
   **Before:**
   NEXT_PUBLIC_SUPABASE_URL=YOUR_SUPABASE_URL_HERE
   
   **After:**
   NEXT_PUBLIC_SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
   
   **Important rules:**
   - No spaces around the = sign
   - No quotation marks
   - No extra spaces at the end
   - Keep each credential on its own line

4. **Save the file:**
   
   **If using nano (Mac):**
   - Press **Ctrl + O** (to save)
   - Press **Enter** (to confirm)
   - Press **Ctrl + X** (to exit)
   
   **If using notepad (Windows):**
   - Click **File → Save**
   - Close notepad

5. **Verify your .env file:**
   **cat .env** (Mac/Linux) or **type .env** (Windows)
   - Press **Enter**
   - You should see your actual credentials (not the placeholders)

**CRITICAL:** Never share this .env file or commit it to Git!

**Success indicator:** .env file contains your actual credentials with no placeholders.

---

## PHASE 6: TEST YOUR SETUP

### Step 6.1: Run Onboarding Script

**Time: 2 minutes**

**This script verifies everything is working.**

1. Make sure you're in the ANTIGRAVITY folder
2. Make sure (venv) is showing in your prompt

3. **Make the script executable (Mac/Linux only):**
   **chmod +x onboard.sh**
   - Press **Enter**

4. **Run the script:**
   
   **Mac/Linux:**
   **./onboard.sh**
   
   **Windows:**
   **bash onboard.sh**
   
   - Press **Enter**

5. **What you should see:**
   - "🚀 Antigravity Workspace Onboarding"
   - Current directory path
   - "Activating virtual environment..."
   - "✅ Python: Python 3.11.x"
   - "Pulling latest changes..."
   - "Already up to date" or list of updates
   - Preview of agents.md
   - Recent git commits
   - "✅ Onboarding complete! Ready to work."

**If you see errors:**
- Make sure virtual environment is activated
- Make sure you're in the ANTIGRAVITY folder
- Check that all previous steps completed successfully

**Success indicator:** Script runs without errors and shows "Ready to work."

---

### Step 6.2: Test Supabase Connection

**Time: 2 minutes**

**Verify you can connect to the database.**

1. Make sure (venv) is showing
2. Type: **python tools/test_supabase_integration.py**
3. Press **Enter**

4. **What you should see:**
   - "🧪 SUPABASE INTEGRATION TEST"
   - "Test 1: Client Initialization"
   - "✅ Supabase client initialized successfully"
   - "Test 2: Database Connection"
   - "✅ Database connection working"

**If you see errors:**
- Check your .env file has correct Supabase URL and key
- Make sure there are no spaces or quotation marks
- Verify the credentials with project lead

**Success indicator:** Both tests show ✅ checkmarks.

---

### Step 6.3: Test LLM Integration (Optional)

**Time: 2 minutes**

**Verify AI integrations work (if you have API keys).**

1. Type: **python tools/test_llm_integration.py**
2. Press **Enter**

3. **What you should see:**
   - "🧪 LLM INTEGRATION TEST"
   - "Test 1: Gemini Client Initialization"
   - "✅ Gemini client initialized successfully"
   - "Test 2: Perplexity Client Initialization"
   - "✅ Perplexity client initialized successfully"

**If you don't have API keys:**
- You'll see warnings - this is okay
- You can still use the project
- Get API keys later if needed

**Success indicator:** Tests pass or show expected warnings.

---

## PHASE 7: OPEN ANTIGRAVITY

### Step 7.1: Launch Antigravity Application

**Time: 2 minutes**

1. Open the Antigravity application on your computer
2. If prompted, set the workspace to your ANTIGRAVITY folder
3. Navigate to: **/Users/YourName/Projects/ANTIGRAVITY** (or your path)
4. Click to open/set the workspace

**Success indicator:** Antigravity recognizes the ANTIGRAVITY folder as the workspace.

---

### Step 7.2: Load Project Context

**Time: 3 minutes**

**Use this exact prompt in Antigravity:**

Copy and paste this into the Antigravity chat:

---

I'm starting a new session on the Antigravity project.

Context needed:
1. Read agents.md to understand the system architecture
2. Check task.md for current work status
3. Review recent git commits (last 10)
4. Check logs/app.log for recent activity

My goal for this session: Get familiar with the project and understand the current state

Please help me:
- Understand what's been done recently
- Identify any blockers or issues
- Suggest next steps based on the current state

---

**What Antigravity will do:**
- Read the system constitution (agents.md)
- Show you the 4-Layer Hierarchy architecture
- Display recent git commits
- Explain the current project state
- Suggest what you can work on

**Success indicator:** Antigravity responds with project overview and suggestions.

---

### Step 7.3: Choose Your Agent Role

**Time: 2 minutes**

**Based on Antigravity's response and team needs, choose your role:**

**Agent Roles:**
- **Agent-Database:** Database schemas, data models, Supabase (L1-L3)
- **Agent-AI:** AI features, LLM integration, prompts (L2-L3)
- **Agent-API:** API endpoints, integrations, webhooks (L4)
- **Agent-QA:** Testing, documentation, quality assurance

**Ask the project lead:** "Which agent role should I focus on?"

**Success indicator:** You know which agent role you'll be working as.

---

## PHASE 8: YOUR FIRST TASK

### Step 8.1: Check Available Tasks

**Time: 2 minutes**

1. In your terminal (with venv activated)
2. Type: **cat task.md**
3. Press **Enter**

**If task.md doesn't exist:**
- That's okay! The project lead will create it
- Or you can ask Antigravity: "What should I work on first?"

**If task.md exists, look for:**
- [ ] = Available tasks (you can claim these)
- [/] = In progress (someone is working on it)
- [x] = Complete (done)

**Success indicator:** You see available tasks or know to ask for guidance.

---

### Step 8.2: Claim Your First Task

**Time: 3 minutes**

1. Choose an available task that matches your agent role
2. Open task.md in a text editor
3. Change [ ] to [/] for your task
4. Add your name: [/] YourName: Task description
5. Save the file

6. **Commit this change:**
   - Type: **git add task.md**
   - Press **Enter**
   - Type: **git commit -m "[YourRole] Claiming task: Task description"**
   - Press **Enter**
   - Type: **git push origin dev**
   - Press **Enter**
   - Enter your GitHub username and token if prompted

**Success indicator:** Your task is marked [/] and pushed to GitHub.

---

### Step 8.3: Start Working

**Time: Ongoing**

1. Use Antigravity to help you complete the task
2. Refer to START_HERE.md for prompting patterns
3. Follow the 4-Layer Hierarchy (L1 → L2 → L3 → L4)
4. Commit your work frequently
5. When done, mark the task as [x] in task.md

**Success indicator:** You're actively working on your first task!

---

## ✅ INSTALLATION COMPLETE CHECKLIST

**Verify you've completed everything:**

- [ ] Created GitHub account
- [ ] Accepted invitation to ANTIGRAVITY repository
- [ ] Created Personal Access Token
- [ ] Installed Git
- [ ] Configured Git with name and email
- [ ] Installed Python 3.11+
- [ ] Created Projects folder
- [ ] Cloned ANTIGRAVITY repository
- [ ] Navigated into ANTIGRAVITY folder
- [ ] Created virtual environment (venv folder exists)
- [ ] Activated virtual environment (see (venv) in prompt)
- [ ] Installed all packages (pip install -r requirements.txt)
- [ ] Verified key packages installed (pip list)
- [ ] Received credentials from project lead
- [ ] Created .env file
- [ ] Filled in .env with actual credentials
- [ ] Ran onboard.sh successfully
- [ ] Tested Supabase connection (✅)
- [ ] Tested LLM integration (✅ or expected warnings)
- [ ] Opened Antigravity application
- [ ] Set workspace to ANTIGRAVITY folder
- [ ] Loaded project context with initial prompt
- [ ] Chose agent role
- [ ] Read START_HERE.md
- [ ] Read agents.md
- [ ] Checked task.md or asked for first task
- [ ] Ready to start working!

**If all checked: YOU'RE READY! 🎉**

---

## 🆘 TROUBLESHOOTING

### "Git clone fails with authentication error"
**Solution:** 
- Make sure you're using your Personal Access Token, not your GitHub password
- Verify the token has "repo" permissions
- Try creating a new token

### "Virtual environment won't activate"
**Solution:**
- Mac/Linux: Make sure you typed: source venv/bin/activate
- Windows: Try: venv\Scripts\activate.bat
- Verify venv folder exists: ls venv (Mac/Linux) or dir venv (Windows)

### "pip install fails"
**Solution:**
- Make sure (venv) is showing in your prompt
- Try: pip install --upgrade pip
- Then: pip install -r requirements.txt again

### "Supabase test fails"
**Solution:**
- Open .env file and verify credentials
- Make sure there are no spaces around = signs
- Make sure there are no quotation marks
- Verify credentials with project lead

### "I don't see (venv) in my prompt"
**Solution:**
- You need to activate the virtual environment
- Mac/Linux: source venv/bin/activate
- Windows: venv\Scripts\activate
- Do this every time you open a new terminal

### "Git push is rejected"
**Solution:**
- Type: git pull origin dev
- Resolve any conflicts
- Type: git push origin dev again

---

## 📞 GETTING HELP

**If you're stuck:**

1. **Check this guide again** - read the specific step carefully
2. **Check the error message** - it often tells you what's wrong
3. **Ask the project lead** - they can help troubleshoot
4. **Use Antigravity** - ask it for help with specific errors

**When asking for help, provide:**
- What step you're on
- What command you typed
- What error message you see
- Your operating system (Mac/Windows/Linux)

---

## 🎉 CONGRATULATIONS!

You've successfully installed and set up the Antigravity project!

**You can now:**
- ✅ Clone and update the repository
- ✅ Work in an isolated Python environment
- ✅ Connect to Supabase database
- ✅ Use AI integrations
- ✅ Collaborate with the team via Git
- ✅ Start building features!

**Next steps:**
1. Read START_HERE.md for daily workflow
2. Read agents.md for system architecture
3. Check task.md for available work
4. Start contributing!

**Welcome to the team! 🚀**
