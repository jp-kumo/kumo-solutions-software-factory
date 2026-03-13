# Portfolio-Ready Project Specs (from Agentic + Production Systems Batches)

## Candidate 1 — Agent Reliability Control Plane

### Employer problem
Teams can demo agents, but cannot prove reliability, cost control, and safety under real multi-step workloads.

### Solution
Build a control plane that wraps agent workflows with:
- model routing by task complexity
- typed input/output validation
- retry/backoff and fallback model strategy
- confidence-based escalation path
- trace + evaluation dashboards

### Deliverables
- architecture diagram
- runnable demo workflow (3+ task classes)
- evaluation harness (success, hallucination, cost, latency)
- incident log with root-cause examples
- runbook for intervention and recovery

### Measurable impact targets
- 20–40% lower cost-per-task vs single-model baseline
- measurable drop in unsupported/hallucinated outputs
- reduced mean time to diagnose failures via traces

### Stack
Python, FastAPI, Pydantic, orchestration framework, telemetry (Langfuse/OpenTelemetry), SQLite/Postgres.

### Role relevance
AI/ML Engineer, LLM Systems Engineer, AI Platform Engineer.

### Resume bullet draft
Engineered a production-style agent control plane with model routing, validation gates, and fallback logic; reduced cost-per-task and improved reliability across multi-step workflows while adding full traceability for failure diagnosis.

---

## Candidate 2 — Regulated Document AI Agent (Governed)

### Employer problem
Document-heavy regulated workflows fail when extraction confidence, policy boundaries, and escalation are missing.

### Solution
Implement a governed document pipeline:
- parser comparison and quality scoring
- uncertainty profiling and recency/consistency checks
- citation-required answer generation
- policy checks + human-in-loop for high-risk cases
- auditable decision history

### Deliverables
- parser benchmark report
- governed extraction + review pipeline
- policy rule set and escalation matrix
- audit trail dataset and sample compliance report

### Measurable impact targets
- improved extraction quality vs baseline parser
- increased citation-complete outputs
- reduced unsafe responses in high-risk scenarios

### Stack
Python, document parsers (Docling/LlamaIndex/PDF libs), orchestration framework, Pydantic, policy layer, audit DB.

### Role relevance
Applied AI Engineer (regulated domains), Responsible AI Engineer, AI Governance Engineer.

### Resume bullet draft
Built a governed document-intelligence agent with parser benchmarking, uncertainty scoring, policy checks, and HITL escalation; improved extraction quality and produced citation-complete, auditable outputs for regulated-style workflows.

---

## Candidate 3 — Workflow Automation ROI Engine

### Employer problem
SME operations lose hours weekly to repetitive process work (lead intake, follow-up, invoicing).

### Solution
Ship a linked automation suite that:
- ingests leads automatically
- executes follow-up cadence with state checks
- triggers invoice and reminder workflows
- escalates exceptions to human operator

### Deliverables
- 3 workflow diagrams
- implemented automations + monitoring
- KPI dashboard (hours saved, response time, payment cycle)
- operating SOP + failure handling checklist

### Measurable impact targets
- 10+ hours/week reclaimed
- improved follow-up consistency
- reduced invoicing delay and faster collection cycle

### Stack
n8n (or similar), CRM, email provider, payment API, Slack/alerts.

### Role relevance
Automation Engineer, Solutions Engineer, AI Operations Consultant.

### Resume bullet draft
Designed and deployed a three-flow automation engine for lead handling, follow-up, and invoicing with escalation logic; reclaimed operator hours weekly and improved process reliability and collection velocity.

---

## Candidate 4 — OpenClaw Runtime Cost Governance Pack

### Employer problem
Agent runtimes become expensive and unstable without explicit cost/performance controls.

### Solution
Implement runtime governance policy with:
- default lightweight model + escalation routing
- provider fallback on rate limits
- cache strategy by model tier
- context pruning and session-load limits
- local heartbeat offload for low-value checks
- token audit cadence + budget alerts

### Deliverables
- before/after cost audit report
- hardened OpenClaw configuration profile
- daily/weekly cost monitoring script and dashboard
- runbook for rate-limit and budget events

### Measurable impact targets
- major reduction in daily spend (target 60–90% depending on baseline)
- stable throughput despite provider limits
- lower average token cost per resolved task

### Stack
OpenClaw config, Ollama local runtime, usage analytics scripts.

### Role relevance
AI Infra Engineer, Platform Reliability Engineer, AI FinOps Engineer.

### Resume bullet draft
Implemented OpenClaw runtime governance (routing, cache policy, context pruning, local heartbeat, token audits) to significantly reduce operating cost while maintaining task throughput and reliability.

---

## Interview STAR/CAR angle (shared)
- **Context:** costly/fragile AI workflows with weak controls.
- **Action:** introduced architecture-level controls, evaluation, and operational governance.
- **Result:** lower cost, higher reliability, and auditable execution aligned with business/regulated requirements.
