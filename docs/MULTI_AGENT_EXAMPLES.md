# Multi-Agent Workflow Examples

## Example 1: E-Commerce Platform

### Agent-Database
- Creates product, user, order tables
- Implements inventory management logic (L3)
- Sets up RLS policies

### Agent-AI  
- Product recommendations (Gemini)
- Search functionality (Perplexity)
- Customer support chatbot

### Agent-API
- REST endpoints for products, cart, checkout
- Payment integration
- Order management system

**Coordination:** Database → AI features → API integration

---

## Example 2: Content Management System

### Agent-Database
- Articles, authors, categories schema
- Content validation logic
- Media storage setup

### Agent-AI
- Content generation (Gemini)
- Research assistant (Perplexity)
- SEO optimization

### Agent-API
- Publishing endpoints
- Scheduling system
- Analytics dashboard

**Coordination:** Parallel work on features, integrate at L4

---

## Example 3: Analytics Dashboard

### Agent-Database
- Events, metrics, users schema
- Data aggregation pipelines
- Real-time ingestion

### Agent-AI
- Trend analysis (Gemini)
- Anomaly detection
- Natural language queries

### Agent-API
- Dashboard endpoints
- Export functionality
- Webhook integrations

**Coordination:** Data pipeline → AI analysis → Visualization APIs

---

## Usage Pattern

**Single Prompt Dispatch:**
```
@Agent-Database: Create user authentication schema
@Agent-AI: Build password strength validator using Gemini  
@Agent-API: Create /register endpoint combining both

Work in parallel, coordinate via task.md
```

**Result:** All agents work simultaneously, log progress, coordinate automatically.
