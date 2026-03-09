# Unified AI Governance Controls Matrix (Portfolio Mapping)

**Date:** 2026-03-09  
**Purpose:** Consolidate governance/security/compliance controls from recent CSA research captures and map them directly to Jacques’s portfolio projects, interview narratives, and implementation actions.

---

## 1) Control Domains (Unified)

## A. Governance & Accountability
- Define AI ownership model (RACI: Responsible/Accountable/Consulted/Informed).
- Document intended use, decision authority, and escalation boundaries.
- Maintain policy-aligned approval gates for model/tool changes.

## B. Risk & Lifecycle Assurance
- Apply lifecycle risk checkpoints (design → build → validate → deploy → monitor).
- Use business-context risk scoring (not one-size-fits-all templates).
- Require rollback/disable (“kill switch”) path for unsafe behavior.

## C. Secure Development (LLM/GenAI)
- Security-by-design and privacy-by-design in app architecture.
- Threat modeling and regular vulnerability assessments.
- Security scans + CI/CD gates before release.

## D. Data & Privacy Controls
- Data classification, minimization, and retention controls.
- Access controls for model/data/API layers (RBAC/ABAC/CBAC where applicable).
- Traceability of data sources, transformation lineage, and quality checks.

## E. Model Safety & Reliability
- Prompt injection defenses and input sanitization.
- Output guardrails + human-in-the-loop review for risky outputs.
- Evaluation harnesses for quality, bias, and robustness.

## F. Monitoring, Incident Response, and Reporting
- Real-time monitoring for drift, performance degradation, and anomalies.
- Alerting thresholds + documented incident workflows.
- Remediation SLAs and post-incident evidence tracking.

## G. Third-Party / Supply Chain Risk
- Vendor due diligence for AI tool providers.
- Dependency and software composition risk visibility.
- Contractual and operational controls for external model/services usage.

## H. Standards & Regulatory Alignment
- Map controls to applicable frameworks and regulations (e.g., NIST AI RMF, ISO 27001, GDPR/CCPA, sector-specific requirements).
- Treat compliance as baseline; maintain beyond-compliance risk posture.

---

## 2) Portfolio Project Mapping

## Project A — Production RAG Support Assistant
**Primary controls to demonstrate:**
- E (Safety/Reliability), D (Data/Privacy), F (Monitoring), C (Secure Development), B (Lifecycle Risk)

**Concrete evidence artifacts:**
- Retrieval eval report (relevance/citation coverage/hallucination rate)
- Prompt-injection test cases + mitigations
- Output safety policy and HITL review procedure
- Monitoring dashboard screenshots (latency/quality/cost)
- Change log + rollback procedure

## Project B — AI Workflow Automation (Lead-to-Action Ops)
**Primary controls to demonstrate:**
- A (Governance), B (Risk/Lifecycle), D (Data Controls), F (Monitoring), G (Third-Party Risk)

**Concrete evidence artifacts:**
- Decision-rights matrix (who approves automation actions)
- Human override + escalation SOP
- Data handling and retention map for inbound records
- SLA monitoring and exception report snapshots
- Vendor/API dependency risk register

## Project C — Mission Control Governance & Reliability Layer
**Primary controls to demonstrate:**
- A (Governance), B (Risk/Lifecycle), H (Standards alignment), F (Monitoring)

**Concrete evidence artifacts:**
- Baseline/regression-gate report output examples
- Requirement-gap trend history snapshots
- CI fail-on-regression behavior proof
- Governance debt prioritization report

---

## 3) Interview Story Mapping (Quick Use)

## Story 1: “How did you make AI safe for production?”
- Mention: injection defenses, output guardrails, HITL review, drift monitoring, rollback path.

## Story 2: “How do you operationalize governance?”
- Mention: RACI ownership, release gates, regression checks, audit-ready artifacts.

## Story 3: “How do you handle AI vendor/supply-chain risk?”
- Mention: due diligence criteria, dependency visibility, policy constraints, monitoring obligations.

## Story 4: “How do you prove business value while staying compliant?”
- Mention: response/SLA improvements, reliability metrics, incident reduction, documented controls.

---

## 4) 30-Day Implementation Checklist

### Week 1 — Baseline
- [ ] Create AI control inventory template (by control domain).
- [ ] Define RACI for each active AI workflow.
- [ ] Define risk classification rubric.

### Week 2 — Technical Controls
- [ ] Add prompt-input sanitization and output policy checks.
- [ ] Add CI security checks and release gates.
- [ ] Add monitoring metrics (quality/latency/drift/incidents).

### Week 3 — Evidence & Compliance
- [ ] Publish control-to-evidence map for each portfolio project.
- [ ] Draft incident response and rollback SOP.
- [ ] Create vendor risk checklist for AI dependencies.

### Week 4 — Presentation & Hiring Packaging
- [ ] Update one-pagers with control evidence.
- [ ] Add governance section to portfolio landing page.
- [ ] Prepare interview STAR stories mapped to control domains.

---

## 5) Suggested Resume/LinkedIn Language
- “Implemented lifecycle-based AI governance controls with measurable reliability and compliance evidence.”
- “Designed and operationalized AI safety guardrails (injection defense, output controls, HITL) for production workflows.”
- “Built change-aware governance automation with regression gates and trend-based risk visibility.”

---

## 6) Practical Principle
**Compliance is the floor, not the ceiling.**  
Use governance controls to increase trust, speed up approvals, and improve delivery reliability—not just to pass audits.
