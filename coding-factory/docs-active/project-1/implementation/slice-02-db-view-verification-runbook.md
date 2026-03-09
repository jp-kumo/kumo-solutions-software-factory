# Slice 02 — DB Reporting View Verification Runbook

## Purpose
Provide a repeatable runtime check that required reporting views exist and are queryable on the active Mission Control database.

## Scripts
- `runtime/project-1/mission-control-v1/scripts/verify_reporting_views.py`
- `runtime/project-1/mission-control-v1/scripts/run_db_view_check.sh` (scheduled/CI wrapper)

## Required views checked
- `vw_project_summary`
- `vw_blocked_projects`
- `vw_due_soon`
- `vw_owner_decisions`
- `vw_security_posture`
- `vw_weekly_review_snapshot`

## Example commands
```bash
cd /home/jpadmin/.openclaw/workspace/coding-factory/runtime/project-1/mission-control-v1
python3 scripts/verify_reporting_views.py \
  --dsn postgresql://postgres:postgres@localhost:15432/mission_control \
  --out-json /home/jpadmin/.openclaw/workspace/data/reports/mission-control-db-view-check.json
```

Wrapper (recommended for automation):
```bash
bash /home/jpadmin/.openclaw/workspace/coding-factory/runtime/project-1/mission-control-v1/scripts/run_db_view_check.sh
```

## Exit codes
- `0` all required views exist and are queryable
- `1` one or more views missing/unqueryable
- `2` invalid invocation (e.g., missing DSN)

## Output
JSON report with:
- `ok` overall status
- per-view `exists`, `queryable`, `row_count`, and `error`
- generation timestamp

Wrapper output behavior:
- writes timestamped report: `data/reports/mission-control-db-view-check-<timestamp>.json`
- updates `data/reports/mission-control-db-view-check-latest.json`

## CI/Nightly Gate
- GitHub Actions workflow added: `.github/workflows/project1-db-view-check.yml`
- Requires secret: `PROJECT1_DB_VIEW_CHECK_DSN`
- Any missing/unqueryable required view returns exit code `1`, which fails the job.
