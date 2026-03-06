# Slice 03 — Metabase Build Packet (v1)

## Scope
First-pass implementation packet for Mission Control v1 Metabase dashboards only:
- Executive Portfolio Dashboard
- Weekly Review Dashboard
- Blocked and Due Soon
- Owner Decision Queue
- Software Security Posture

v1 constraints applied: no speculative metrics, no schema expansion beyond existing reporting views.

---

## 1) SQL Question Validation vs Reporting Views

### Reporting views available (`db/migrations/002_reporting_views.sql`)
- `vw_project_summary`
- `vw_blocked_projects`
- `vw_due_soon`
- `vw_owner_decisions`
- `vw_security_posture`
- `vw_portfolio_rollup`
- `vw_weekly_review_snapshot`

### Metabase question files validated
- `metabase/questions/01-due-soon.sql` → `vw_due_soon` ✅
- `metabase/questions/02-owner-decisions.sql` → `vw_owner_decisions` ✅
- `metabase/questions/03-blocked-projects.sql` → `vw_blocked_projects` ✅
- `metabase/questions/04-security-posture.sql` → `vw_security_posture` ✅
- `metabase/questions/05-portfolio-rollup.sql` → `vw_portfolio_rollup` ✅ *(added for v1 completeness)*
- `metabase/questions/06-weekly-review-snapshot.sql` → `vw_weekly_review_snapshot` ✅ *(added for v1 completeness)*

Result: all current Metabase SQL questions reference existing reporting views.

---

## 2) Dashboard Assembly / Runbook Mapping

## A. Executive Portfolio Dashboard
**Purpose:** single-screen executive health/status view of portfolio.

**Source questions / views**
1. `05-portfolio-rollup.sql` (`vw_portfolio_rollup`)
   - Output: `category`, `project_count`, `active_count`, `blocked_count`, `red_count`, `owner_decision_count`
2. *GUI question from* `vw_project_summary` (simple aggregation in Metabase)
   - Output: total projects, active projects, blocked projects, red health count
3. `01-due-soon.sql` (`vw_due_soon`)
   - Output: project list due within 30 days
4. `02-owner-decisions.sql` (`vw_owner_decisions`)
   - Output: projects awaiting owner decision

**Suggested cards**
- KPI: total projects / active / blocked / red
- Bar: projects by category
- Table: due soon
- Table: owner decisions needed

---

## B. Weekly Review Dashboard
**Purpose:** weekly operating rhythm; summarize owner updates, blockers, and decisions.

**Source questions / views**
1. `06-weekly-review-snapshot.sql` (`vw_weekly_review_snapshot`)
   - Output: `review_week_start`, `owner_name`, `summary`, `priorities`, `blockers`, `decisions_needed`, `stop_start_continue`, `updated_at`
2. `03-blocked-projects.sql` (`vw_blocked_projects`)
   - Output: blocked project list supporting weekly unblock discussion
3. `02-owner-decisions.sql` (`vw_owner_decisions`)
   - Output: decisions queue for current week

**Suggested cards**
- Table: latest weekly summaries by owner
- Table: blockers (from weekly review text)
- Table: blocked projects
- Table: owner decisions required this week

---

## C. Blocked and Due Soon Dashboard
**Purpose:** execution risk triage board for immediate attention.

**Source questions / views**
1. `03-blocked-projects.sql` (`vw_blocked_projects`)
2. `01-due-soon.sql` (`vw_due_soon`)

**Suggested cards**
- Table: blocked projects (priority, owner, target date, next action)
- Table: due soon projects (sorted by `target_date`)
- KPI: blocked count
- KPI: due-in-30-days count

---

## D. Owner Decision Queue Dashboard
**Purpose:** clear queue of projects waiting on owner action.

**Source questions / views**
1. `02-owner-decisions.sql` (`vw_owner_decisions`)

**Suggested cards**
- Table: decision queue with priority and last update
- KPI: decisions pending
- Optional breakdown: decisions pending by owner (GUI summarize on `owner_name`)

---

## E. Software Security Posture Dashboard
**Purpose:** software-project security readiness and release risk.

**Source questions / views**
1. `04-security-posture.sql` (`vw_security_posture`)

**Suggested cards**
- KPI: software projects requiring review
- KPI: projects with `highest_open_severity in ('high','critical')`
- KPI: projects with `release_security_decision = 'no_go'`
- KPI: projects with `release_security_decision = 'conditional_go'`
- Table: OWASP/ASVS/API/MASVS status by project

---

## 3) Verification Checklist (Build + Data)

## Executive Portfolio Dashboard
- [ ] Dashboard created and shared in Metabase collection.
- [ ] KPI cards tie to `vw_project_summary` or `vw_portfolio_rollup` only.
- [ ] Category breakdown reflects `vw_portfolio_rollup.category` counts.
- [ ] Due soon and owner decision tables show non-empty sample data.
- [ ] Sort order: due soon ascending by `target_date`; decisions by `priority` then recent update.

## Weekly Review Dashboard
- [ ] Uses `06-weekly-review-snapshot.sql` as primary source.
- [ ] Latest review week appears first.
- [ ] Owner names resolve correctly (no unexpected null owner labels).
- [ ] Blocked/decision supporting tables included and load correctly.

## Blocked and Due Soon
- [ ] Includes both `03-blocked-projects.sql` and `01-due-soon.sql`.
- [ ] Blocked list contains only `status='blocked'` projects.
- [ ] Due soon list excludes completed/cancelled projects.
- [ ] KPI counts match table row counts under same filters.

## Owner Decision Queue
- [ ] Queue contains only rows where `owner_decision_needed = true`.
- [ ] Priority ordering is deterministic and visible.
- [ ] Pending decisions KPI matches table total.

## Software Security Posture
- [ ] Dashboard uses `04-security-posture.sql` / `vw_security_posture`.
- [ ] Severity and release decision KPI filters produce expected counts.
- [ ] OWASP/ASVS/API/MASVS columns visible for each software project.
- [ ] Rows with missing security review are visible and treated as “needs review”.

---

## 4) Data Gaps Found + Minimal v1-Safe Fixes

### Gap 1: Missing Metabase SQL question files for two required v1 dashboards
- **Issue:** repository initially lacked explicit Metabase question files for `vw_portfolio_rollup` and `vw_weekly_review_snapshot`.
- **Fix applied (v1-safe):**
  - added `metabase/questions/05-portfolio-rollup.sql`
  - added `metabase/questions/06-weekly-review-snapshot.sql`

### Gap 2: Security posture null review semantics
- **Issue:** `vw_security_posture` is a left join; software projects without `security_reviews` produce null controls/severity/decision.
- **v1-safe handling:** keep view as-is (correct for visibility), and in Metabase label nulls as "Pending Review" in dashboard presentation/filter defaults.

### Gap 3: Weekly review freshness visibility
- **Issue:** no explicit freshness KPI by default.
- **v1-safe handling:** add one GUI metric on `vw_weekly_review_snapshot` (`max(review_week_start)`) to indicate latest week loaded.

No schema migration required for the above v1 fixes.

---

## 5) Runtime Verification Pass (2026-03-06 UTC)

### A. Local service reachability checks

Executed from project runtime root:
`/home/jpadmin/.openclaw/workspace/coding-factory/runtime/project-1/mission-control-v1`

- TCP check: `127.0.0.1:5432` → **open**
- TCP check: `127.0.0.1:3000` → **open**
- HTTP probe: `http://127.0.0.1:3000/` returns `200`, header `X-Powered-By: Next.js`, title `OpenClaw Mission Control`

**Interpretation:**
- A web service is reachable on port `3000`, but it is **not Metabase** (Metabase would expose Metabase API/UI signatures, not a Next.js Mission Control login page).
- PostgreSQL port is reachable.

### B. SQL question execution validation status

Metabase question files present and syntactically executable against Postgres if reporting views exist:
- `metabase/questions/01-due-soon.sql`
- `metabase/questions/02-owner-decisions.sql`
- `metabase/questions/03-blocked-projects.sql`
- `metabase/questions/04-security-posture.sql`
- `metabase/questions/05-portfolio-rollup.sql`
- `metabase/questions/06-weekly-review-snapshot.sql`

**Runtime exec blocker (exact):**
1. `docker compose ps` (and any `docker compose exec ...`) fails in this runtime context with:
   - `permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock`
2. No local `psql` client available in PATH for direct host-side SQL execution.

Because of the above, this pass cannot produce row-level query output from the live runtime DB despite open DB port. This is an environment-permission/client-tooling blocker, not a SQL file mismatch blocker.

---

## 6) Final Dashboard Assembly — Next Actions

1. **Restore container control for verification**
   - Run verification as a user in the `docker` group, or with approved elevated access.
   - Re-run:
     - `docker compose ps`
     - `docker compose exec -T postgres psql -U mission_control_app -d mission_control -f /path/to/question.sql` for each question.

2. **Confirm Metabase service binding**
   - Ensure compose `metabase` is actually bound to expected host port (`3000` by default here).
   - If Mission Control UI must keep `3000`, remap Metabase to a free port (e.g., `3001`) and update runbook.

3. **Complete live data verification checklist**
   - Capture row counts/sample outputs for all 6 SQL questions.
   - Validate sort/filter semantics used by each dashboard card.

4. **Assemble final dashboards in Metabase**
   - Create 5 dashboards listed in Scope.
   - Attach validated questions (plus GUI aggregates where noted).
   - Apply default filters/labels (including “Pending Review” handling for null security rows).

5. **Sign-off packet completion**
   - Add screenshot links/IDs for each dashboard.
   - Mark section 3 checklist items complete based on live verification evidence.
