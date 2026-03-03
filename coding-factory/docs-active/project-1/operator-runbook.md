# Operator Runbook — Mission Control v1 (Project #1)

## 1) First-time setup

```bash
cp .env.example .env
# edit .env with non-default secrets

docker compose up -d
docker compose ps
```

## 2) Initial verification

- PostgreSQL is healthy
- Appsmith reachable at `http://localhost:8080`
- Metabase reachable at `http://localhost:3000`

## 3) Backup

```bash
./scripts/backup-postgres.sh
```

Backups are written to `./backups/`.

## 4) Restore

```bash
./scripts/restore-postgres.sh backups/<file>.sql.gz
```

## 5) Common local operations

```bash
make up
make down
make logs
make ps
make validate
```

## 6) Before first internal release

- Change all default secrets
- Add TLS/reverse proxy
- Restrict network access
- Run security gate review
- Confirm restore from backup
- Review dashboards and Appsmith pages for least-privilege access

## 7) Gate reminder (non-negotiable)
No coding/release progression if earliest missing gate is incomplete.
