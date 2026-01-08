# Supabase MCP Setup Instructions

## ✅ What You've Done So Far

1. **Added Supabase MCP Server:**
   ```bash
   gemini mcp add -t http supabase https://mcp.supabase.com/mcp?project_ref=qkyemdzfnhqwmrfkzgqj
   ```
   
2. **MCP Configuration:**
   ```json
   {
     "mcpServers": {
       "supabase": {
         "httpUrl": "https://mcp.supabase.com/mcp?project_ref=qkyemdzfnhqwmrfkzgqj"
       }
     }
   }
   ```

## 🔑 Next Steps: Complete the Setup

### Step 1: Authenticate the MCP Server

Run this command in Antigravity:
```bash
/mcp auth supabase
```

This will prompt you to authenticate with your Supabase credentials.

### Step 2: Update Your `.env` File

You need to manually edit `/Users/franciscocambero/Anitgravity/.env` with your Supabase credentials.

**Open the file and update these lines:**

```bash
# SUPABASE CONFIGURATION
NEXT_PUBLIC_SUPABASE_URL="https://qkyemdzfnhqwmrfkzgqj.supabase.co"
NEXT_PUBLIC_SUPABASE_ANON_KEY="[paste your anon key here]"
SUPABASE_SERVICE_ROLE_KEY="[paste your service role key here]"
```

**Where to find these keys:**
1. Go to https://supabase.com/dashboard
2. Select your project (qkyemdzfnhqwmrfkzgqj)
3. Navigate to **Settings** → **API**
4. Copy:
   - **Project URL** (should be `https://qkyemdzfnhqwmrfkzgqj.supabase.co`)
   - **anon public** key
   - **service_role** key (click "Reveal")

### Step 3: Test the Connection

After updating your `.env` file, run:

```bash
cd /Users/franciscocambero/Anitgravity
source venv/bin/activate
python tools/test_supabase_connection.py
```

This will verify:
- ✅ Environment variables are set correctly
- ✅ Supabase connection works
- ✅ MCP server is configured

### Step 4: Verify MCP Resources

Once authenticated, you should be able to list Supabase resources:

```bash
# In Antigravity, I can use:
list_resources(ServerName="supabase")
```

This will show available tables, functions, and other database resources.

---

## 🔧 Troubleshooting

### MCP Server Not Showing Up?
- Make sure you ran `/mcp auth supabase`
- Restart Antigravity IDE after adding the MCP server
- Check MCP server status with `/mcp list`

### Connection Errors?
- Verify your `.env` file has the correct keys
- Check that your Supabase project is active
- Ensure your API keys haven't been revoked

### Need to Re-authenticate?
```bash
/mcp auth supabase --force
```

---

## 📚 What's Next?

Once the MCP server is authenticated and working, you'll be able to:

1. **Query your database** directly through MCP
2. **Create tables** and manage schema
3. **Run SQL queries** via the agent
4. **Build the L1 Configuration layer** with database models
5. **Start the Discovery Protocol** to define your system

---

**Current Status:**
- ✅ MCP server added
- ⏳ Waiting for authentication
- ⏳ Waiting for `.env` configuration
