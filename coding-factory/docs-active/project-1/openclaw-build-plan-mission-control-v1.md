# OpenClaw Build Plan for Mission Control v1

## Goal
Use the Coding Factory to deliver Mission Control as Project #1.

## Routing model
1. Chief of Staff defines scope
2. Main Orchestrator controls gates
3. Security / Compliance Agent enforces security gates
4. Web / API / QA / Platform subagents implement

## Required kickoff sequence
1. feature brief
2. architecture RFC
3. API / data contract handoff
4. implementation handoff
5. QA and security plan
6. release readiness

## Suggested role assignments
- Chief of Staff: scope, schedule, reporting
- Main Orchestrator: stage routing and gate enforcement
- Architect Agent: data model and solution design
- Web Agent: Appsmith page plan and later custom web UI if needed
- API / Data Agent: PostgreSQL schema and DB views
- QA Agent: test plan for forms, dashboards, and access flows
- Platform Agent: docker compose, backups, deployment
- Security Agent: OWASP / ASVS / API / MASVS applicability and GO / NO-GO

## Build order
1. Schema and seed data
2. Appsmith CRUD
3. Metabase dashboards
4. Security review workflow
5. Weekly review workflow
6. Agent write-back and automations later

## Project risks
- trying to overbuild v1
- too many fields too early
- treating it like a public product before internal value is proven
