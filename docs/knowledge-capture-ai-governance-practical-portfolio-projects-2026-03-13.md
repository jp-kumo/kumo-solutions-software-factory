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
- Define role/RACI model, review cadence, escalation path, incident handling.
- Add policy-to-control traceability matrix.

### Measurable impact
- policy control coverage
- approval SLA
- incident escalation response time target

### Stack
- policy docs + workflow diagrams + control matrix + automated checklist generator

### Role relevance
- AI governance architect, AI program lead, GRC-focused AI engineer

---

## Project 4 (recommended extension): Continuous AI Control Monitoring
### Employer problem
Controls are documented once but not continuously monitored after deployment.

### Build
- Implement recurring checks for model drift, data quality drift, explainability availability, and human-override logging.
- Build daily/weekly compliance status dashboard.
- Add alerting and exception register.

### Measurable impact
- control pass-rate trend
- mean-time-to-detect control failures
- unresolved control exceptions aging

### Stack
- Python jobs + SQL + Grafana/Metabase + alert hooks (Slack/Telegram)

### Role relevance
- MLOps + governance hybrid, platform risk engineer

---

## Project 5 (recommended extension): Third-Party AI Vendor Governance Pack
### Employer problem
Enterprises increasingly consume vendor AI without standard due diligence.

### Build
- Vendor assessment questionnaire mapped to EU AI Act + NIST AI RMF controls.
- Scorecard and approval rubric.
- Standard contract addendum checklist (auditability, transparency, incident notification, data boundaries).

### Measurable impact
- due-diligence cycle time
- vendor risk scoring consistency
- % vendors passing minimum governance bar

### Stack
- structured forms + scoring engine + report generator

### Role relevance
- procurement risk, security governance, AI strategy roles

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
