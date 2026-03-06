# Slice 03 — Appsmith Build Packet (First Pages)

Project: `mission-control-v1`  
Scope: v1 first Appsmith pages only (no API layer, no role/permission hardening beyond existing DB connectivity)  
Source specs: `runtime/project-1/mission-control-v1/appsmith/pages/01,02,04,05,06`  
Schema baseline: `db/migrations/001_core_schema.sql`, `002_reporting_views.sql`

---

## 1) Implementation objective

Produce implementation-ready Appsmith instructions for these pages:

1. Portfolio Dashboard
2. Projects Registry
3. Weekly Review
4. Decisions Log
5. Security Review Queue

Deliverables in this packet:
- Concrete widget/query/binding checklist per page
- Query definitions aligned to current DB schema/views
- Page dependency map (views/tables/queries)
- Acceptance checks for v1 completion

---

## 2) Global Appsmith setup (do once)

## 2.1 Data source
- [ ] Configure PostgreSQL datasource to `mission_control` DB.
- [ ] Verify read/write with a simple `select now();` test query.
- [ ] Keep parameterized SQL enabled for all write paths.

## 2.2 Naming + conventions
- [ ] Query naming: `qRead*` for reads, `qWrite*` for mutations.
- [ ] Page-level JS object naming: `<PageName>Utils` (optional, minimal use).
- [ ] Route with slug parameter where needed (`project-detail?slug=<slug>` if detail page exists).

## 2.3 Shared helper queries
These are reused across multiple pages.

### `qReadOwners`
```sql
select id, name, role
from owners
where is_active = true
order by name;
```

### `qReadProjects`
```sql
select
  p.id,
  p.title,
  p.slug,
  p.category,
  p.project_type,
  p.status,
  p.health,
  p.priority,
  p.owner_id,
  o.name as owner_name,
  p.target_date,
  p.next_action,
  p.next_action_due,
  p.owner_decision_needed,
  p.software_security_required,
  p.release_readiness_status,
  p.updated_at
from projects p
left join owners o on o.id = p.owner_id
where ({{!selStatus.selectedOptionValue}} or p.status = {{selStatus.selectedOptionValue}})
  and ({{!selCategory.selectedOptionValue}} or p.category = {{selCategory.selectedOptionValue}})
  and ({{!selOwner.selectedOptionValue}} or p.owner_id = {{selOwner.selectedOptionValue}})
order by p.updated_at desc;
```

### `qReadInitiatives`
```sql
select id, name, status
from initiatives
order by name;
```

---

## 3) Page packet — Portfolio Dashboard

Spec reference: `appsmith/pages/01-portfolio-dashboard.md`

## 3.1 Build checklist
- [ ] Add KPI cards: Active Projects, Blocked Projects, Due in 30 Days, Owner Decisions Needed.
- [ ] Add filter controls: `selCategory`, `selStatus`, `selHealth`, `selPriority`.
- [ ] Add summary table bound to `qReadProjectSummary.data`.
- [ ] Add quick-nav buttons to: Projects Registry, Weekly Review, Security Review Queue.
- [ ] Row click action: navigate to project detail page with slug (if detail page already exists); else open registry and prefilter by slug.

## 3.2 Queries

### `qReadPortfolioCounts`
```sql
select
  count(*) filter (where status = 'active') as active_projects,
  count(*) filter (where status = 'blocked') as blocked_projects,
  count(*) filter (
    where target_date is not null
      and target_date <= current_date + interval '30 day'
      and status not in ('completed','cancelled')
  ) as due_in_30_days,
  count(*) filter (where owner_decision_needed = true) as owner_decisions_needed
from projects
where ({{!selCategory.selectedOptionValue}} or category = {{selCategory.selectedOptionValue}})
  and ({{!selStatus.selectedOptionValue}} or status = {{selStatus.selectedOptionValue}})
  and ({{!selHealth.selectedOptionValue}} or health = {{selHealth.selectedOptionValue}})
  and ({{!selPriority.selectedOptionValue}} or priority = {{selPriority.selectedOptionValue}});
```

### `qReadProjectSummary`
```sql
select *
from vw_project_summary
where ({{!selCategory.selectedOptionValue}} or category = {{selCategory.selectedOptionValue}})
  and ({{!selStatus.selectedOptionValue}} or status = {{selStatus.selectedOptionValue}})
  and ({{!selHealth.selectedOptionValue}} or health = {{selHealth.selectedOptionValue}})
  and ({{!selPriority.selectedOptionValue}} or priority = {{selPriority.selectedOptionValue}})
order by updated_at desc;
```

### `qReadBlockedProjects`
```sql
select *
from vw_blocked_projects
where ({{!selCategory.selectedOptionValue}} or category = {{selCategory.selectedOptionValue}})
  and ({{!selHealth.selectedOptionValue}} or health = {{selHealth.selectedOptionValue}})
  and ({{!selPriority.selectedOptionValue}} or priority = {{selPriority.selectedOptionValue}})
order by priority asc, target_date asc nulls last;
```

### `qReadOwnerDecisions`
```sql
select *
from vw_owner_decisions
where ({{!selCategory.selectedOptionValue}} or category = {{selCategory.selectedOptionValue}})
  and ({{!selHealth.selectedOptionValue}} or health = {{selHealth.selectedOptionValue}})
  and ({{!selPriority.selectedOptionValue}} or priority = {{selPriority.selectedOptionValue}})
order by priority asc, updated_at desc;
```

## 3.3 Key bindings
- KPI card values:
  - `{{qReadPortfolioCounts.data?.[0]?.active_projects ?? 0}}`
  - `{{qReadPortfolioCounts.data?.[0]?.blocked_projects ?? 0}}`
  - `{{qReadPortfolioCounts.data?.[0]?.due_in_30_days ?? 0}}`
  - `{{qReadPortfolioCounts.data?.[0]?.owner_decisions_needed ?? 0}}`
- Summary table data: `{{qReadProjectSummary.data}}`
- Filter `onOptionChange`: run `qReadPortfolioCounts`, `qReadProjectSummary`, `qReadBlockedProjects`, `qReadOwnerDecisions`.

## 3.4 Page acceptance checks
- [ ] Changing any filter updates table + KPI cards.
- [ ] Table row click routes to detail context correctly.
- [ ] KPI values match direct SQL counts.

---

## 4) Page packet — Projects Registry

Spec reference: `appsmith/pages/02-projects-registry.md`

## 4.1 Build checklist
- [ ] Add top filter row: status/category/owner (`selStatus`,`selCategory`,`selOwner`).
- [ ] Add projects table bound to `qReadProjects`.
- [ ] Add create form (`frmCreateProject`) with required fields from spec.
- [ ] Add edit drawer (`drwEditProject`) hydrated from selected table row.
- [ ] Add validation messages and disable submit until required fields valid.

## 4.2 Queries

### `qWriteCreateProject`
```sql
insert into projects (
  initiative_id,
  owner_id,
  title,
  slug,
  category,
  project_type,
  status,
  health,
  priority,
  target_date,
  next_action,
  description,
  software_security_required,
  release_readiness_status
) values (
  nullif({{selCreateInitiative.selectedOptionValue}}, '')::uuid,
  {{selCreateOwner.selectedOptionValue}}::uuid,
  {{inpCreateTitle.text}},
  {{inpCreateSlug.text}},
  {{selCreateCategory.selectedOptionValue}},
  {{selCreateProjectType.selectedOptionValue}},
  {{selCreateStatus.selectedOptionValue}},
  {{selCreateHealth.selectedOptionValue}},
  {{selCreatePriority.selectedOptionValue}},
  nullif({{dpCreateTargetDate.selectedDate}}, '')::date,
  {{inpCreateNextAction.text}},
  {{txtCreateDescription.text}},
  {{swCreateSecurityRequired.isSwitchedOn}},
  {{swCreateSecurityRequired.isSwitchedOn ? selCreateReleaseReadiness.selectedOptionValue : 'not_applicable'}}
)
returning id;
```

### `qWriteUpdateProject`
```sql
update projects
set
  initiative_id = nullif({{selEditInitiative.selectedOptionValue}}, '')::uuid,
  owner_id = {{selEditOwner.selectedOptionValue}}::uuid,
  title = {{inpEditTitle.text}},
  slug = {{inpEditSlug.text}},
  category = {{selEditCategory.selectedOptionValue}},
  project_type = {{selEditProjectType.selectedOptionValue}},
  status = {{selEditStatus.selectedOptionValue}},
  health = {{selEditHealth.selectedOptionValue}},
  priority = {{selEditPriority.selectedOptionValue}},
  target_date = nullif({{dpEditTargetDate.selectedDate}}, '')::date,
  next_action = {{inpEditNextAction.text}},
  description = {{txtEditDescription.text}},
  owner_decision_needed = {{swEditOwnerDecisionNeeded.isSwitchedOn}},
  software_security_required = {{swEditSecurityRequired.isSwitchedOn}},
  release_readiness_status = {{swEditSecurityRequired.isSwitchedOn ? selEditReleaseReadiness.selectedOptionValue : 'not_applicable'}}
where id = {{tblProjects.selectedRow.id}}::uuid
returning id;
```

## 4.3 Required form validation (client-side + DB enforcement)
- [ ] Required: `title, slug, category, project_type, status, health, priority, owner_id, target_date, next_action`.
- [ ] `slug` pattern: `^[a-z0-9-]{3,80}$`.
- [ ] If `software_security_required = false`, force `release_readiness_status='not_applicable'`.
- [ ] If `software_security_required = true`, disallow `not_applicable`.

## 4.4 Key bindings
- Table data: `{{qReadProjects.data}}`
- Create submit `onClick`:
  1) run `qWriteCreateProject`
  2) show success toast
  3) reset form
  4) run `qReadProjects`
- Edit submit `onClick`:
  1) run `qWriteUpdateProject`
  2) close drawer
  3) show success toast
  4) run `qReadProjects`

## 4.5 Page acceptance checks
- [ ] Project create persists and appears in table.
- [ ] Editing changes selected record and updates `updated_at`.
- [ ] Invalid/empty required fields blocked before query execution.

---

## 5) Page packet — Weekly Review

Spec reference: `appsmith/pages/04-weekly-review.md`

## 5.1 Build checklist
- [ ] Compute current week start (Monday) in page JS or inline expression.
- [ ] Add weekly review form for `summary`, `priorities`, `blockers`, `decisions_needed`, `stop_start_continue`, `owner_id`.
- [ ] Add snapshot table bound to `vw_weekly_review_snapshot`.
- [ ] Add embedded blocked projects list (`vw_blocked_projects`).
- [ ] Add embedded owner decisions list (`vw_owner_decisions`).

## 5.2 Queries

### `qReadCurrentWeekReview`
```sql
select *
from weekly_reviews
where review_week_start = {{dateFns.startOfWeek(new Date(), { weekStartsOn: 1 }).toISOString().slice(0,10)}}::date
limit 1;
```

### `qWriteUpsertWeeklyReview`
```sql
insert into weekly_reviews (
  review_week_start,
  owner_id,
  summary,
  priorities,
  blockers,
  decisions_needed,
  stop_start_continue
) values (
  {{dateFns.startOfWeek(new Date(), { weekStartsOn: 1 }).toISOString().slice(0,10)}}::date,
  {{selReviewOwner.selectedOptionValue}}::uuid,
  {{txtSummary.text}},
  {{txtPriorities.text}},
  {{txtBlockers.text}},
  {{txtDecisionsNeeded.text}},
  {{txtStopStartContinue.text}}
)
on conflict (review_week_start)
do update set
  owner_id = excluded.owner_id,
  summary = excluded.summary,
  priorities = excluded.priorities,
  blockers = excluded.blockers,
  decisions_needed = excluded.decisions_needed,
  stop_start_continue = excluded.stop_start_continue
returning id;
```

### `qReadWeeklyReviewSnapshot`
```sql
select *
from vw_weekly_review_snapshot
order by review_week_start desc
limit 12;
```

## 5.3 Key bindings
- Form default values hydrated from `qReadCurrentWeekReview.data?.[0]` when present.
- Embedded blocked list: `{{qReadBlockedProjects.data}}`
- Embedded owner decisions: `{{qReadOwnerDecisions.data}}`
- Save button runs `qWriteUpsertWeeklyReview` then refreshes `qReadCurrentWeekReview` + `qReadWeeklyReviewSnapshot`.

## 5.4 Page acceptance checks
- [ ] Exactly one weekly row per week (`unique(review_week_start)` preserved).
- [ ] Re-saving same week updates existing row (no duplicate).
- [ ] Embedded blocked/decision lists are visible and current.

---

## 6) Page packet — Decisions Log

Spec reference: `appsmith/pages/05-decisions-log.md`

## 6.1 Build checklist
- [ ] Add filters: project select (`selDecisionProject`), date range (`drDecisionRange`).
- [ ] Add decisions table with sort by `decision_date desc`.
- [ ] Add create decision form (project optional for portfolio-level decision).

## 6.2 Queries

### `qReadDecisions`
```sql
select
  d.id,
  d.project_id,
  p.title as project_title,
  d.decision_date,
  d.summary,
  d.rationale,
  d.decided_by,
  d.follow_up_action,
  d.updated_at
from decisions d
left join projects p on p.id = d.project_id
where ({{!selDecisionProject.selectedOptionValue}} or d.project_id = {{selDecisionProject.selectedOptionValue}}::uuid)
  and ({{!drDecisionRange.startDate}} or d.decision_date >= {{drDecisionRange.startDate}}::date)
  and ({{!drDecisionRange.endDate}} or d.decision_date <= {{drDecisionRange.endDate}}::date)
order by d.decision_date desc, d.updated_at desc;
```

### `qWriteCreateDecision`
```sql
insert into decisions (
  project_id,
  decision_date,
  summary,
  rationale,
  decided_by,
  follow_up_action
) values (
  nullif({{selCreateDecisionProject.selectedOptionValue}}, '')::uuid,
  {{dpDecisionDate.selectedDate}}::date,
  {{inpDecisionSummary.text}},
  {{txtDecisionRationale.text}},
  {{inpDecidedBy.text}},
  {{txtDecisionFollowUp.text}}
)
returning id;
```

## 6.3 Key bindings
- Table data: `{{qReadDecisions.data}}`
- Create submit: run `qWriteCreateDecision`, reset form, refresh `qReadDecisions`.

## 6.4 Page acceptance checks
- [ ] New decision appears immediately with correct date/project binding.
- [ ] Project/date filters correctly reduce table data.
- [ ] Required fields (`decision_date`, `summary`, `decided_by`) enforced.

---

## 7) Page packet — Security Review Queue

Spec reference: `appsmith/pages/06-security-review-queue.md`

## 7.1 Build checklist
- [ ] Add posture table from `vw_security_posture`.
- [ ] Add filters:
  - `selReleaseDecision`
  - `selHighestSeverity`
  - `selReviewRequired` (all/true/false)
- [ ] Add update form bound to selected table row for `security_reviews` updates.
- [ ] Show conditional risk acceptance fields when needed.

## 7.2 Queries

### `qReadSecurityPosture`
```sql
select *
from vw_security_posture
where ({{!selReleaseDecision.selectedOptionValue}} or release_security_decision = {{selReleaseDecision.selectedOptionValue}})
  and ({{!selHighestSeverity.selectedOptionValue}} or highest_open_severity = {{selHighestSeverity.selectedOptionValue}})
  and (
    {{selReviewRequired.selectedOptionValue === 'all'}}
    or ({{selReviewRequired.selectedOptionValue === 'true'}} and review_required = true)
    or ({{selReviewRequired.selectedOptionValue === 'false'}} and coalesce(review_required,false) = false)
  )
order by
  case highest_open_severity
    when 'critical' then 1
    when 'high' then 2
    when 'medium' then 3
    when 'low' then 4
    else 5
  end,
  reviewed_at asc nulls first;
```

### `qReadSoftwareProjects`
```sql
select id, title, slug
from projects
where software_security_required = true
order by title;
```

### `qWriteUpdateSecurityReview`
```sql
insert into security_reviews (
  project_id,
  review_required,
  owasp_top10_status,
  asvs_mapping_status,
  api_top10_status,
  masvs_status,
  highest_open_severity,
  release_security_decision,
  risk_acceptance_required,
  risk_acceptance_owner,
  notes,
  reviewed_at
) values (
  {{tblSecurityQueue.selectedRow.id}}::uuid,
  {{swReviewRequired.isSwitchedOn}},
  {{selOwaspStatus.selectedOptionValue}},
  {{selAsvsStatus.selectedOptionValue}},
  {{selApiTop10Status.selectedOptionValue}},
  {{selMasvsStatus.selectedOptionValue}},
  {{selHighestOpenSeverity.selectedOptionValue}},
  {{selReleaseSecurityDecision.selectedOptionValue}},
  {{swRiskAcceptanceRequired.isSwitchedOn}},
  {{inpRiskAcceptanceOwner.text}},
  {{txtSecurityNotes.text}},
  now()
)
on conflict (project_id)
do update set
  review_required = excluded.review_required,
  owasp_top10_status = excluded.owasp_top10_status,
  asvs_mapping_status = excluded.asvs_mapping_status,
  api_top10_status = excluded.api_top10_status,
  masvs_status = excluded.masvs_status,
  highest_open_severity = excluded.highest_open_severity,
  release_security_decision = excluded.release_security_decision,
  risk_acceptance_required = excluded.risk_acceptance_required,
  risk_acceptance_owner = excluded.risk_acceptance_owner,
  notes = excluded.notes,
  reviewed_at = excluded.reviewed_at
returning id;
```

## 7.3 Conditional binding logic
- Risk acceptance owner input visible when:
  - `{{swRiskAcceptanceRequired.isSwitchedOn}}` OR
  - `{{selReleaseSecurityDecision.selectedOptionValue === 'conditional_go'}}`
- Optional validation rule:
  - require `risk_acceptance_owner` if `risk_acceptance_required=true`.

## 7.4 Page acceptance checks
- [ ] Projects with `software_security_required=true` appear automatically.
- [ ] Security review updates persist and reflect in table refresh.
- [ ] Conditional risk acceptance fields appear when required.

---

## 8) Dependency map (page → queries → DB objects)

| Page | Queries | DB Views | DB Tables |
|---|---|---|---|
| Portfolio Dashboard | `qReadPortfolioCounts`, `qReadProjectSummary`, `qReadBlockedProjects`, `qReadOwnerDecisions` | `vw_project_summary`, `vw_blocked_projects`, `vw_owner_decisions` | `projects`, `owners` |
| Projects Registry | `qReadProjects`, `qReadOwners`, `qReadInitiatives`, `qWriteCreateProject`, `qWriteUpdateProject` | (optional `vw_project_summary` for display variant) | `projects`, `owners`, `initiatives` |
| Weekly Review | `qReadCurrentWeekReview`, `qWriteUpsertWeeklyReview`, `qReadWeeklyReviewSnapshot`, `qReadBlockedProjects`, `qReadOwnerDecisions` | `vw_weekly_review_snapshot`, `vw_blocked_projects`, `vw_owner_decisions` | `weekly_reviews`, `projects`, `owners` |
| Decisions Log | `qReadDecisions`, `qWriteCreateDecision`, `qReadProjects` | none required | `decisions`, `projects` |
| Security Review Queue | `qReadSecurityPosture`, `qReadSoftwareProjects`, `qWriteUpdateSecurityReview` | `vw_security_posture` | `security_reviews`, `projects` |

---

## 9) End-to-end acceptance checklist (slice-level)

## 9.1 Data + query validation
- [ ] Every query executes in Appsmith without SQL errors.
- [ ] All write queries use parameterized bindings (no string concatenation).
- [ ] No query references non-existent columns in current v1 schema.

## 9.2 Workflow validation
- [ ] Portfolio Dashboard filters and KPIs work with live DB data.
- [ ] Projects Registry create/edit workflow is complete.
- [ ] Weekly Review enforces one record per week (upsert behavior).
- [ ] Decisions Log supports create + filter.
- [ ] Security Review Queue supports update + conditional risk acceptance visibility.

## 9.3 Non-goals (explicitly out of this slice)
- API layer or external integration endpoints
- Appsmith granular RBAC hardening
- UX polish beyond functional operation
- Additional pages beyond listed first-page scope

---

## 10) Notes for implementer

- This packet is artifact-only and implementation-ready; UI manipulation in Appsmith is not claimed as completed here.
- Where prior gate docs differ from runtime schema naming, runtime DB migration files are treated as source of truth for this slice.

---

## 11) Runtime verification — Appsmith reachability (local stack)

Verification timestamp: **2026-03-06 19:38:02 UTC**

Checks executed from `runtime/project-1/mission-control-v1`:

1. `docker compose ps`
   - **Result:** failed in current shell context with Docker socket permission error:
   - `permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock`
2. `curl -sS -D - http://127.0.0.1:8080/`
   - **Result:** connection failed (`curl: (7) Could not connect to server`)
3. `ss -ltnp | grep ':8080\b'`
   - **Result:** no listener detected on Appsmith port `8080`

### Verification conclusion

- **Appsmith is not reachable** from this runtime context at `http://127.0.0.1:8080`.
- Current evidence indicates either:
  - Docker services are not started, or
  - Docker daemon is running but inaccessible to this user/session due to socket permission constraints.

---

## 12) Next implementation actions (once runtime is reachable)

1. Restore Docker control for this operator/session (or run via a user with Docker access).
2. Start stack from project root:
   - `docker compose up -d`
3. Re-verify health/reachability:
   - `docker compose ps`
   - `curl -I http://127.0.0.1:8080/` (Appsmith)
   - `curl -I http://127.0.0.1:3000/` (Metabase)
4. In Appsmith UI, configure PostgreSQL datasource to `mission_control` and run `select now();`.
5. Implement pages in this packet in order:
   - Portfolio Dashboard → Projects Registry → Weekly Review → Decisions Log → Security Review Queue.
6. Execute section **9) End-to-end acceptance checklist (slice-level)** and capture pass/fail notes.

---

## 13) Blockers / dependencies for page implementation

### Active blockers

- **Blocker A — Docker daemon access in this execution context**
  - Cannot run `docker compose ps` due to `/var/run/docker.sock` permission denied.
  - Prevents validating container health/state directly.

- **Blocker B — Appsmith service not reachable on configured port**
  - Port `8080` has no active listener and HTTP probe fails.
  - Appsmith page implementation cannot proceed until service is up and reachable.

### Dependencies

- Docker daemon availability + operator permission to manage compose stack.
- `mission-control-v1/.env` configured values (already present; includes `APPSMITH_PORT=8080`).
- Postgres service healthy before Appsmith startup (`depends_on` condition in compose).
