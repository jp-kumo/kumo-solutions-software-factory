# Appsmith Page Spec — Portfolio Dashboard

## Goal
Give the owner and Chief of Staff a one-screen operational view of the portfolio.

## Widgets
- KPI cards:
  - active projects
  - blocked projects
  - due in 30 days
  - owner decisions needed
- table: `vw_project_summary`
- filter controls:
  - category
  - status
  - health
  - priority
- quick links:
  - Projects Registry
  - Weekly Review
  - Security Queue

## Queries
- `qReadPortfolioCounts`
- `qReadProjectSummary`
- `qReadBlockedProjects`
- `qReadOwnerDecisions`

## Acceptance
- filters update the summary table
- clicking a project row opens Project Detail page
- cards reflect the current database state
