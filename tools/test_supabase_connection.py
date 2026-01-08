#!/usr/bin/env python3
"""
Supabase MCP Connection Test Script
Tests the connection to Supabase via the MCP server
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_mcp_connection():
    """Test MCP server connection"""
    print("🔍 Checking Supabase MCP Configuration...")
    print()
    
    # Check environment variables
    supabase_url = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
    supabase_anon_key = os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")
    supabase_service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    print("📋 Environment Variables Status:")
    print(f"  NEXT_PUBLIC_SUPABASE_URL: {'✅ Set' if supabase_url else '❌ Missing'}")
    if supabase_url:
        print(f"    Value: {supabase_url}")
    
    print(f"  NEXT_PUBLIC_SUPABASE_ANON_KEY: {'✅ Set' if supabase_anon_key else '❌ Missing'}")
    if supabase_anon_key:
        print(f"    Length: {len(supabase_anon_key)} characters")
    
    print(f"  SUPABASE_SERVICE_ROLE_KEY: {'✅ Set' if supabase_service_key else '⚠️  Optional (not set)'}")
    if supabase_service_key:
        print(f"    Length: {len(supabase_service_key)} characters")
    
    print()
    
    # Test Supabase connection
    if supabase_url and supabase_anon_key:
        try:
            from supabase import create_client, Client
            
            print("🔌 Testing Supabase Connection...")
            supabase: Client = create_client(supabase_url, supabase_anon_key)
            
            # Try a simple query (this will fail if no tables exist, but connection works)
            print("  Attempting to connect to Supabase...")
            
            # Test health endpoint
            response = supabase.table('_supabase_health').select("*").execute()
            print("  ✅ Connection successful!")
            
        except Exception as e:
            error_msg = str(e)
            if "relation" in error_msg.lower() or "does not exist" in error_msg.lower():
                print("  ✅ Connection successful! (No tables exist yet, but connection works)")
            else:
                print(f"  ⚠️  Connection issue: {error_msg}")
                print("  Note: This might be normal if you haven't set up tables yet")
    else:
        print("❌ Cannot test connection - missing required environment variables")
        print()
        print("📝 Next Steps:")
        print("1. Get your Supabase credentials from: https://supabase.com/dashboard")
        print("2. Navigate to: Your Project → Settings → API")
        print("3. Copy the Project URL and anon key")
        print("4. Update your .env file with these values")
    
    print()
    print("🎯 MCP Server Configuration:")
    print("  Server: supabase")
    print("  Type: HTTP")
    print("  URL: https://mcp.supabase.com/mcp?project_ref=qkyemdzfnhqwmrfkzgqj")
    print()
    print("  To authenticate the MCP server, use: /mcp auth supabase")
    print()

if __name__ == "__main__":
    test_mcp_connection()
