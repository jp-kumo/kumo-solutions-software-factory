# Appsmith Implementation Guide

Appsmith is the **operational UI layer**.

## Recommended first pages

1. Portfolio Dashboard
2. Projects Registry
3. Project Detail / Edit
4. Weekly Review
5. Decisions Log
6. Security Review Queue

## Data sources to configure

1. PostgreSQL data source pointing to the `mission_control` database
2. Optional read-only PostgreSQL data source for dashboard/reporting queries

## Recommended page order

1. `pages/01-portfolio-dashboard.md`
2. `pages/02-projects-registry.md`
3. `pages/03-project-detail-edit.md`
4. `pages/04-weekly-review.md`
5. `pages/05-decisions-log.md`
6. `pages/06-security-review-queue.md`

## Query conventions

- prefix reads with `qRead`
- prefix writes with `qWrite`
- prefer parameterized queries
- keep write queries small and explicit
- log major state changes through the database, not client-side logic only
