# Mission Control v1 Architecture

## High-level design

```text
Users / Agents
    |
    v
Appsmith (operational UI)
    |
    +----> PostgreSQL (system of record)
    |
    v
Metabase (dashboards + analytics)
```

## Why this shape

- PostgreSQL holds the canonical data model.
- Appsmith handles create/update workflows and weekly operations.
- Metabase handles visual portfolio dashboards and trend/reporting views.

## Environments

- **local-dev**: single-host Docker Compose
- **staging-internal**: one VM or homelab node, TLS, stronger secrets
- **production-internal**: hardened network, pinned images, monitored backups, restore tests

## Future additions

- reverse proxy with TLS
- SSO
- internal API for automation and agent write-backs
- audit logging enrichment
- custom front end only if workflow needs outgrow Appsmith
