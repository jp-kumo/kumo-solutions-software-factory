# Mission Control v1 Product Spec

## Product name
Mission Control

## Product vision
Mission Control is a self-hosted portfolio dashboard that lets the owner see **all active and proposed work in one place** and understand:
- what exists
- what matters most
- what is blocked
- what needs a decision
- which projects are healthy or unhealthy
- which agent teams are overloaded
- whether releases are security-ready

## Problem statement
The current work environment spans multiple project types:
- software products
- business initiatives
- learning / certification plans
- content projects
- operations / admin work
- personal strategic projects

These work streams do not belong in a single software-only tool, but they still need:
- shared visibility
- prioritization
- milestones
- status
- health
- decision logging
- weekly review structure

## Primary users
1. Owner
2. Chief of Staff
3. Main Orchestrator
4. Security / Compliance Agent

## Secondary users
1. Specialist subagents
2. Future human collaborators

## Core jobs to be done
1. See all projects by priority and health
2. Review what changed this week
3. Identify blockers and overdue items
4. Find projects that need owner decisions
5. Track milestones and deadlines
6. Track project security posture for software work
7. See portfolio balance across categories

## Success criteria for v1
1. The owner can review all current projects in under 10 minutes
2. Every active project has:
   - status
   - priority
   - owner
   - next milestone
   - next action
3. Every software project has:
   - security review status
   - release readiness status
4. The Chief of Staff can run a weekly review from the system
5. The system supports at least 25-50 projects without confusion

## Non-goals for v1
- no external customer access
- no fine-grained time tracking
- no complex portfolio finance module
- no custom RBAC beyond simple internal roles
- no advanced AI chat interface inside the product

## Functional requirements

### FR-1 Portfolio dashboard
Display:
- active project count
- projects by status
- projects by category
- projects by health
- blocked projects
- due in next 7 / 30 days
- waiting-for-owner-decision count

### FR-2 Project registry
Each project record must support:
- title
- slug
- description
- category
- type
- status
- health
- priority
- owner
- sponsor
- strategic value
- effort estimate
- start date
- target date
- next milestone
- next action
- project notes
- risk summary

### FR-3 Views
Provide at minimum:
- all projects table
- kanban by status
- calendar / milestone view
- my priorities this week
- blocked view
- owner decision queue
- software projects security view

### FR-4 Decisions
Track decisions with:
- date
- summary
- rationale
- decider
- affected project
- follow-up action

### FR-5 Weekly review
Track:
- weekly top priorities
- what moved
- what is stuck
- what needs escalation
- what should stop

### FR-6 Security tracking
For software projects, capture:
- security review required yes/no
- OWASP Top 10 review status
- ASVS mapping status
- API Top 10 review status
- MASVS review status when mobile applies
- release security GO / NO-GO

### FR-7 Auditability
Log major status changes and critical decisions.

## Non-functional requirements
- self-hosted
- durable, boring stack
- simple backup strategy
- easy to inspect
- easy to extend
- low monthly operating cost
- acceptable performance on homelab-class hardware

## v1 acceptance test
Mission Control v1 is complete when:
1. The owner can add and update projects
2. The owner can see a dashboard with health, status, and deadlines
3. The Chief of Staff can run a weekly review workflow
4. Software projects show security and release readiness
5. The system is backed by PostgreSQL and can be backed up predictably
