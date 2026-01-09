# Building Complete SaaS Applications with Antigravity

## Overview

This guide shows you how to build **production-ready SaaS applications** using the Antigravity orchestration framework. Each example includes complete architecture, from authentication to billing.

---

## SaaS Application Template

Every SaaS app needs these core components:

```
┌─────────────────────────────────────────────────────────────┐
│ SAAS APPLICATION ARCHITECTURE                               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ 1. Authentication & Authorization                           │
│    - User registration/login                                │
│    - JWT tokens                                             │
│    - Role-based access control (RBAC)                       │
│                                                              │
│ 2. Multi-Tenancy                                            │
│    - Organization/workspace isolation                       │
│    - Row-level security (RLS)                               │
│    - Tenant-specific data                                   │
│                                                              │
│ 3. Subscription & Billing                                   │
│    - Stripe integration                                     │
│    - Plan management (Free, Pro, Enterprise)                │
│    - Usage tracking                                         │
│                                                              │
│ 4. Core Features                                            │
│    - Your unique value proposition                          │
│    - Business logic                                         │
│    - AI/ML capabilities                                     │
│                                                              │
│ 5. API Layer                                                │
│    - RESTful API                                            │
│    - Rate limiting                                          │
│    - API keys for integrations                              │
│                                                              │
│ 6. Frontend                                                 │
│    - React/Next.js dashboard                                │
│    - Responsive design                                      │
│    - Real-time updates                                      │
│                                                              │
│ 7. Infrastructure                                           │
│    - Supabase (Database + Auth + Storage)                   │
│    - Vercel/Railway (Hosting)                               │
│    - Monitoring & Analytics                                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Example 1: AI Content Generator SaaS

**Product:** Generate marketing content using AI (blog posts, social media, ads)

### Complete Build Workflow

```python
# apps/content_generator_saas.py
from tools.L4_synthesis.workflow_builder import WorkflowBuilder
from tools.L2_foundation.agent_helpers import AgentRole

def build_content_generator_saas():
    """
    Build a complete AI Content Generator SaaS application
    
    Features:
    - User authentication
    - Multi-tenant workspaces
    - Stripe subscription (Free, Pro, Enterprise)
    - AI content generation (blog posts, social media, ads)
    - Content history and templates
    - API for integrations
    - Usage tracking and limits
    """
    
    workflow = (
        WorkflowBuilder("AI Content Generator SaaS")
        
        # ============================================================
        # PHASE 1: AUTHENTICATION & USER MANAGEMENT
        # ============================================================
        
        .add_step(
            "auth_config",
            AgentRole.DATABASE,
            """L1 Configuration: Define authentication system
            - User roles: admin, user
            - Auth methods: email/password, Google OAuth
            - Session management: JWT tokens
            - Password requirements
            """
        )
        
        .add_step(
            "auth_schema",
            AgentRole.DATABASE,
            """L2 Database: Create auth schema in Supabase
            Tables:
            - users (id, email, password_hash, role, created_at)
            - profiles (user_id, name, avatar_url, bio)
            - sessions (user_id, token, expires_at)
            
            RLS Policies:
            - Users can only read/update their own profile
            - Admins can read all users
            """,
            depends_on=["auth_config"]
        )
        
        .add_step(
            "auth_api",
            AgentRole.API,
            """L4 API: Create authentication endpoints
            - POST /auth/register
            - POST /auth/login
            - POST /auth/logout
            - POST /auth/refresh
            - GET /auth/me
            - POST /auth/google (OAuth)
            """,
            depends_on=["auth_schema"]
        )
        
        # ============================================================
        # PHASE 2: MULTI-TENANCY (WORKSPACES)
        # ============================================================
        
        .add_step(
            "workspace_schema",
            AgentRole.DATABASE,
            """L2 Database: Create workspace schema
            Tables:
            - workspaces (id, name, slug, owner_id, plan, created_at)
            - workspace_members (workspace_id, user_id, role, invited_at)
            - workspace_invites (workspace_id, email, token, expires_at)
            
            RLS Policies:
            - Users can only access workspaces they're members of
            - Owners can manage workspace members
            - All data scoped to workspace_id
            """,
            depends_on=["auth_schema"]
        )
        
        .add_step(
            "workspace_api",
            AgentRole.API,
            """L4 API: Create workspace endpoints
            - POST /workspaces (create)
            - GET /workspaces (list user's workspaces)
            - GET /workspaces/{id}
            - PUT /workspaces/{id}
            - DELETE /workspaces/{id}
            - POST /workspaces/{id}/members (invite)
            - DELETE /workspaces/{id}/members/{user_id}
            """,
            depends_on=["workspace_schema"]
        )
        
        # ============================================================
        # PHASE 3: SUBSCRIPTION & BILLING
        # ============================================================
        
        .add_step(
            "billing_config",
            AgentRole.DATABASE,
            """L1 Configuration: Define subscription plans
            Plans:
            - Free: 10 generations/month, basic templates
            - Pro ($29/mo): 500 generations/month, all templates, API access
            - Enterprise ($99/mo): Unlimited, priority support, custom templates
            
            Stripe configuration:
            - Product IDs
            - Price IDs
            - Webhook endpoints
            """
        )
        
        .add_step(
            "billing_schema",
            AgentRole.DATABASE,
            """L2 Database: Create billing schema
            Tables:
            - subscriptions (workspace_id, plan, stripe_customer_id, 
                            stripe_subscription_id, status, current_period_end)
            - usage_tracking (workspace_id, month, generations_used, api_calls)
            - invoices (workspace_id, stripe_invoice_id, amount, status, paid_at)
            
            RLS Policies:
            - Workspace owners can view their subscription
            - System can update usage tracking
            """,
            depends_on=["billing_config", "workspace_schema"]
        )
        
        .add_step(
            "stripe_integration",
            AgentRole.API,
            """L4 API: Integrate Stripe
            Endpoints:
            - POST /billing/checkout (create checkout session)
            - POST /billing/portal (customer portal)
            - POST /billing/webhook (Stripe webhooks)
            - GET /billing/subscription
            - POST /billing/upgrade
            - POST /billing/cancel
            
            Webhook handlers:
            - checkout.session.completed
            - customer.subscription.updated
            - customer.subscription.deleted
            - invoice.paid
            - invoice.payment_failed
            """,
            depends_on=["billing_schema"]
        )
        
        # ============================================================
        # PHASE 4: CORE FEATURE - AI CONTENT GENERATION
        # ============================================================
        
        .add_step(
            "content_schema",
            AgentRole.DATABASE,
            """L2 Database: Create content schema
            Tables:
            - content_templates (id, name, type, prompt_template, category)
            - generated_content (id, workspace_id, user_id, template_id,
                                input_params, output_text, tokens_used, created_at)
            - content_history (workspace_id, user_id, content_id, action, timestamp)
            
            Types: blog_post, social_media, ad_copy, email, product_description
            
            RLS Policies:
            - Users can only access content in their workspace
            - Content scoped by workspace_id
            """,
            depends_on=["workspace_schema"]
        )
        
        .add_step(
            "content_generation_logic",
            AgentRole.AI,
            """L3 Business Logic: Implement AI content generation
            
            Features:
            - Use Gemini for content generation
            - Template-based prompts
            - Tone adjustment (professional, casual, friendly)
            - Length control (short, medium, long)
            - SEO optimization
            - Multi-language support
            
            Usage limits:
            - Check workspace subscription plan
            - Track usage against limits
            - Return error if limit exceeded
            
            Quality checks:
            - Profanity filter
            - Plagiarism detection
            - Brand safety
            """,
            depends_on=["content_schema", "billing_schema"]
        )
        
        .add_step(
            "content_api",
            AgentRole.API,
            """L4 API: Create content generation endpoints
            - POST /content/generate
              Input: { template_id, params: {topic, tone, length} }
              Output: { content, tokens_used, suggestions }
            
            - GET /content/history
            - GET /content/{id}
            - PUT /content/{id} (edit)
            - DELETE /content/{id}
            - POST /content/{id}/export (PDF, DOCX)
            
            - GET /templates
            - GET /templates/{id}
            - POST /templates (custom templates for Enterprise)
            """,
            depends_on=["content_generation_logic"]
        )
        
        # ============================================================
        # PHASE 5: API FOR INTEGRATIONS
        # ============================================================
        
        .add_step(
            "api_keys_schema",
            AgentRole.DATABASE,
            """L2 Database: Create API keys schema
            Tables:
            - api_keys (id, workspace_id, name, key_hash, last_used, created_at)
            - api_usage (api_key_id, endpoint, requests_count, date)
            
            RLS Policies:
            - Workspace owners can manage API keys
            - Track usage per API key
            """
        )
        
        .add_step(
            "public_api",
            AgentRole.API,
            """L4 API: Create public API for integrations
            
            Authentication: Bearer token (API key)
            Rate limiting: Based on subscription plan
            
            Endpoints:
            - POST /api/v1/generate
            - GET /api/v1/templates
            - GET /api/v1/usage
            
            Features:
            - API key authentication
            - Rate limiting (Free: 100/day, Pro: 10,000/day, Enterprise: unlimited)
            - Usage tracking
            - Webhook notifications
            """,
            depends_on=["api_keys_schema", "content_api"]
        )
        
        # ============================================================
        # PHASE 6: FRONTEND APPLICATION
        # ============================================================
        
        .add_step(
            "frontend_structure",
            AgentRole.API,
            """Create Next.js frontend structure
            
            Pages:
            - / (landing page)
            - /login
            - /register
            - /dashboard (workspace selector)
            - /workspace/{id}/generate (main app)
            - /workspace/{id}/history
            - /workspace/{id}/templates
            - /workspace/{id}/settings
            - /workspace/{id}/billing
            - /workspace/{id}/api-keys
            - /pricing
            - /docs
            
            Components:
            - ContentGenerator (main UI)
            - TemplateSelector
            - ContentEditor
            - UsageChart
            - BillingPanel
            - TeamManagement
            
            State Management: Zustand or Redux
            Styling: Tailwind CSS
            """,
            depends_on=["content_api", "stripe_integration"]
        )
        
        .add_step(
            "ui_implementation",
            AgentRole.API,
            """Implement frontend components
            
            ContentGenerator:
            - Template selection dropdown
            - Input form (topic, tone, length)
            - Generate button
            - Loading state with progress
            - Output display with copy/export
            - Regenerate option
            
            Dashboard:
            - Usage statistics
            - Recent generations
            - Quick actions
            - Upgrade prompts (for Free users)
            
            Billing:
            - Current plan display
            - Usage meter
            - Upgrade/downgrade buttons
            - Invoice history
            """,
            depends_on=["frontend_structure"]
        )
        
        # ============================================================
        # PHASE 7: TESTING
        # ============================================================
        
        .add_step(
            "backend_tests",
            AgentRole.QA,
            """Write backend tests
            
            Unit Tests:
            - Auth logic
            - Content generation
            - Usage tracking
            - Billing calculations
            
            Integration Tests:
            - Auth flow (register → login → access)
            - Content generation flow
            - Stripe webhook handling
            - API key authentication
            
            E2E Tests:
            - User signup → create workspace → generate content
            - Subscription upgrade flow
            - Usage limit enforcement
            """,
            depends_on=["public_api"]
        )
        
        .add_step(
            "frontend_tests",
            AgentRole.QA,
            """Write frontend tests
            
            Component Tests:
            - ContentGenerator renders correctly
            - Form validation works
            - API calls handled properly
            
            E2E Tests (Playwright):
            - Complete user journey
            - Payment flow
            - Content generation
            """,
            depends_on=["ui_implementation"]
        )
        
        # ============================================================
        # PHASE 8: DEPLOYMENT & MONITORING
        # ============================================================
        
        .add_step(
            "deployment_config",
            AgentRole.API,
            """Create deployment configuration
            
            Backend:
            - FastAPI on Railway/Render
            - Environment variables
            - Database migrations
            - Stripe webhook URL
            
            Frontend:
            - Next.js on Vercel
            - Environment variables
            - API URL configuration
            
            Database:
            - Supabase project
            - RLS policies enabled
            - Backups configured
            
            Monitoring:
            - Sentry for error tracking
            - PostHog for analytics
            - Stripe dashboard for billing
            """,
            depends_on=["backend_tests", "frontend_tests"]
        )
        
        .add_approval_gate(
            "review_before_deploy",
            """Review before production deployment:
            - All tests passing?
            - Stripe in production mode?
            - Environment variables set?
            - RLS policies tested?
            - Rate limiting configured?
            - Error tracking enabled?
            """
        )
        
        .add_step(
            "deploy",
            AgentRole.API,
            """Deploy to production
            
            Steps:
            1. Deploy database migrations
            2. Deploy backend API
            3. Deploy frontend
            4. Configure DNS
            5. Enable SSL
            6. Test production endpoints
            7. Monitor for errors
            """,
            depends_on=["deployment_config"]
        )
        
        .build()
    )
    
    return workflow.execute(
        enable_observability=True,
        enable_cost_tracking=True,
        notify_on_approval=True
    )


# Execute the workflow
if __name__ == "__main__":
    print("🚀 Building AI Content Generator SaaS...")
    result = build_content_generator_saas()
    
    print(f"\n✅ SaaS Application Built Successfully!")
    print(f"Duration: {result.duration / 60:.1f} minutes")
    print(f"Files Created: {result.files_created}")
    print(f"Database Tables: {result.tables_created}")
    print(f"API Endpoints: {result.endpoints_created}")
    print(f"Tests Written: {result.tests_count}")
    print(f"Estimated Cost: ${result.cost:.2f}")
```

---

## Example 2: Project Management SaaS

**Product:** Team collaboration and project management tool

```python
# apps/project_management_saas.py

def build_project_management_saas():
    """
    Build a complete Project Management SaaS (like Asana/Linear)
    
    Features:
    - Multi-tenant workspaces
    - Projects and tasks
    - Team collaboration
    - Real-time updates
    - File attachments
    - Time tracking
    - Reporting and analytics
    """
    
    workflow = (
        WorkflowBuilder("Project Management SaaS")
        
        # Auth & Multi-tenancy (same as above)
        .add_step("auth_setup", AgentRole.DATABASE, "Setup authentication")
        .add_step("workspace_setup", AgentRole.DATABASE, "Setup workspaces")
        .add_step("billing_setup", AgentRole.API, "Setup Stripe billing")
        
        # Core Features
        .add_step(
            "project_schema",
            AgentRole.DATABASE,
            """Create project management schema
            Tables:
            - projects (workspace_id, name, description, status, owner_id)
            - tasks (project_id, title, description, assignee_id, status, priority, due_date)
            - task_comments (task_id, user_id, content, created_at)
            - task_attachments (task_id, file_url, file_name, uploaded_by)
            - time_entries (task_id, user_id, hours, date, description)
            - labels (workspace_id, name, color)
            - task_labels (task_id, label_id)
            
            Statuses: backlog, todo, in_progress, in_review, done
            Priorities: low, medium, high, urgent
            """
        )
        
        .add_step(
            "realtime_logic",
            AgentRole.AI,
            """Implement real-time collaboration
            - Supabase Realtime for live updates
            - Presence tracking (who's online)
            - Collaborative editing
            - Activity feed
            - Notifications
            """
        )
        
        .add_step(
            "analytics_logic",
            AgentRole.AI,
            """Implement analytics and reporting
            - Burndown charts
            - Velocity tracking
            - Time tracking reports
            - Team productivity metrics
            - Custom dashboards
            """
        )
        
        .add_step(
            "project_api",
            AgentRole.API,
            """Create project management API
            - Projects CRUD
            - Tasks CRUD with filtering
            - Comments and attachments
            - Time tracking
            - Reports and analytics
            - Webhooks for integrations
            """
        )
        
        # Frontend
        .add_step(
            "frontend_app",
            AgentRole.API,
            """Build React frontend
            - Kanban board view
            - List view
            - Calendar view
            - Gantt chart
            - Team dashboard
            - Real-time updates
            """
        )
        
        .build()
    )
    
    return workflow.execute()
```

---

## Example 3: AI-Powered CRM SaaS

**Product:** Customer Relationship Management with AI insights

```python
# apps/ai_crm_saas.py

def build_ai_crm_saas():
    """
    Build an AI-Powered CRM SaaS
    
    Features:
    - Contact and company management
    - Deal pipeline
    - Email integration
    - AI-powered lead scoring
    - AI email drafting
    - Sales forecasting
    - Activity tracking
    """
    
    workflow = (
        WorkflowBuilder("AI-Powered CRM SaaS")
        
        # Standard SaaS foundation
        .add_step("auth_setup", AgentRole.DATABASE, "Setup authentication")
        .add_step("workspace_setup", AgentRole.DATABASE, "Setup workspaces")
        .add_step("billing_setup", AgentRole.API, "Setup Stripe billing")
        
        # CRM Core
        .add_step(
            "crm_schema",
            AgentRole.DATABASE,
            """Create CRM schema
            Tables:
            - contacts (workspace_id, name, email, phone, company_id, owner_id)
            - companies (workspace_id, name, industry, size, website)
            - deals (workspace_id, title, value, stage, contact_id, close_date)
            - activities (workspace_id, type, contact_id, deal_id, notes, date)
            - emails (workspace_id, contact_id, subject, body, sent_at)
            - tasks (workspace_id, assignee_id, contact_id, due_date, status)
            
            Deal Stages: lead, qualified, proposal, negotiation, closed_won, closed_lost
            Activity Types: call, email, meeting, note
            """
        )
        
        # AI Features
        .add_step(
            "ai_lead_scoring",
            AgentRole.AI,
            """Implement AI lead scoring
            - Analyze contact engagement
            - Score based on company size, industry, activity
            - Predict likelihood to close
            - Recommend next actions
            - Use Gemini for analysis
            """
        )
        
        .add_step(
            "ai_email_assistant",
            AgentRole.AI,
            """Implement AI email assistant
            - Draft personalized emails
            - Suggest follow-up timing
            - Analyze email sentiment
            - Auto-categorize emails
            - Generate meeting summaries
            """
        )
        
        .add_step(
            "sales_forecasting",
            AgentRole.AI,
            """Implement sales forecasting
            - Predict monthly/quarterly revenue
            - Identify at-risk deals
            - Recommend deal prioritization
            - Team performance analytics
            """
        )
        
        # Integrations
        .add_step(
            "email_integration",
            AgentRole.API,
            """Integrate email (Gmail, Outlook)
            - OAuth authentication
            - Sync emails automatically
            - Send emails from CRM
            - Track email opens/clicks
            """
        )
        
        .add_step(
            "crm_api",
            AgentRole.API,
            """Create CRM API
            - Contacts and companies CRUD
            - Deals pipeline management
            - Activities logging
            - AI insights endpoints
            - Reporting and analytics
            - Webhooks for integrations
            """
        )
        
        # Frontend
        .add_step(
            "crm_frontend",
            AgentRole.API,
            """Build CRM frontend
            - Contact/company management
            - Deal pipeline (Kanban)
            - Activity timeline
            - Email inbox
            - AI insights dashboard
            - Reports and forecasting
            """
        )
        
        .build()
    )
    
    return workflow.execute()
```

---

## SaaS Application Generator

Want to build ANY SaaS app? Use this meta-workflow:

```python
# apps/saas_generator.py

def generate_saas_app(description: str):
    """
    Generate a complete SaaS application from a description
    
    Example:
        generate_saas_app("Build a social media scheduling tool")
    """
    
    # Phase 1: Research and plan
    from tools.L4_synthesis.openmanus_integration import get_openmanus
    
    research = get_openmanus().research(
        f"SaaS application architecture for: {description}",
        max_results=10
    )
    
    # Phase 2: Generate architecture
    from tools.L4_synthesis.agno_integration import get_agno_agent
    
    architect = get_agno_agent(AgentRole.ORCHESTRATOR)
    architecture = architect.execute_task(
        f"""Based on this research, design a complete SaaS architecture for: {description}
        
        Research findings: {research.synthesis}
        
        Include:
        1. Database schema (all tables)
        2. API endpoints
        3. Frontend pages
        4. Third-party integrations needed
        5. Subscription plans
        6. Unique features
        """,
        context={"research": research}
    )
    
    # Phase 3: Build the application
    workflow = (
        WorkflowBuilder(f"SaaS: {description}")
        
        # Foundation
        .add_step("auth", AgentRole.DATABASE, "Setup authentication")
        .add_step("workspaces", AgentRole.DATABASE, "Setup multi-tenancy")
        .add_step("billing", AgentRole.API, "Setup Stripe billing")
        
        # Core features (dynamically generated from architecture)
        .add_step("database", AgentRole.DATABASE, 
                  f"Implement database schema: {architecture}")
        .add_step("business_logic", AgentRole.AI,
                  f"Implement business logic: {architecture}")
        .add_step("api", AgentRole.API,
                  f"Create API endpoints: {architecture}")
        .add_step("frontend", AgentRole.API,
                  f"Build frontend: {architecture}")
        
        # Testing and deployment
        .add_step("tests", AgentRole.QA, "Write comprehensive tests")
        .add_approval_gate("review", "Review before deployment")
        .add_step("deploy", AgentRole.API, "Deploy to production")
        
        .build()
    )
    
    return workflow.execute()


# Usage
if __name__ == "__main__":
    # Generate any SaaS app!
    result = generate_saas_app(
        "Build a social media scheduling tool with AI caption generation"
    )
    
    # Or
    result = generate_saas_app(
        "Build an invoice management system with OCR and payment tracking"
    )
    
    # Or
    result = generate_saas_app(
        "Build a customer support ticketing system with AI-powered responses"
    )
```

---

## Common SaaS Patterns

### Pattern 1: Freemium Model

```python
SUBSCRIPTION_PLANS = {
    "free": {
        "price": 0,
        "features": {
            "max_workspaces": 1,
            "max_members": 3,
            "max_projects": 5,
            "storage_gb": 1,
            "api_calls_per_month": 100,
        }
    },
    "pro": {
        "price": 29,
        "stripe_price_id": "price_xxx",
        "features": {
            "max_workspaces": 5,
            "max_members": 25,
            "max_projects": 100,
            "storage_gb": 50,
            "api_calls_per_month": 10000,
            "priority_support": True,
        }
    },
    "enterprise": {
        "price": 99,
        "stripe_price_id": "price_yyy",
        "features": {
            "max_workspaces": "unlimited",
            "max_members": "unlimited",
            "max_projects": "unlimited",
            "storage_gb": 500,
            "api_calls_per_month": "unlimited",
            "priority_support": True,
            "custom_integrations": True,
            "dedicated_support": True,
        }
    }
}
```

### Pattern 2: Usage-Based Billing

```python
# Track usage and charge accordingly
def track_usage(workspace_id: str, resource: str, amount: int):
    """Track resource usage for billing"""
    
    # Log usage
    supabase.table("usage_tracking").insert({
        "workspace_id": workspace_id,
        "resource": resource,  # e.g., "api_calls", "storage_gb", "ai_generations"
        "amount": amount,
        "timestamp": datetime.now()
    }).execute()
    
    # Check if limit exceeded
    subscription = get_subscription(workspace_id)
    current_usage = get_current_usage(workspace_id, resource)
    
    if current_usage > subscription.limits[resource]:
        # Charge overage or block access
        if subscription.plan == "enterprise":
            charge_overage(workspace_id, resource, amount)
        else:
            raise UsageLimitExceeded(f"{resource} limit exceeded")
```

### Pattern 3: White-Label SaaS

```python
# Allow customers to white-label your SaaS
def setup_white_label(workspace_id: str, config: dict):
    """Setup white-label configuration"""
    
    supabase.table("white_label_config").insert({
        "workspace_id": workspace_id,
        "custom_domain": config["domain"],  # e.g., "app.customer.com"
        "logo_url": config["logo"],
        "primary_color": config["color"],
        "company_name": config["name"],
        "support_email": config["support_email"],
    }).execute()
    
    # Configure DNS and SSL
    setup_custom_domain(config["domain"])
```

---

## Next Steps

1. **Choose a SaaS idea** from the examples or create your own
2. **Run the generator** to build the complete application
3. **Customize** the generated code for your specific needs
4. **Deploy** to production
5. **Launch** and start acquiring customers!

The orchestration framework handles all the complexity - you just define what you want to build!
