# Appsmith Page Spec — Security Review Queue

## Goal
Show software projects that need security attention or release decisions.

## Widgets
- table of `vw_security_posture`
- filters:
  - release security decision
  - highest open severity
  - review status
- update form for `security_reviews`

## Queries
- `qReadSecurityPosture`
- `qWriteUpdateSecurityReview`
- `qReadSoftwareProjects`

## Acceptance
- software projects appear automatically
- release security decision can be updated
- risk acceptance fields are visible when required
