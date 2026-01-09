# Antigravity System Architecture

> **🚀 NEW WORKSPACE?** Start here: [`START_HERE.md`](START_HERE.md) | Quick Reference: [`QUICK_REFERENCE.md`](QUICK_REFERENCE.md)

## 🧠 The Philosophy: Vibe Coding

This system operates on the **"DO" Framework** (Directive → Orchestration → Execution):
- **The Brain** (`agents.md`): The Constitution. Defines how the system thinks.
- **The Hands** (`tools/`): Atomic Python scripts. Deterministic execution.
- **The Vault** (`.env`): Secrets and configuration. Never committed.

## 🏗️ Architecture Overview

### The 4-Layer Hierarchy
Data flows **UPWARD** only. Circular dependencies are **FORBIDDEN**.

```
L4: Synthesis (api_gateway, daily_report)
    ↑
L3: Analysis (business_rules, scoring_engine)
    ↑
L2: Foundation (input_validation, data_quality)
    ↑
L1: Configuration (system_config, constants)
```

### Directory Structure
```
/docs/              # Directive Layer (Markdown only, NO CODE)
/tools/             # Execution Layer (Atomic Python scripts)
  /L1_config/       # Configuration & Constants
  /L2_foundation/   # Validation & Data Quality
  /L3_analysis/     # Business Logic
  /L4_synthesis/    # Integration & Reporting
/tests/             # Unit & Integration Tests
.env                # Environment Variables (CREATE THIS!)
agents.md           # System Constitution
```

## 🚀 Quickstart

### 1. Environment Setup
```bash
# Copy the environment template
cp .env.example .env

# Edit .env with your actual credentials
# REQUIRED: NEXT_PUBLIC_SUPABASE_URL, NEXT_PUBLIC_SUPABASE_ANON_KEY
nano .env
```

### 2. Install Dependencies
```bash
# Python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Node.js (if using TypeScript/Next.js)
npm install
```

### 3. Verify Installation
```bash
# Run tests
pytest

# Type checking
mypy tools/
```

## 📋 Quality Rubric: The 10 Commandments

Before marking ANY task complete, code must pass:
1. ✅ **SOLID Architecture** (Single Responsibility, Dependency Inversion)
2. ✅ **Code Hygiene** (PEP 8, Type Hints, Docstrings)
3. ✅ **Cyclomatic Complexity** (Max 3 nesting levels, <50 lines per function)
4. ✅ **Security** (OWASP, Input validation, No secrets in code)
5. ✅ **Agentic Optimizations** (Deterministic, Structured outputs)
6. ✅ **Observability** (Structured logging, Error context)
7. ✅ **Performance** (Big O analysis, Generators for large data)
8. ✅ **Database Efficiency** (No N+1 queries, Proper indexing)
9. ✅ **Resilience** (Retry logic, Specific exception handling)
10. ✅ **Test Coverage** (Unit tests, Edge case handling)

## 🔄 Self-Annealing Protocol

The system automatically heals itself:
1. **Detect:** Spot the error (e.g., "API Timeout")
2. **Diagnose:** Reason why it failed (e.g., "Filter too strict")
3. **Fix:** Attempt workaround
4. **Anneal:** Update Directive/Script to handle automatically next time

## 📚 Build Lifecycle

1. **PROTOTYPE:** Validate `system_config` and `input_validation` with mock data
2. **PERSISTENCE:** Integrate Supabase schema
3. **FEATURE BUILD:** Connect L3 (Analysis) and L4 (Synthesis) layers
4. **PRODUCTION:** Docker → GitHub → Cloud deployment

## 🛡️ Security Notes

- **NEVER** commit `.env` to version control
- Use Supabase Row Level Security (RLS) for all tables
- Validate ALL user inputs before processing
- Use parameterized queries (via Supabase SDK/ORM)

## 📖 Next Steps

1. **Create `.env`** from `.env.example` (REQUIRED)
2. **Run Discovery Protocol** to define your system specification
3. **Build L1 Configuration** layer first
4. **Follow the 4-Layer Hierarchy** upward

---

**Need Help?** Review `agents.md` for the complete operating system philosophy.
