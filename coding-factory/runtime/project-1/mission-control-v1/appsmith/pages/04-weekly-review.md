# Appsmith Page Spec — Weekly Review

## Goal
Support the Chief of Staff's weekly portfolio review.

## Widgets
- current week review form
- snapshot table for `vw_weekly_review_snapshot`
- embedded list of blocked projects
- embedded list of owner decisions needed

## Queries
- `qReadCurrentWeekReview`
- `qWriteUpsertWeeklyReview`
- `qReadBlockedProjects`
- `qReadOwnerDecisions`

## Acceptance
- one review per week
- edit overwrites the current week entry cleanly
