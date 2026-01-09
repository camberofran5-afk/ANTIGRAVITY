# GitHub Setup Instructions

## Authentication Failed - Need Personal Access Token

The push failed because GitHub requires authentication. Here's how to fix it:

### Step 1: Create GitHub Personal Access Token

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name: "Antigravity Project"
4. Select scopes:
   - ✅ `repo` (Full control of private repositories)
5. Click "Generate token"
6. **COPY THE TOKEN** (you'll only see it once!)

### Step 2: Configure Git with Token

```bash
# Use token as password when pushing
git push -u origin main

# When prompted:
# Username: camberofran5-afk
# Password: <paste your token here>
```

### Step 3: (Optional) Save Credentials

To avoid entering token every time:

```bash
# macOS - use keychain
git config --global credential.helper osxkeychain

# Then push again, enter token once, it will be saved
git push -u origin main
```

---

## Alternative: Use SSH Instead

### Step 1: Generate SSH Key

```bash
ssh-keygen -t ed25519 -C "camberofran5@gmail.com"
# Press Enter to accept default location
# Press Enter twice for no passphrase
```

### Step 2: Add SSH Key to GitHub

```bash
# Copy public key
cat ~/.ssh/id_ed25519.pub
# Copy the output
```

1. Go to: https://github.com/settings/keys
2. Click "New SSH key"
3. Paste the key
4. Click "Add SSH key"

### Step 3: Change Remote to SSH

```bash
git remote set-url origin git@github.com:camberofran5-afk/ANTIGRAVITY.git
git push -u origin main
```

---

## Quick Fix (Recommended)

**Use Personal Access Token method - it's faster!**

1. Create token at: https://github.com/settings/tokens
2. Run: `git push -u origin main`
3. Enter username: `camberofran5-afk`
4. Enter password: `<your token>`

Done! 🚀
