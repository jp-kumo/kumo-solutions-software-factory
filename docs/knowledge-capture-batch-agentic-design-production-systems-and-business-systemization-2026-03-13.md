# Knowledge Capture Batch: Agentic Design, Production AI Delivery, and Business Systemization (2026-03-13)

## Sources
1. Master ALL 20 Agentic AI Design Patterns [Complete Course]
2. End to End Production Legal AI Agents (MCP, Google ADK, Docling)
3. How to Build AI Agents from Scratch in 2026 (Zero → Production Stack)
4. Build These AI/ML Projects In 2026 (NEW Projects)
5. How I Build and Ship Custom AI Solutions for Clients
6. Perplexity’s NEW Computer is INSANE (10x Your Productivity)
7. I’ve changed how I build software
8. Business Process Mapping 101 (Step By Step Guide)
9. How To Build A Business That Runs Itself
10. Ultimate Guide to Systemize Your Business in 2026

---

## Why this batch matters for Jacques
This batch is unusually high-value because it connects three outcomes Jacques needs now:
- **Hiring signal** (portfolio artifacts that look like real production engineering)
- **Consulting revenue signal** (repeatable AI delivery process for Kumo Solutions)
- **Operator signal** (business systems that reduce founder bottlenecks)

Together, these create differentiated “builder + operator” positioning rather than generic AI-project portfolios.

---

## Core synthesis (cross-source)

### 1) Agentic patterns are useful only when tied to controls
Common pattern content (prompt chaining, routing, parallelization, reflection, tool use, planning, multi-agent, memory, eval, safety) is valuable **only** when paired with:
- typed I/O contracts
- confidence thresholds
- retry/backoff limits
- explicit escalation paths
- observability and postmortem loops

Hiring/consulting implication: “I know patterns” is weak; “I implemented pattern + control plane + evals” is strong.

### 2) Production readiness is mostly non-model work
Across sources, practical production quality comes from:
- schema validation (e.g., Pydantic)
- parser/ingest quality comparison
- uncertainty profiling
- flow orchestration with fail-safe states
- evals, drift monitoring, and alerting
- deployment hygiene and security boundaries

This aligns with regulated-industry expectations and Jacques’s background in quality/risk contexts.

### 3) Multi-agent systems should stay scoped and testable
A recurring warning: over-complex agent-to-agent messaging creates fragile systems.
Preferred strategy:
- start with narrow roles
- deterministic handoffs
- explicit graph/flow boundaries
- human-in-loop at high-risk decisions
- avoid “autonomous everything” architecture for v1

### 4) Consulting delivery advantage now = standardized stack + process
The custom-AI delivery source is clear:
- fixed architecture pattern
- sprint cadence
- evaluation gates
- deployment runbooks
- observability baseline

This is ideal for Kumo service packaging because it turns one-off freelance work into repeatable productized delivery.

### 5) Business systemization is execution infrastructure, not admin overhead
Process mapping/systemization sources converge on:
- map work by function and task
- assign clear ownership
- track cadence/KPIs/errors
- maintain lightweight SOP/checklist templates
- improve from error logs and feedback loops

This supports Jacques’s goal of sustainable multi-stream income by preventing founder-only bottlenecks.

---

## High-signal project blueprints (portfolio + consulting alignment)

## Project A — Agent Pattern Reliability Bench (APRB)
**Employer/Client problem:** Teams know agent patterns conceptually but cannot prove reliability/cost tradeoffs in production.

**Solution:** Build a benchmark harness that compares selected patterns (prompt chaining, routing, reflection, ReAct, planning) against the same task suite with identical evaluation gates.

**Measurable impact target:**
- +X% task success on edge-case suite
- -Y% hallucination rate via verification loop
- Z% token/cost delta by strategy
- MTTD/MTTR on failure classes with traceability

**Stack:** Python, FastAPI, Pydantic, LangGraph/CrewAI (or equivalent), evaluation suite, Langfuse/OpenTelemetry-style tracing, SQLite/Postgres.

**Role relevance:** ML/AI engineer, LLM systems engineer, platform engineer.

---

## Project B — Regulated Document Agent with Governance Controls
**Employer/Client problem:** Document-heavy workflows fail due to extraction errors, missing confidence checks, and no escalation boundaries.

**Solution:** Build an end-to-end pipeline:
- parser A/B/C comparison (e.g., Docling vs alternatives)
- uncertainty and recency scoring
- typed output with mandatory citations
- policy boundaries + HITL gate
- auditable decision trail

**Measurable impact target:**
- extraction fidelity improvement vs baseline parser
- reduction in unsafe/unsupported outputs
- SLA for escalation turnaround
- % outputs with complete citation lineage

**Stack:** Python, Pydantic, document parsers, ADK/LangGraph orchestration, policy engine, audit log store.

**Role relevance:** AI governance, applied AI in regulated environments, enterprise AI implementation.

---

## Project C — AI Delivery OS for Kumo Solutions (internal + showcase)
**Employer/Client problem:** Custom AI projects fail from unclear discovery, bad scoping, no eval gate, and weak handoff.

**Solution:** Create a reusable “delivery OS”:
- discovery rubric (ROI + risk + data readiness)
- sprint templates
- acceptance/eval checklists
- deployment and monitoring runbook
- post-launch improvement loop

**Measurable impact target:**
- reduced time from discovery → first deployed MVP
- fewer post-launch defects
- improved client acceptance rate at sprint review
- predictable maintenance effort

**Stack:** docs/templates repo + automation scripts + issue templates + dashboard snippets.

**Role relevance:** AI solutions architect, technical consultant, engineering lead.

---

## Project D — Business Process Intelligence Copilot
**Employer/Client problem:** SMEs operate from tribal knowledge and cannot scale without founder intervention.

**Solution:**
- process inventory mapper
- ownership matrix
- SOP/checklist generator
- process health dashboard (errors, latency, handoff failures)
- improvement recommendation engine

**Measurable impact target:**
- reduced cycle time for key process
- reduced rework/error count
- onboarding-time reduction for new team members

**Stack:** workflow mapping + lightweight knowledge base + reporting layer.

**Role relevance:** operations-focused AI engineer, automation consultant, digital transformation roles.

---

## Recruiter-facing differentiation narrative
Jacques’s strongest narrative from this batch:
1. **I design agentic systems with control gates, not demos.**
2. **I can ship regulated-workflow AI with traceability and escalation.**
3. **I standardize delivery for repeatable business outcomes.**
4. **I connect technical architecture to operating model and measurable KPIs.**

That narrative maps cleanly to cloud/AI engineering roles and Kumo client work.

---

## Immediate implementation backlog (next 14 days)
1. Build APRB v0 with 3 patterns + one evaluation dataset.
2. Build Document Agent v0 with parser comparison + confidence thresholds.
3. Publish Kumo AI Delivery OS v0 templates (discovery, sprint, eval, runbook).
4. Create one portfolio page per project with problem → architecture → evidence → outcomes.

---

## Suggested KB tags
- agentic-design-patterns
- production-ai-engineering
- ai-governance
- evaluation-and-observability
- multi-agent-orchestration
- process-systemization
- consulting-delivery
- portfolio-hiring
- kumo

---

## Notes
This batch reinforces a strategic position: **“production AI systems engineer with governance and operating-model discipline.”**
That is higher-signal than generic LLM app demos and directly supports Jacques’s 2026 hiring + consulting goals.
