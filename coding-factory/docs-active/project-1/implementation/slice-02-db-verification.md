# Slice 02 — DB bootstrap/migration/seed/view verification (Mission Control v1)

Date (UTC): 2026-03-06 19:38 (rerun)

## Scope executed
Project path:
- `/home/jpadmin/.openclaw/workspace/coding-factory/runtime/project-1/mission-control-v1`

Requested scope:
1. Execute DB bootstrap/init from `db/init` and `db/migrations`
2. Apply seeds if safe for local staging
3. Verify required views exist and are queryable

## Execution result summary
Status: **BLOCKED (environment/runtime permissions)**

I could validate that the expected SQL artifacts exist in-repo, but I could not execute PostgreSQL initialization/migration/seed statements in this environment due Docker daemon access restrictions and missing local `psql` client.

## Rerun (2026-03-06 19:37–19:38 UTC)
Commands executed from project root `/home/jpadmin/.openclaw/workspace/coding-factory/runtime/project-1/mission-control-v1`:

```bash
docker compose ps
sudo -n docker compose ps
pg_isready -h localhost -p 5432 -U mission_control_app -d mission_control
```

Observed outputs:
- `docker compose ps` -> permission denied on `/var/run/docker.sock`
- `sudo -n docker compose ps` -> `sudo: a password is required`
- `pg_isready ...` -> `command not found`

Interpretation:
- DB container state cannot be verified from this execution identity.
- Runtime migration/seed/view query checks remain blocked until Docker access is granted (or equivalent privileged operator reruns).

## Evidence

### A) Attempted stack bootstrap
Command:
```bash
docker compose up -d
```
Output:
```text
unable to get image 'metabase/metabase:latest': permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Get "http://%2Fvar%2Frun%2Fdocker.sock/v1.51/images/metabase/metabase:latest/json": dial unix /var/run/docker.sock: connect: permission denied
```

### B) Runtime access diagnostics
Command:
```bash
id && ls -l /var/run/docker.sock
```
Output:
```text
uid=1001(jpadmin) gid=1001(jpadmin) groups=1001(jpadmin),27(sudo),100(users)
srw-rw---- 1 root docker 0 Feb 19 20:24 /var/run/docker.sock
```
Interpretation:
- Active user is **not** in `docker` group
- Docker socket is owned by `root:docker` with group-only access

### C) Local SQL client availability
Command:
```bash
psql --version
```
Output:
```text
/bin/bash: line 1: psql: command not found
```

## SQL artifact presence verification (static)
Verified in migration file `db/migrations/002_reporting_views.sql`:

```text
1:create or replace view vw_project_summary as
24:create or replace view vw_blocked_projects as
29:create or replace view vw_due_soon as
36:create or replace view vw_owner_decisions as
41:create or replace view vw_security_posture as
73:create or replace view vw_weekly_review_snapshot as
```

## Required view queryability check
Required runtime checks:
- `vw_project_summary`
- `vw_blocked_projects`
- `vw_due_soon`
- `vw_owner_decisions`
- `vw_security_posture`
- `vw_weekly_review_snapshot`

Result: **Not executable in this session** due to inability to start/access DB runtime.

## Seed safety note
Seed file `db/seeds/001_sample_seed.sql` is largely idempotent using `ON CONFLICT` / `NOT EXISTS`, but at least one insert (`tasks`) does not include a de-duplication guard and may create duplicates if replayed against an already-seeded database.

## Minimal remediation steps
1. Enable DB runtime access for this execution identity:
   - Add user to docker group: `sudo usermod -aG docker jpadmin`
   - Re-login/new shell to refresh group membership
   - Re-run: `docker compose up -d`
2. (Optional fallback) Install local PostgreSQL client tools if direct `psql` checks are preferred.
3. Re-run verification queries:
   ```sql
   select count(*) from vw_project_summary;
   select count(*) from vw_blocked_projects;
   select count(*) from vw_due_soon;
   select count(*) from vw_owner_decisions;
   select count(*) from vw_security_posture;
   select count(*) from vw_weekly_review_snapshot;
   ```

## Conclusion
Execution of bootstrap/migrations/seeds and runtime queryability verification is currently blocked by host permissions, not SQL definition gaps. All required view definitions are present in the approved v1 migration artifact.