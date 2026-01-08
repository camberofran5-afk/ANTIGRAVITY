"""
L1 Configuration: System Constants and Types
Centralized configuration for the entire system.
Zero dependencies on other layers.
"""

from enum import Enum
from typing import TypedDict


class Environment(str, Enum):
    """Application environment types."""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class LogLevel(str, Enum):
    """Logging levels."""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class DatabaseConfig(TypedDict):
    """Database configuration structure."""
    url: str
    anon_key: str
    service_role_key: str


# System-wide constants
MAX_RETRY_ATTEMPTS = 3
RETRY_BACKOFF_SECONDS = 2
REQUEST_TIMEOUT_SECONDS = 30
MAX_QUERY_RESULTS = 1000

# Data quality thresholds
MIN_DATA_QUALITY_SCORE = 0.7
MAX_CYCLOMATIC_COMPLEXITY = 10
MAX_FUNCTION_LENGTH = 50

# Pagination
DEFAULT_PAGE_SIZE = 50
MAX_PAGE_SIZE = 100
