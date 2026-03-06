# Dashboard Spec — Security Posture Dashboard

## Purpose
Show current software-project security posture and release risk.

## Cards
- software projects requiring review
- projects with high/critical findings
- projects with `no_go`
- projects with `conditional_go`
- OWASP/ASVS/API/MASVS progress breakdown

## Data sources
- `vw_security_posture`
- `projects`
- `security_reviews`
