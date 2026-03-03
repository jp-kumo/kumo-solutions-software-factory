# Mission Control v1 Data Model

## Core entities
1. initiatives
2. projects
3. milestones
4. tasks
5. decisions
6. risks
7. weekly_reviews
8. security_reviews
9. owners

## Entity summaries

### initiatives
A top-level strategic bucket.

Fields:
- id
- name
- description
- status
- target_quarter

### projects
The main unit of management.

Fields:
- id
- initiative_id
- title
- slug
- description
- category
- project_type
- status
- health
- priority
- owner_id
- sponsor
- strategic_value
- effort_size
- start_date
- target_date
- next_action
- next_action_due
- owner_decision_needed
- software_security_required
- release_readiness_status
- created_at
- updated_at

### milestones
Project-specific milestone tracking.

### tasks
A lightweight project action table for v1.

### decisions
Captures important portfolio and project decisions.

### risks
Tracks project risk items.

### weekly_reviews
Stores the weekly review record and summary.

### security_reviews
Stores security gate results for software projects.

## Important design choices
1. Keep tasking lightweight in v1
2. Treat projects as the main reporting entity
3. Store security as structured metadata, not freeform notes
4. Use enums or constrained text values for status, health, priority, category
5. Add SQL views for dashboards rather than denormalizing too early

## Reporting views to create
- vw_project_summary
- vw_blocked_projects
- vw_due_soon
- vw_owner_decisions
- vw_security_posture
- vw_weekly_review_snapshot
