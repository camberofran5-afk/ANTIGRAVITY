# Agent Team Assignments - Phase 6A

## Team Database (Agent 2 - Backend Specialist)

**Role**: Database Architecture & Integration  
**Responsibility**: Replace in-memory storage with persistent SQLite database

### Skills Required:
- SQLAlchemy ORM
- Database schema design
- Migration systems (Alembic)
- Python async/await
- FastAPI integration

### Tasks:
1. Design database schema
2. Create SQLAlchemy models
3. Implement CRUD operations
4. Set up migrations
5. Test persistence

**Compute Budget**: 80 tool calls, 150K tokens

---

## Team Auth (Agent 4 - Security Specialist)

**Role**: Authentication & Authorization  
**Responsibility**: Implement JWT-based login system

### Skills Required:
- JWT tokens
- Password hashing (bcrypt)
- FastAPI security
- React authentication
- Protected routes

### Tasks:
1. Create auth backend (JWT)
2. Build login/register UI
3. Implement token management
4. Protect API routes
5. Test auth flow

**Compute Budget**: 70 tool calls, 130K tokens

---

## Team UX (Agent 1 - Frontend Specialist)

**Role**: User Experience  
**Responsibility**: Replace alerts with professional toast notifications

### Skills Required:
- React components
- react-hot-toast library
- TypeScript
- UI/UX best practices

### Tasks:
1. Install toast library
2. Create toast utilities
3. Replace all alerts
4. Add loading states
5. Style toasts

**Compute Budget**: 15 tool calls, 20K tokens

---

## Coordination Protocol

### Daily Sync:
- Share progress updates
- Resolve blockers
- Coordinate API contracts
- Review code changes

### Integration Points:
1. **Database ↔ Auth**: User model schema
2. **Auth ↔ UX**: Login API endpoints
3. **UX ↔ Database**: Toast on CRUD operations

### Communication:
- Use shared task.md for status
- Document API changes
- Flag blockers immediately
- Request reviews when needed

---

## Success Metrics

**Phase 6A Complete When**:
- ✅ All 29 story points delivered
- ✅ Database persistence working
- ✅ Authentication functional
- ✅ Toast notifications live
- ✅ All tests passing
- ✅ Within compute budget (300K tokens)

---

**Team Lead**: Agent 0 (PM)  
**Start Date**: 2026-01-13  
**Target**: Complete Phase 6A before starting 6B
