"""
L1 Configuration: Supabase Client Initialization
This module provides the centralized Supabase client for the entire system.
Following the 4-Layer Hierarchy: L1 = Configuration (Zero dependencies)
"""

import os
from typing import Optional
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()


class SupabaseConfig:
    """
    Centralized Supabase configuration.
    
    This class follows the Single Responsibility Principle (SOLID):
    - Only responsible for Supabase client initialization
    - No business logic
    - No data validation (that's L2)
    """
    
    def __init__(self):
        """Initialize Supabase configuration from environment variables."""
        self.url: str = os.getenv("NEXT_PUBLIC_SUPABASE_URL", "")
        self.anon_key: str = os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY", "")
        self.service_role_key: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
        
        if not self.url or not self.anon_key:
            raise ValueError(
                "Missing required Supabase credentials. "
                "Please set NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_ANON_KEY in .env"
            )
    
    def get_client(self, use_service_role: bool = False) -> Client:
        """
        Get a Supabase client instance.
        
        Args:
            use_service_role: If True, use service_role key (bypasses RLS).
                            If False, use anon key (respects RLS).
        
        Returns:
            Supabase Client instance
            
        Raises:
            ValueError: If service_role key is requested but not configured
        """
        if use_service_role:
            if not self.service_role_key or self.service_role_key == "[key]":
                raise ValueError(
                    "Service role key not configured. "
                    "Set SUPABASE_SERVICE_ROLE_KEY in .env for admin access."
                )
            return create_client(self.url, self.service_role_key)
        
        return create_client(self.url, self.anon_key)


# Singleton instance for easy import
_config: Optional[SupabaseConfig] = None


def get_supabase_client(use_service_role: bool = False) -> Client:
    """
    Get the global Supabase client instance.
    
    This is the primary way to access Supabase throughout the application.
    
    Args:
        use_service_role: If True, use service_role key (admin access)
    
    Returns:
        Supabase Client instance
        
    Example:
        >>> from tools.L1_config.supabase_client import get_supabase_client
        >>> supabase = get_supabase_client()
        >>> response = supabase.table('users').select("*").execute()
    """
    global _config
    
    if _config is None:
        _config = SupabaseConfig()
    
    return _config.get_client(use_service_role=use_service_role)


def get_supabase_url() -> str:
    """Get the Supabase project URL."""
    global _config
    
    if _config is None:
        _config = SupabaseConfig()
    
    return _config.url


if __name__ == "__main__":
    # Test the configuration
    print("🔍 Testing Supabase Configuration...")
    print()
    
    try:
        config = SupabaseConfig()
        print(f"✅ Configuration loaded successfully")
        print(f"   URL: {config.url}")
        print(f"   Anon Key: {config.anon_key[:20]}... ({len(config.anon_key)} chars)")
        print()
        
        # Test client creation
        client = get_supabase_client()
        print(f"✅ Supabase client created successfully")
        print(f"   Client type: {type(client).__name__}")
        print()
        
        print("🎯 Ready to use Supabase!")
        print()
        print("Usage:")
        print("  from tools.L1_config.supabase_client import get_supabase_client")
        print("  supabase = get_supabase_client()")
        print("  response = supabase.table('your_table').select('*').execute()")
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        exit(1)
