# In-House Development Department Blueprint (Cost-Safe)

## Mission
Build and operate an internal, role-specialized software department that can design, build, secure, test, and ship production-quality applications (starting with local CRM), while staying lean and cost-controlled.

## Phase 1 (Activate now): 4 Core Agents

### 1) Product Architect
**Owns:** requirements translation, architecture, technical decisions

**Definition of done:**
- One-page architecture decision record (ADR)
- Clear module boundaries
- Risk + tradeoff notes

---

### 2) Frontend/UX Engineer
**Owns:** UI flows, responsiveness, accessibility, client-side state

**Definition of done:**
- Working UI flows for sprint scope
- Responsive behavior verified
- Accessibility baseline checks complete

---

### 3) Backend/Data Engineer
**Owns:** API, business logic, database schema + migrations

**Definition of done:**
- API endpoints for sprint scope
- Migration + schema updates applied
- Error handling + validation in place

---

### 4) QA/Security Engineer (combined)
**Owns:** test strategy, bug gates, auth/security guardrails

**Definition of done:**
- Test coverage for critical paths
- Security checklist pass for release
- Blocking defects triaged and resolved

## Phase 2 (Add when workload justifies)
- DevOps/Infra Engineer
- GRC/Compliance Specialist
- Dedicated Database Performance Specialist

## Operating Rhythm
- Daily async standup in Slack (`#exec-priorities`):
  - Yesterday shipped
  - Today focus
  - Blocker
- Weekly architecture + quality review
- Monthly tech debt + security hardening review

## Delivery Pipeline (for each feature)
1. Product Architect writes feature brief + acceptance criteria
2. Frontend/Backend implement in parallel
3. QA/Security validates + gates release
4. Architect signs release notes + next sprint handoff

## Local CRM Program (first target)

### MVP Scope
- Contacts
- Organizations
- Opportunities
- Pipeline stages
- Tasks/follow-ups
- Interaction notes

### Suggested Stack (pragmatic)
- Frontend: React + Tailwind
- Backend: Node/NestJS (or FastAPI if Python path chosen)
- DB: PostgreSQL + Prisma
- Auth: local auth + RBAC-lite
- Deploy: local-first Docker compose

### Non-Negotiables
- Data export/backups from day 1
- Activity log on record changes
- Search across contacts/orgs/opportunities

## Cost Guardrails for Department
- Use low-cost/default models for routine planning/reporting
- Escalate model/reasoning only for blocker resolution
- Keep prompts and handoffs concise and file-backed
- Reuse templates/playbooks to reduce token burn

## Immediate Next 7 Days
1. Lock CRM data model v1
2. Build CRUD for contacts + opportunities
3. Add pipeline board view
4. Add follow-up task scheduler
5. Implement basic QA + security checklist
6. Ship internal demo + gather feedback
7. Plan v1.1 based on real usage
