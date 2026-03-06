# Operator Runbook

## 1. First-time setup

```bash
cp .env.example .env
# edit .env
docker compose up -d
docker compose ps
```

## 2. Initial verification

- PostgreSQL healthy
- Appsmith reachable on `http://localhost:8080`
- Metabase reachable on `http://localhost:3000`

## 3. Backup

```bash
./scripts/backup-postgres.sh
```

Backups are written to `./backups/`.

## 4. Restore

```bash
./scripts/restore-postgres.sh backups/<file>.sql.gz
```

## 5. Common local operations

```bash
make up
make down
make logs
make ps
make validate
```

## 6. Before the first internal release

- change all default secrets
- add TLS/reverse proxy
- restrict network access
- run security gate review
- confirm restore from backup
- review dashboards and Appsmith pages for least-privilege access
