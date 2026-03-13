# Knowledge Capture: 5 Practical AI Governance Portfolio Projects (2026)

## Source
- "5 Practical Projects to Prove You Understand AI Governance (2026 Edition)"
- Author: Taimur Ijlal
- User-provided content snippet (captured from shared message)

---

## Why this matters for Jacques
This is high-signal hiring and consulting positioning content because it shifts from framework literacy to operational proof.

Core message:
- Reading EU AI Act / NIST AI RMF is baseline.
- Differentiation comes from building artifacts that map regulation to practical controls, decisions, and risk communication.

This aligns directly with Kumo Solutions positioning for regulated/high-trust clients.

---

## Portfolio project concepts distilled

## Project 1: AI System Inventory + Risk Classification Engine
### Employer problem
Organizations often cannot answer: "What AI systems are live, who owns them, and what risk tier applies?"

### Build
- Structured inventory for a realistic company (e.g., fintech use cases: credit scoring, fraud detection, chatbot, personalization).
- Include: purpose, owner, data sources, model type, business impact, review cadence, dependencies.
- Add rule-based classifier for EU AI Act risk tiers with rationale output.
- Map each system to NIST AI RMF functions: Govern, Map, Measure, Manage.

### Measurable impact (portfolio proof)
- % systems classified automatically
- time-to-classification reduction
- coverage of mandatory metadata fields

### Stack
- Python/FastAPI + SQLite/Postgres + simple rules engine + dashboard/report output (Markdown/PDF)

### Role relevance
- AI governance analyst, AI risk lead, AI engineer in regulated domains, technical PM

---

## Project 2: AI Risk Assessment + Governance Review Pack
### Employer problem
High-impact AI use cases are launched without structured harm analysis or executive-level decision artifacts.

### Build
- Pick one high-impact use case (e.g., AI CV screening tool).
- Produce formal risk register: harms, likelihood, severity, controls, residual risk.
- Define human oversight checkpoints and deployment gates.
- Write executive governance memo with go/no-go recommendation.

### Measurable impact
- risk control completeness score
- residual risk reduction estimate
- decision cycle time improvement

### Stack
- Markdown templates + YAML/JSON risk schema + scoring script + generated executive brief

### Role relevance
- governance program manager, responsible AI specialist, risk/compliance partner

---

## Project 3: Responsible AI Policy + Operating Model
### Employer problem
Many firms have principles but no operating mechanism to execute and enforce them.

### Build
- Draft Responsible AI policy with enforceable principles (fairness, accountability, transparency, safety, privacy).
- Design intake-to-approval workflow for new AI use cases.
- Define role/RACI model, review cadence, escalation path, and operating controls.
- Include a simple governance operating model diagram that explicitly shows:
  - who owns AI oversight (committee/function),
  - how legal, risk, security, and engineering interact,
  - where approvals and escalations occur.
- Add policy-to-control traceability matrix tied to NIST AI RMF Govern function.

### Measurable impact
- policy control coverage
- approval SLA
- review cadence adherence
- escalation response time target

### Stack
- policy docs + workflow diagrams + operating model/RACI + control matrix + automated checklist generator

### Role relevance
- AI governance architect, AI program lead, GRC-focused AI engineer

---

## Project 4: AI Incident Response + Regulatory Escalation Scenario
### Employer problem
Organizations lack AI-specific crisis playbooks and clear regulatory escalation pathways when model harms surface.

### Build
- Create a realistic failure scenario (e.g., credit scoring system disproportionately disadvantaging a protected group).
- Build a week-by-week incident timeline covering:
  - detection,
  - internal notification chain,
  - triage ownership,
  - legal/regulatory trigger assessment,
  - customer/stakeholder communication,
  - root-cause analysis,
  - model remediation/retraining/revalidation,
  - post-incident control updates.
- Include decision logs and role accountability checkpoints.

### Framework linkage
- Strong alignment to NIST AI RMF Manage function and EU AI Act lifecycle risk expectations.

### Measurable impact
- mean-time-to-detect (MTTD)
- mean-time-to-escalate (MTTE)
- mean-time-to-remediate (MTTR)
- residual risk reduction after corrective actions

### Stack
- incident runbook docs + escalation matrix + timeline artifact + remediation tracker

### Role relevance
- AI risk operations lead, AI governance manager, model risk/compliance roles

---

## Project 5: High-Risk AI Documentation + Conformity Pack (EU AI Act)
### Employer problem
High-risk AI deployments often fail on documentation quality, traceability, and defensibility.

### Build
- Simulate documentation for a high-risk use case (e.g., automated hiring support system).
- Include a concise but structured pack covering:
  - intended purpose and scope,
  - risk management approach,
  - data governance and quality controls,
  - human oversight model,
  - logging/traceability design,
  - ongoing performance monitoring and review plan.
- Keep focus on clarity, structure, and auditability over sheer volume.

### Measurable impact
- documentation completeness score
- traceability coverage across lifecycle controls
- review readiness checklist pass rate

### Stack
- structured templates + control crosswalk + evidence index + conformity checklist

### Role relevance
- regulatory AI governance, model risk, AI assurance/compliance roles
---

## Recruiter-facing differentiation strategy
For each project repo include:
1. Problem statement (business + risk)
2. Framework mapping (EU AI Act / NIST AI RMF)
3. Working artifact/demo
4. Metrics and tradeoffs
5. Executive summary for non-technical stakeholders

This demonstrates both technical execution and governance communication maturity.

---

## Suggested immediate next move for Jacques
Start with Project 1 + Project 2 as a paired portfolio sequence:
- Project 1 proves systems-level governance visibility.
- Project 2 proves decision-quality and executive communication.

Together they create a strong narrative for March 2026 hiring and for Kumo consulting offers in regulated environments.
