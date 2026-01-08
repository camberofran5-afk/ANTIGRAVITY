"""
L1 Configuration: Logging Configuration
Centralized logging setup with structured logging.
Following the 4-Layer Hierarchy: L1 = Configuration (Zero dependencies)
"""

import os
import sys
import logging
from pathlib import Path
from typing import Any, Dict
from dotenv import load_dotenv
import structlog

# Load environment variables
load_dotenv()


class LoggingConfig:
    """
    Centralized logging configuration.
    
    Uses structlog for structured JSON logging with:
    - Timestamps
    - Log levels
    - Context information
    - File and console output
    """
    
    def __init__(self):
        """Initialize logging configuration."""
        self.log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        self.log_dir = Path("logs")
        self.log_file = self.log_dir / "app.log"
        
        # Create logs directory if it doesn't exist
        self.log_dir.mkdir(exist_ok=True)
        
        # Configure structlog
        self._configure_structlog()
    
    def _configure_structlog(self):
        """Configure structlog with processors and formatters."""
        
        # Shared processors for both console and file output
        shared_processors = [
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
        ]
        
        # Configure structlog
        structlog.configure(
            processors=shared_processors + [
                structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )
        
        # Configure standard library logging
        formatter = structlog.stdlib.ProcessorFormatter(
            foreign_pre_chain=shared_processors,
            processors=[
                structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                structlog.processors.JSONRenderer(),
            ],
        )
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(self.log_level)
        
        # File handler
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(self.log_level)
        
        # Root logger configuration
        root_logger = logging.getLogger()
        root_logger.addHandler(console_handler)
        root_logger.addHandler(file_handler)
        root_logger.setLevel(self.log_level)


# Initialize logging configuration
_logging_config: LoggingConfig = LoggingConfig()


def get_logger(name: str = __name__) -> structlog.stdlib.BoundLogger:
    """
    Get a structured logger instance.
    
    Args:
        name: Logger name (usually __name__)
    
    Returns:
        Structured logger instance
        
    Example:
        >>> from tools.L1_config.logging_config import get_logger
        >>> logger = get_logger(__name__)
        >>> logger.info("user_login", user_id=123, ip_address="192.168.1.1")
        >>> logger.error("database_error", error="Connection timeout", table="users")
    """
    return structlog.get_logger(name)


def log_function_call(func):
    """
    Decorator to automatically log function calls with parameters and results.
    
    Example:
        >>> @log_function_call
        >>> def process_data(user_id: int, data: dict):
        >>>     return {"status": "success"}
    """
    logger = get_logger(func.__module__)
    
    def wrapper(*args, **kwargs):
        logger.info(
            "function_called",
            function=func.__name__,
            args=args,
            kwargs=kwargs
        )
        
        try:
            result = func(*args, **kwargs)
            logger.info(
                "function_completed",
                function=func.__name__,
                result=result
            )
            return result
        except Exception as e:
            logger.error(
                "function_failed",
                function=func.__name__,
                error=str(e),
                error_type=type(e).__name__
            )
            raise
    
    return wrapper


if __name__ == "__main__":
    # Test the logging configuration
    print("🔍 Testing Logging Configuration...")
    print()
    
    logger = get_logger(__name__)
    
    print("✅ Logging configured successfully")
    print(f"   Log level: {_logging_config.log_level}")
    print(f"   Log file: {_logging_config.log_file}")
    print()
    
    # Test different log levels
    logger.debug("debug_message", detail="This is a debug message")
    logger.info("info_message", detail="This is an info message")
    logger.warning("warning_message", detail="This is a warning")
    logger.error("error_message", detail="This is an error")
    
    print()
    print("🎯 Structured logging ready!")
    print()
    print("Usage:")
    print("  from tools.L1_config.logging_config import get_logger")
    print("  logger = get_logger(__name__)")
    print("  logger.info('event_name', user_id=123, action='login')")
    print()
    print(f"Logs are written to: {_logging_config.log_file}")
