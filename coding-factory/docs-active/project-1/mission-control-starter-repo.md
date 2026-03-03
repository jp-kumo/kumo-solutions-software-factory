# Mission Control Starter Repo

Mission Control is a self-hosted **portfolio and project command center** for all work types, not just software projects.

This starter repo provides a practical v1 foundation built around:

- **PostgreSQL** as the source of truth
- **Appsmith** as the operational UI
- **Metabase** as the analytics/dashboard layer

## Goals of this repo

- Stand up a working local/staging stack quickly
- Provide a durable schema for project, milestone, decision, risk, weekly review, and security tracking
- Give the Coding Factory a concrete starting point for Project #1
- Keep security, governance, and portability in scope from day one

## Repository structure

```text
.
├── appsmith/                 # Page specs, query specs, and import notes
├── config/                   # Project-level configuration and kickoff references
├── db/
│   ├── init/                 # One-time bootstrap SQL for database/users
│   ├── migrations/           # Schema + views
│   ├── seeds/                # Sample data
│   └── queries/              # Handy SQL for operators and dashboards
├── docs/                     # Architecture, security, roadmap, runbook
├── metabase/                 # Dashboard + question specs
├── scripts/                  # Local operator scripts
├── .github/workflows/        # Repo checks
├── docker-compose.yml        # Local/staging stack
└── .env.example              # Required environment variables
```

## Recommended usage

- **Local development / pilot:** use this repo directly
- **Homelab staging:** adapt the compose file, set strong secrets, add reverse proxy/TLS, and configure backups
- **Production-internal:** pin image digests, move secrets to a secret store, front with TLS, and harden network access

## Quick start

1. Copy `.env.example` to `.env` and change secrets.
2. Review `db/init/001-bootstrap.sql` and `db/migrations/001_core_schema.sql`.
3. Start the stack:

   ```bash
   docker compose up -d
   ```

4. Read:
   - `docs/operator-runbook.md`
   - `appsmith/README.md`
   - `metabase/README.md`

5. Build the first pages and dashboards from the specs.

## First pages to implement in Appsmith

1. Portfolio Dashboard
2. Projects Registry
3. Weekly Review
4. Decisions Log
5. Security Review Queue

## First dashboards to implement in Metabase

1. Executive Portfolio Dashboard
2. Weekly Review Dashboard
3. Blocked and Due Soon
4. Owner Decision Queue
5. Software Security Posture

## Security and operations

This repo is a **starter**. Before serious internal production use, you should:

- pin Docker image digests
- front services with TLS
- restrict network access
- use strong secrets
- schedule backups and restore tests
- review OWASP Top 10:2025 / ASVS / API Top 10 / MASVS applicability
- add authentication and access control hardening

See:
- `docs/security-baseline.md`
- `docs/operator-runbook.md`
- `docs/implementation-roadmap.md`
