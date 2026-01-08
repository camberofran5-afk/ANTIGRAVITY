# L1 Configuration Layer
# Zero dependencies - Pure configuration and constants

from .supabase_client import get_supabase_client, get_supabase_url
from .llm_client import get_gemini_model, get_perplexity_client, get_openai_client
from .logging_config import get_logger, log_function_call
from .system_config import (
    Environment,
    LogLevel,
    MAX_RETRY_ATTEMPTS,
    RETRY_BACKOFF_SECONDS,
    REQUEST_TIMEOUT_SECONDS,
    DEFAULT_PAGE_SIZE,
    MAX_PAGE_SIZE,
)

__all__ = [
    "get_supabase_client",
    "get_supabase_url",
    "get_gemini_model",
    "get_perplexity_client",
    "get_openai_client",
    "get_logger",
    "log_function_call",
    "Environment",
    "LogLevel",
    "MAX_RETRY_ATTEMPTS",
    "RETRY_BACKOFF_SECONDS",
    "REQUEST_TIMEOUT_SECONDS",
    "DEFAULT_PAGE_SIZE",
    "MAX_PAGE_SIZE",
]
