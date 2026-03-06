# Appsmith Page Spec — Projects Registry

## Goal
Create and update project records quickly.

## Widgets
- projects table
- create project form
- edit drawer/modal
- status filter
- category filter
- owner filter

## Required fields
- title
- slug
- category
- project_type
- status
- health
- priority
- owner_id
- target_date
- next_action

## Queries
- `qReadProjects`
- `qWriteCreateProject`
- `qWriteUpdateProject`
- `qReadOwners`
- `qReadInitiatives`

## Acceptance
- project create works
- edit updates persist
- invalid required fields are blocked in the form
