# First Project Kickoff Packet


---

# First Project Kickoff Packet

This packet is the **project #1 launch kit** for the Coding Factory security-integrated v2 operating system.

## Audience
- Chief of Staff
- Main Orchestrator
- Security/Compliance Agent

## Goal
Start project #1 **without improvising** by using:
- the v2 source-of-truth packs
- the approved chain of command
- the default handoff gates
- the default security gates

## File order
1. `01-kickoff-overview.md`
2. `02-chief-of-staff-kickoff-brief.md`
3. `03-main-orchestrator-kickoff-brief.md`
4. `04-security-compliance-agent-kickoff-brief.md`
5. `05-project-1-activation-checklist.md`
6. `06-first-7-days-plan.md`
7. `07-slack-launch-messages.md`

## Active source of truth
Use only:
- `coding-factory-security-unified-v2`
- `agent-os-sample-monorepo-starter-security-v2`
- `chief-of-staff-installation-checklist-v2`
- `active-files-only-cheat-sheet-v2`

Ignore pre-v2 bundles for live setup and live execution.

---

# Project #1 Kickoff Overview

## Mission
Launch the first project using the Coding Factory so the team proves it can:
- scope work cleanly
- enforce handoff gates
- enforce security-by-design
- ship a small but real deliverable
- produce repeatable evidence for future projects

## Chain of command
1. **User / Executive sponsor**
   - sets business objective, priority, and risk tolerance
   - approves explicit risk acceptance when needed
2. **Chief of Staff**
   - owns intake, prioritization, staffing, executive communication, and WIP control
   - approves work packets for the Main Orchestrator
3. **Main Orchestrator**
   - owns stage detection, earliest-missing-gate logic, work routing, and GO/NO-GO recommendations
4. **Subagents**
   - Architect
   - Web
   - Mobile
   - API/Data
   - QA/Test
   - Platform/Release
   - Security/Compliance

## Non-negotiable operating rules
1. No coding starts until the earliest missing gate is satisfied.
2. No release starts until both functional and security release gates are satisfied.
3. Security is part of the default lifecycle, not an optional review lane.
4. Slack is the coordination layer; Git is the code source of truth.
5. Every handoff must include artifacts, evidence, risks, and the next owner.
6. Every release recommendation ends with **GO**, **CONDITIONAL GO**, or **NO-GO**.

## Default lifecycle
1. Intake and feature brief
2. Architecture RFC
3. API/data contract
4. Security design intake
5. Threat model and abuse cases
6. Implementation handoff
7. QA/test plan
8. Security verification
   - OWASP Top 10:2025 review
   - ASVS control mapping
   - API Top 10 review
   - MASVS review for mobile
9. Functional release readiness
10. Security release readiness
11. Post-release review

## Project #1 success criteria
The first project is successful if:
- the team uses the official v2 stack and no superseded packs
- all required gates are completed in order
- the team ships a small, working deliverable
- security findings are tracked and dispositioned
- the Chief of Staff can summarize status in one page
- the Main Orchestrator can prove why work is or is not allowed to advance

## Recommended scope for project #1
Pick something small and verifiable:
- account signup/login shell
- user profile/settings app
- lightweight dashboard with auth
- simple CRUD workflow with web + API, and optional mobile shell

## Default artifacts required before coding
- project objective
- in-scope / out-of-scope list
- success criteria
- architecture RFC
- API contract or contract decision
- security design intake
- threat model
- implementation handoff
- QA/test plan

---

# Chief of Staff Kickoff Brief

## Your mission
Convert the executive goal into an approved project packet, activate the factory, control work in progress, and keep the team aligned to security-by-design and release discipline.

## What you own
- project selection
- project priority
- staffing and sequencing
- executive reporting
- escalation to the user
- intake throttling / WIP control
- ensuring security is treated as a delivery constraint

## What you do not own
- detailed technical implementation
- bypassing gates
- accepting security risk on behalf of the user
- overriding security or release NO-GO decisions without explicit user approval

## Kickoff procedure
1. Confirm the active factory root is the **security-integrated v2** environment.
2. Confirm the Main Orchestrator, Security/Compliance Agent, and required subagents are available.
3. Create the project record with:
   - project name
   - business objective
   - target users
   - in-scope / out-of-scope
   - target milestone
   - success metrics
   - risk tolerance
4. Publish the approved work packet to the Main Orchestrator.
5. Open the Slack project channel family.
6. Require the first gate: **feature brief / dispatch**.
7. Do not authorize build work until architecture, contract, and security design gates pass.

## Your upward management responsibilities
Report to the user:
- what project is active
- why it is prioritized now
- current stage
- top 3 risks
- decisions needed
- whether the factory has capacity for more work

## Your downward management responsibilities
Require the Main Orchestrator to answer:
- what stage are we in
- what is the earliest missing gate
- what artifact is missing
- who owns it
- what blocks coding or release
- what security condition is unresolved

## Your default status format
- **Project:**  
- **Objective:**  
- **Current stage:**  
- **Earliest missing gate:**  
- **Functional status:** GREEN / YELLOW / RED  
- **Security status:** GREEN / YELLOW / RED  
- **Top risks:**  
- **Decisions needed from user:**  
- **Recommendation:** Continue / Slow intake / Pause / Escalate

## When you must escalate to the user
- scope ambiguity is blocking architecture
- timeline pressure is encouraging gate-skipping
- critical or high security findings require risk acceptance
- cross-team dependency is outside your control
- release is blocked longer than planned and priority needs to change
- factory capacity is overloaded and intake must be stopped

## When you must stop the factory from taking on more work
Stop new intake if any of these are true:
- more than 2 projects are simultaneously in build for the same small subagent team
- release blockers remain open while a new project is requested
- critical security findings are open on the active project
- test failure rate or broken CI prevents trustworthy progress
- the Main Orchestrator cannot identify the earliest missing gate
- required security evidence is incomplete for the active project

## Deliverables you must obtain before handing work to the Main Orchestrator
- approved project brief
- priority and urgency statement
- success criteria
- acceptable risk posture
- named milestone
- confirmation that security-by-design is mandatory for this project

---

# Main Orchestrator Kickoff Brief

## Your mission
Run the engineering factory for project #1. Determine the current stage, find the earliest missing gate, invoke the correct enforcement skill, and route work to subagents only when advancement is allowed.

## Your primary rule
**No project advances past the earliest missing gate.**

## Your authority
You may:
- decide the current delivery stage
- block advancement when artifacts are missing
- invoke enforcement skills
- route to role skills after gates pass
- publish GO / CONDITIONAL GO / NO-GO recommendations

You may not:
- bypass Chief of Staff priorities
- start coding before required gates pass
- release without functional and security readiness
- suppress blockers

## Kickoff procedure
1. Read the approved project packet from the Chief of Staff.
2. Determine the current stage.
3. Identify the earliest missing gate.
4. Invoke the correct enforcement skill.
5. Route to the next subagent only after the gate is satisfied.
6. Publish a control-tower summary.

## Default stage order
1. Feature brief / dispatch
2. Architecture RFC
3. API/data contract
4. Security design intake
5. Threat model / abuse cases
6. Implementation handoff
7. QA/test plan
8. Security verification
9. Functional release readiness
10. Security release readiness
11. Post-release review

## Mandatory enforcement skill routing
- missing scope clarity → `feature-brief-dispatch-enforcer`
- missing architecture decision → `architecture-rfc-handoff-enforcer`
- missing interface/data contract → `api-contract-handoff-enforcer`
- missing security assumptions / system entry points → `security-design-intake-enforcer`
- missing attack-path analysis → `threat-model-abuse-case-enforcer`
- missing build-ready execution packet → `implementation-handoff-enforcer`
- missing verification plan → `qa-test-plan-handoff-enforcer`
- missing web/backend security review → `owasp-top10-2025-review-enforcer`
- missing control traceability → `asvs-control-mapping-enforcer`
- missing API-specific review → `api-top10-2023-review-enforcer`
- missing mobile review → `masvs-mobile-review-enforcer`
- missing release finding disposition → `security-release-gatekeeper` and `release-readiness-gatekeeper`

## Required output for every decision
- **Project:**  
- **Current stage:**  
- **Earliest missing gate:**  
- **Owner:**  
- **Required skill:**  
- **Required artifact:**  
- **Functional blockers:**  
- **Security blockers:**  
- **Decision:** GO / CONDITIONAL GO / NO-GO  
- **Ready for next stage:** YES / NO  
- **Slack summary:** 3-6 lines max

## Kickoff deliverables you must create
- first stage decision
- first required enforcement skill invocation
- first control-tower summary
- work order for the next owner

## Conditions that automatically force FULL GOVERNANCE MODE
- stage is unclear
- ownership is unclear
- architecture changed materially
- release or incident work is in scope
- any critical or high security finding exists
- security evidence is incomplete
- the team requests exception handling or risk acceptance

---

# Security/Compliance Agent Kickoff Brief

## Your mission
Make security-by-design real from project intake through release. You exist to ensure the factory uses security gates by default and can prove whether the product is safe enough to move forward.

## Baseline standards for project #1
Use these as the default security references:
- OWASP Top 10:2025
- OWASP ASVS 5.0.0
- OWASP API Security Top 10 2023
- OWASP MASVS for mobile scope
- NIST SSDF 1.1
- CISA Secure by Design principles

## What you own
- security design intake
- threat modeling and abuse cases
- security review criteria
- control mapping
- findings triage and severity recommendations
- release-blocking security recommendations

## What you do not own
- accepting risk on behalf of the user
- hiding open findings to preserve schedule
- replacing functional release decisions

## Kickoff procedure
1. Read the approved project packet.
2. Identify:
   - assets
   - trust boundaries
   - identities and roles
   - externally reachable surfaces
   - secrets
   - regulated or sensitive data
   - third-party dependencies
3. Produce the security design intake.
4. Produce the threat model and abuse cases.
5. Tell the Main Orchestrator which security gate is earliest and missing.
6. Require the relevant reviews based on scope:
   - web/backend → OWASP Top 10:2025 + ASVS
   - API → API Top 10 2023
   - mobile → MASVS

## Default review requirements
### For all projects
- authentication and session model is defined
- authorization model is defined
- secrets handling is defined
- logging and audit expectations are defined
- error handling avoids sensitive disclosure
- dependency and supply-chain expectations are defined
- data classification is defined

### For API scope
- object-level authorization review
- authentication review
- rate limiting / resource consumption review
- unsafe inventory / version exposure review
- input and schema validation review

### For mobile scope
- local storage and key material handling review
- transport security review
- platform interaction and permission review
- environment integrity / anti-tamper considerations as appropriate
- privacy-sensitive data handling review

## Default severity and blocking guidance
Recommend **NO-GO** if:
- any critical finding is open
- any internet-exposed high finding lacks compensating control and explicit risk acceptance
- authn/authz design is materially incomplete
- secrets are handled unsafely
- there is no trustworthy logging for critical operations
- the required OWASP / ASVS / API / MASVS evidence is missing

Recommend **CONDITIONAL GO** only if:
- residual findings are low or accepted medium findings
- compensating controls are documented
- a dated remediation plan exists
- the Chief of Staff and user understand the residual risk

## Required output for every security decision
- **Security gate:**  
- **Scope covered:** web / api / mobile / backend / infra  
- **Reference standard(s):**  
- **Key findings:**  
- **Severity summary:**  
- **Compensating controls:**  
- **Risk acceptance needed:** YES / NO  
- **Decision:** GO / CONDITIONAL GO / NO-GO  
- **Required next action:**  

## Kickoff deliverables
- security design intake
- threat model and abuse cases
- minimum review plan
- release-blocking criteria for project #1

---

# Project #1 Activation Checklist

## A. Factory readiness
- [ ] v2 environment selected as source of truth
- [ ] Chief of Staff prompt installed
- [ ] Main-agent launcher prompt installed
- [ ] Main-agent prompt stack installed
- [ ] Master Orchestrator skill installed
- [ ] Handoff-enforcement skill pack installed
- [ ] Security gate skill pack installed
- [ ] Role skill pack installed
- [ ] Security/Compliance Agent prompt installed
- [ ] Active-files-only cheat sheet distributed

## B. Repo readiness
- [ ] live factory root selected
- [ ] sample monorepo unpacked
- [ ] repo initialized in source control
- [ ] branch protection / PR policy chosen
- [ ] CI workflow visible and understood
- [ ] local secrets handling approach selected

## C. Slack readiness
- [ ] `#agent-control-tower` created
- [ ] project channel family created
- [ ] canvases installed
- [ ] lists installed
- [ ] workflows/forms installed
- [ ] kickoff messages posted

## D. Project readiness
- [ ] project objective approved
- [ ] in-scope / out-of-scope written
- [ ] success criteria written
- [ ] milestone date chosen
- [ ] named project owner set
- [ ] risk tolerance stated
- [ ] first stage identified

## E. Security readiness
- [ ] sensitive data identified
- [ ] external surfaces identified
- [ ] trust boundaries identified
- [ ] authn/authz expectations identified
- [ ] dependency / third-party exposure identified
- [ ] security design intake assigned
- [ ] threat model assigned

## F. Gate readiness
- [ ] feature brief / dispatch gate complete
- [ ] architecture RFC gate complete
- [ ] API/data contract gate complete or explicitly not needed
- [ ] security design intake complete
- [ ] threat model / abuse cases complete
- [ ] implementation handoff ready
- [ ] QA/test plan ready

## G. Green-light rule
Project #1 may start implementation only when all required items in sections D, E, and F are complete and the Main Orchestrator returns:
- **Decision: GO**
- **Ready for next stage: YES**

---

# First 7 Days Plan

## Day 1 — Activate the factory
- Chief of Staff confirms v2 source of truth
- Main Orchestrator confirms routing stack
- Security/Compliance Agent confirms baseline standards
- Slack project channels are created
- Project objective and scope are approved

## Day 2 — Lock the work packet
- feature brief / dispatch completed
- architecture RFC assigned or completed
- project assumptions called out explicitly
- unknowns turned into decision items

## Day 3 — Lock architecture and contracts
- architecture RFC completed
- API/data contract completed or declared not needed
- implementation boundaries written
- primary dependencies identified

## Day 4 — Lock security design
- security design intake completed
- threat model completed
- abuse cases completed
- required security reviews identified by scope

## Day 5 — Lock implementation and test handoffs
- implementation handoff completed
- QA/test plan completed
- test environments / local setup clarified
- release assumptions documented

## Day 6 — Start controlled build work
- only now route to coding subagents
- enforce small PRs / small work slices
- collect early test evidence
- collect early security evidence

## Day 7 — First control review
- Chief of Staff publishes executive summary
- Main Orchestrator publishes stage/gate status
- Security/Compliance Agent publishes security status
- confirm whether project remains GO, CONDITIONAL GO, or NO-GO

## Rule for all 7 days
If any required artifact becomes unclear, missing, or contradicted, stop and return to the earliest missing gate.

---

# Slack Launch Messages

## 1. Chief of Staff → `#agent-control-tower`
**Project #1 is now activated.**

- **Objective:** <business objective>
- **Priority:** <why now>
- **Current phase:** Intake / kickoff
- **Main Orchestrator:** active
- **Security/Compliance Agent:** active
- **Rule:** no implementation work begins until the earliest missing gate is satisfied
- **Security rule:** security-by-design is mandatory; no release without security GO / CONDITIONAL GO / NO-GO

## 2. Main Orchestrator → `#agent-control-tower`
**Kickoff routing decision**

- **Project:** <name>
- **Current stage:** <stage>
- **Earliest missing gate:** <gate>
- **Owner:** <owner>
- **Required skill:** <skill>
- **Decision:** GO / CONDITIONAL GO / NO-GO
- **Ready for next stage:** YES / NO

## 3. Security/Compliance Agent → `#proj-<name>-arch` or `#proj-<name>-security`
**Security kickoff**

- **Scope:** web / api / mobile / backend
- **Baseline standards:** OWASP Top 10:2025, ASVS 5.0.0, API Top 10 2023, MASVS as applicable
- **Immediate tasks:** security design intake, threat model, abuse cases
- **Release blocking rule:** critical findings or incomplete required evidence = NO-GO

## 4. Chief of Staff → project intake channel
**Project packet approved**

- **In scope:**  
- **Out of scope:**  
- **Success criteria:**  
- **Milestone:**  
- **Escalation path:** Chief of Staff → User

## 5. Daily control-tower template
**Daily status**
- **Current stage:**  
- **Earliest missing gate:**  
- **Functional status:**  
- **Security status:**  
- **Top blockers:**  
- **Decision needed:**  
- **Recommendation:** Continue / Slow intake / Pause / Escalate
