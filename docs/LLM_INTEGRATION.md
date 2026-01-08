# LLM Integration Guide

## Overview
Complete LLM integration for Gemini and Perplexity following the 4-Layer Hierarchy architecture with SOLID principles, retry logic, and comprehensive error handling.

---

## Architecture

### L1: Configuration Layer (`tools/L1_config/`)
**Purpose:** Centralized LLM client initialization

#### Files Created:
- `llm_client.py` - Gemini and Perplexity client initialization
- Updated `__init__.py` - Public API exports

#### Usage:
```python
from tools.L1_config import get_gemini_model, get_perplexity_client

# Get Gemini model
model = get_gemini_model("gemini-1.5-flash")

# Get Perplexity client
client = get_perplexity_client()
```

### L2: Foundation Layer (`tools/L2_foundation/`)
**Purpose:** High-level LLM operations with error handling  
**Depends on:** L1 (Configuration)

#### Files Created:
- `llm_helpers.py` - LLM operations with retry logic
- Updated `__init__.py` - Public API exports

#### Available Functions:

**generate_with_gemini(prompt, model_name, temperature, max_tokens)**
```python
from tools.L2_foundation import generate_with_gemini

# Generate text
response = generate_with_gemini(
    "Explain quantum computing in simple terms",
    temperature=0.7
)
print(response)
```

**search_with_perplexity(query, model, temperature, max_tokens)**
```python
from tools.L2_foundation import search_with_perplexity

# Search with web access
response = search_with_perplexity(
    "Latest developments in AI 2024",
    model="llama-3.1-sonar-small-128k-chat"
)
print(response)
```

**chat_with_gemini(messages, model_name, temperature)**
```python
from tools.L2_foundation import chat_with_gemini

# Multi-turn conversation
messages = [
    {"role": "user", "content": "What is Python?"},
    {"role": "assistant", "content": "Python is a programming language."},
    {"role": "user", "content": "What are its main features?"}
]
response = chat_with_gemini(messages)
print(response)
```

**summarize_text(text, max_length, provider)**
```python
from tools.L2_foundation import summarize_text

# Summarize long text
long_article = "..." # Your long text here
summary = summarize_text(long_article, max_length=100, provider="gemini")
print(summary)
```

---

## Features

### ✅ Automatic Retry Logic
All LLM operations include exponential backoff retry:
- Max attempts: 3
- Backoff: 2^attempt seconds (2s, 4s, 8s)
- Catches API errors and rate limits

### ✅ Error Handling
Custom `LLMError` exception with context:
```python
from tools.L2_foundation import generate_with_gemini, LLMError

try:
    response = generate_with_gemini("Your prompt")
except LLMError as e:
    print(f"LLM operation failed: {e}")
```

### ✅ Type Hints
All functions include comprehensive type hints for IDE support

### ✅ Multiple Providers
- **Gemini**: Google's latest models (gemini-1.5-flash, gemini-1.5-pro)
- **Perplexity**: Web-connected LLMs (llama-3.1-sonar models)

---

## Available Models

### Gemini Models
- `gemini-1.5-flash` (default) - Fast, efficient
- `gemini-1.5-pro` - More capable, slower

### Perplexity Models
- `llama-3.1-sonar-small-128k-chat` (default) - Fast, web-connected
- `llama-3.1-sonar-large-128k-chat` - More capable, web-connected

---

## Testing

### Run Integration Tests:
```bash
./venv/bin/python tools/test_llm_integration.py
```

### Test Results:
```
✅ Gemini client initialization
✅ Perplexity client initialization
✅ Helper functions loaded
✅ Error handling with retry logic
```

---

## Example Use Cases

### 1. Content Generation
```python
from tools.L2_foundation import generate_with_gemini

blog_post = generate_with_gemini(
    "Write a 200-word blog post about AI safety",
    temperature=0.8,
    max_tokens=300
)
```

### 2. Web Research
```python
from tools.L2_foundation import search_with_perplexity

research = search_with_perplexity(
    "What are the latest breakthroughs in quantum computing?",
    temperature=0.2
)
```

### 3. Text Summarization
```python
from tools.L2_foundation import summarize_text

summary = summarize_text(
    long_document,
    max_length=150,
    provider="gemini"
)
```

### 4. Interactive Chat
```python
from tools.L2_foundation import chat_with_gemini

conversation = [
    {"role": "user", "content": "Help me debug this Python code"}
]
response = chat_with_gemini(conversation, temperature=0.3)
```

---

## Quality Rubric Compliance

| Gate | Status | Implementation |
|------|--------|----------------|
| 1. SOLID Architecture | ✅ | Single Responsibility, Dependency Inversion |
| 2. Code Hygiene | ✅ | PEP 8, Type Hints, Google-style Docstrings |
| 3. Cyclomatic Complexity | ✅ | Max 3 nesting levels, <50 lines per function |
| 4. Security | ✅ | API keys in `.env`, never in code |
| 5. Agentic Optimizations | ✅ | Deterministic, structured outputs |
| 6. Observability | ✅ | Error context in exceptions |
| 7. Performance | ✅ | Efficient API usage, configurable parameters |
| 8. Database Efficiency | N/A | Not applicable for LLM operations |
| 9. Resilience | ✅ | Retry logic with exponential backoff |
| 10. Test Coverage | ✅ | Integration tests included |

---

## File Structure

```
/Users/franciscocambero/Anitgravity/
├── tools/
│   ├── L1_config/
│   │   ├── __init__.py
│   │   ├── llm_client.py           # Client initialization
│   │   └── supabase_client.py      # (Previously created)
│   ├── L2_foundation/
│   │   ├── __init__.py
│   │   ├── llm_helpers.py          # LLM operations
│   │   └── database_helpers.py     # (Previously created)
│   └── test_llm_integration.py     # Integration tests
└── .env                             # API keys (protected)
```

---

**Status:** ✅ LLM Integration Complete | 🎯 Ready for Application Development
