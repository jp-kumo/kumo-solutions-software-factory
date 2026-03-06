# Metabase Implementation Guide

Metabase is the **visual analytics and executive dashboard layer**.

## Connect Metabase to
- the same PostgreSQL instance
- the `mission_control` database
- reporting views in `db/migrations/002_reporting_views.sql`

## First dashboards to build

1. Executive Portfolio Dashboard
2. Weekly Review Dashboard
3. Blocked and Due Soon
4. Owner Decision Queue
5. Software Security Posture

## Recommended question sources

Prefer the views:
- `vw_project_summary`
- `vw_blocked_projects`
- `vw_due_soon`
- `vw_owner_decisions`
- `vw_security_posture`
- `vw_portfolio_rollup`
- `vw_weekly_review_snapshot`
