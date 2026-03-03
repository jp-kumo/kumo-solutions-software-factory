# Slack Workflow Template — Project #1

## Workflow 1: Intake Form
Fields:
- Request title
- Business objective (1 sentence)
- Requested due date
- Risk if delayed
- Affected systems
- Security sensitivity (low/med/high)

Route:
- Post to `#proj-kumo-mission-control-v1-intake`
- Notify Chief of Staff

## Workflow 2: Gate Decision Form
Fields:
- Gate name
- Status (GO / CONDITIONAL GO / NO-GO)
- Evidence links
- Blocking issues
- Owner decision required? (Y/N)

Route:
- Post to `#proj-kumo-mission-control-v1-arch` / `-api` / `-qa` / `-release`
- If NO-GO, escalate to `#agent-control-tower`

## Workflow 3: Security Finding Escalation
Fields:
- Severity (critical/high/medium/low)
- Summary
- Repro/reference
- Proposed remediation
- Target fix date

Route:
- Post to `#proj-kumo-mission-control-v1-incidents`
- Notify Security/Compliance + Chief of Staff
- If critical: block release and notify owner
