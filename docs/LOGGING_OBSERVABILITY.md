# Logging & Observability Guide

## Overview
Comprehensive structured logging system using `structlog` for JSON-formatted logs with timestamps, log levels, and contextual information.

---

## Architecture

### L1: Configuration Layer (`tools/L1_config/`)
**Purpose:** Centralized logging configuration

#### Files Created:
- `logging_config.py` - Structured logging setup
- Updated `__init__.py` - Public API exports

#### Usage:
```python
from tools.L1_config import get_logger

logger = get_logger(__name__)
logger.info("user_login", user_id=123, ip_address="192.168.1.1")
```

---

## Features

### ✅ Structured JSON Logging
All logs are output in JSON format for easy parsing:
```json
{
  "event": "user_login",
  "user_id": 123,
  "ip_address": "192.168.1.1",
  "level": "info",
  "logger": "myapp.auth",
  "timestamp": "2024-01-08T17:26:30.999574Z"
}
```

### ✅ Multiple Output Targets
- **Console**: Stdout for development
- **File**: `logs/app.log` for persistence

### ✅ Log Levels
- `DEBUG`: Detailed diagnostic information
- `INFO`: General informational messages
- `WARNING`: Warning messages
- `ERROR`: Error messages
- `CRITICAL`: Critical failures

### ✅ Context Information
- Timestamps (ISO format)
- Logger name (module path)
- Log level
- Stack traces (for errors)

---

## Usage Examples

### Basic Logging
```python
from tools.L1_config import get_logger

logger = get_logger(__name__)

# Info log
logger.info("operation_started", operation="data_sync", records=100)

# Warning log
logger.warning("rate_limit_approaching", current=95, limit=100)

# Error log
logger.error("database_error", error="Connection timeout", table="users")
```

### Logging with Context
```python
logger.info(
    "api_request",
    method="POST",
    endpoint="/api/users",
    user_id=123,
    duration_ms=45
)
```

### Function Call Logging (Decorator)
```python
from tools.L1_config import log_function_call

@log_function_call
def process_payment(user_id: int, amount: float):
    # Function logic here
    return {"status": "success", "transaction_id": "tx_123"}

# Automatically logs:
# - function_called (with args/kwargs)
# - function_completed (with result)
# - function_failed (if exception occurs)
```

### Error Logging with Exception
```python
try:
    result = risky_operation()
except Exception as e:
    logger.error(
        "operation_failed",
        operation="risky_operation",
        error=str(e),
        error_type=type(e).__name__
    )
    raise
```

---

## Integration with Existing Helpers

### Database Helpers
Logging is integrated into all database operations:
```python
from tools.L2_foundation import select_all

# This will automatically log the query
users = select_all('users', filters={'status': 'active'})
# Logs: database_query, table='users', filters={'status': 'active'}
```

### LLM Helpers
Logging is integrated into all LLM operations:
```python
from tools.L2_foundation import generate_with_gemini

# This will automatically log the LLM call
response = generate_with_gemini("Explain AI")
# Logs: llm_request, provider='gemini', prompt_length=11
# Logs: llm_response, provider='gemini', response_length=...
```

---

## Configuration

### Environment Variables
Set log level via `.env`:
```bash
LOG_LEVEL="DEBUG"  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
```

### Log File Location
Logs are written to: `logs/app.log`

The `logs/` directory is automatically created and excluded from git via `.gitignore`.

---

## Best Practices

### 1. Use Structured Fields
```python
# Good ✅
logger.info("user_action", user_id=123, action="login", success=True)

# Bad ❌
logger.info(f"User {user_id} logged in successfully")
```

### 2. Include Context
```python
logger.error(
    "payment_failed",
    user_id=user_id,
    amount=amount,
    payment_method="credit_card",
    error=str(e)
)
```

### 3. Use Appropriate Log Levels
- `DEBUG`: Verbose diagnostic info (disabled in production)
- `INFO`: Normal operations (user actions, API calls)
- `WARNING`: Unexpected but handled situations
- `ERROR`: Failures that need attention
- `CRITICAL`: System-level failures

### 4. Log at Key Points
- Function entry/exit (for critical functions)
- External API calls
- Database operations
- User actions
- Error conditions

---

## Viewing Logs

### Console Output
Logs appear in console during development:
```bash
./venv/bin/python your_script.py
```

### File Output
View log file:
```bash
tail -f logs/app.log
```

Parse JSON logs:
```bash
cat logs/app.log | jq '.'
```

Filter by log level:
```bash
cat logs/app.log | jq 'select(.level=="error")'
```

---

## Example: Complete Logging Flow

```python
from tools.L1_config import get_logger
from tools.L2_foundation import select_all, generate_with_gemini

logger = get_logger(__name__)

def process_user_request(user_id: int, query: str):
    logger.info("request_started", user_id=user_id, query=query)
    
    try:
        # Database operation (automatically logged)
        user = select_all('users', filters={'id': user_id}, limit=1)[0]
        logger.info("user_found", user_id=user_id, username=user['name'])
        
        # LLM operation (automatically logged)
        response = generate_with_gemini(query)
        logger.info("llm_response_generated", response_length=len(response))
        
        logger.info("request_completed", user_id=user_id, success=True)
        return response
        
    except Exception as e:
        logger.error(
            "request_failed",
            user_id=user_id,
            error=str(e),
            error_type=type(e).__name__
        )
        raise
```

---

**Status:** ✅ Logging & Observability Complete | 🎯 Ready for Production Monitoring
