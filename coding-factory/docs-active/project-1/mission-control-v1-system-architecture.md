# Mission Control v1 System Architecture

## High-level architecture

```text
Users / Agents
    |
    v
Appsmith (operational UI)
    |
    +----> PostgreSQL (primary application database)
    |
    +----> optional internal API later
    |
    v
Metabase (analytics and dashboards)
    |
    v
PostgreSQL (read-only analytics queries against same source data or reporting views)
```

## Components

### 1. PostgreSQL
System of record for:
- projects
- milestones
- decisions
- tasks
- risks
- weekly reviews
- security reviews

### 2. Appsmith
Operational interface for:
- create / update projects
- move project statuses
- record weekly review outcomes
- log decisions
- maintain security and release metadata

### 3. Metabase
Dashboard layer for:
- executive dashboards
- weekly portfolio review
- due date and aging dashboards
- health heatmaps
- security posture summary

## Deployment shape for v1
Single host or small homelab VM:
- PostgreSQL container
- Appsmith container
- Metabase container
- reverse proxy optional
- daily backup job

## Recommended environments
- local-dev
- staging
- production-internal

## Data ownership
- Appsmith writes to PostgreSQL
- Metabase primarily reads from PostgreSQL
- owner and Chief of Staff are primary operators
- agents may update records through controlled Appsmith pages or later through APIs

## Future extensions
- internal API service for automation
- SSO
- webhook integration
- OpenClaw write-backs
- richer role-based access control
