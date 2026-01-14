"""
ERP Ganadero - Supabase Client (L1 Configuration)

Supabase connection and authentication.
"""

import os
from typing import Optional
from dotenv import load_dotenv
import structlog

logger = structlog.get_logger()

# Load environment variables
load_dotenv()

# Check if we should use mock mode
USE_MOCK = os.getenv("USE_MOCK_DB", "false").lower() == "true"

if USE_MOCK:
    from .mock_supabase import get_mock_supabase
    logger.info("using_mock_supabase")
else:
    from supabase import create_client, Client


class SupabaseClient:
    """Supabase client singleton"""
    
    _instance: Optional[any] = None
    
    @classmethod
    def get_client(cls):
        """Get Supabase client instance"""
        if cls._instance is None:
            if USE_MOCK:
                cls._instance = get_mock_supabase()
                logger.info("mock_supabase_initialized")
            else:
                url = os.getenv("SUPABASE_URL")
                key = os.getenv("SUPABASE_KEY")
                
                if not url or not key:
                    raise ValueError(
                        "SUPABASE_URL and SUPABASE_KEY must be set in environment"
                    )
                
                cls._instance = create_client(url, key)
                logger.info("supabase_client_initialized", url=url)
        
        return cls._instance
    
    @classmethod
    def reset(cls):
        """Reset client (for testing)"""
        cls._instance = None


def get_supabase():
    """Get Supabase client"""
    return SupabaseClient.get_client()
