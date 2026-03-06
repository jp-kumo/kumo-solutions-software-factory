insert into owners (name, role, email)
values
  ('Owner', 'owner', 'owner@example.com'),
  ('Chief of Staff', 'chief_of_staff', 'cos@example.com'),
  ('Main Orchestrator', 'main_orchestrator', 'orchestrator@example.com'),
  ('Security / Compliance Agent', 'security_agent', 'security@example.com')
on conflict do nothing;

insert into initiatives (name, description, status, target_quarter)
values
  ('Mission Control', 'Build the internal command center for all project types.', 'active', '2026-Q2')
on conflict (name) do nothing;

insert into projects (
  initiative_id,
  owner_id,
  title,
  slug,
  description,
  category,
  project_type,
  status,
  health,
  priority,
  sponsor,
  strategic_value,
  effort_size,
  start_date,
  target_date,
  next_milestone,
  next_action,
  next_action_due,
  owner_decision_needed,
  software_security_required,
  release_readiness_status,
  notes,
  risk_summary
)
select
  i.id,
  o.id,
  'Mission Control v1',
  'mission-control-v1',
  'Self-hosted portfolio command center built on PostgreSQL, Appsmith, and Metabase.',
  'software',
  'internal_tool',
  'active',
  'yellow',
  'p1',
  'Owner',
  5,
  'medium',
  current_date,
  current_date + interval '45 day',
  'Appsmith Portfolio Dashboard wired to PostgreSQL',
  'Review schema and launch compose stack',
  current_date + interval '3 day',
  true,
  true,
  'in_progress',
  'Project #1 for the Coding Factory.',
  'Scope creep is the main v1 risk.'
from initiatives i
cross join owners o
where i.name = 'Mission Control'
  and o.role = 'chief_of_staff'
  and not exists (select 1 from projects where slug = 'mission-control-v1');

insert into milestones (project_id, title, milestone_date, status, notes)
select p.id, 'Schema approved', current_date + interval '5 day', 'planned', 'Approve schema and views'
from projects p
where p.slug = 'mission-control-v1'
  and not exists (
    select 1 from milestones m where m.project_id = p.id and m.title = 'Schema approved'
  );

insert into milestones (project_id, title, milestone_date, status, notes)
select p.id, 'Appsmith core pages live', current_date + interval '15 day', 'planned', 'Dashboard, projects, weekly review, decisions'
from projects p
where p.slug = 'mission-control-v1'
  and not exists (
    select 1 from milestones m where m.project_id = p.id and m.title = 'Appsmith core pages live'
  );

insert into milestones (project_id, title, milestone_date, status, notes)
select p.id, 'Metabase dashboards live', current_date + interval '20 day', 'planned', 'Executive portfolio dashboards'
from projects p
where p.slug = 'mission-control-v1'
  and not exists (
    select 1 from milestones m where m.project_id = p.id and m.title = 'Metabase dashboards live'
  );

insert into tasks (project_id, title, status, priority, due_date, assignee_owner_id)
select p.id, 'Stand up local stack', 'todo', 'p1', current_date + interval '2 day', o.id
from projects p
join owners o on o.role = 'chief_of_staff'
where p.slug = 'mission-control-v1';

insert into decisions (project_id, summary, rationale, decided_by, follow_up_action)
select p.id,
       'Use PostgreSQL + Appsmith + Metabase for v1',
       'Fastest self-hosted path to a useful visual command center.',
       'Owner',
       'Implement starter repo and validate workflows'
from projects p
where p.slug = 'mission-control-v1'
  and not exists (select 1 from decisions d where d.project_id = p.id and d.summary = 'Use PostgreSQL + Appsmith + Metabase for v1');

insert into risks (project_id, title, severity, status, mitigation, owner)
select p.id,
       'V1 scope creep',
       'high',
       'open',
       'Limit scope to dashboard, registry, weekly review, decisions, and security queue.',
       'Chief of Staff'
from projects p
where p.slug = 'mission-control-v1'
  and not exists (select 1 from risks r where r.project_id = p.id and r.title = 'V1 scope creep');

insert into weekly_reviews (review_week_start, owner_id, summary, priorities, blockers, decisions_needed, stop_start_continue)
select date_trunc('week', current_date)::date,
       o.id,
       'Initial project activation week.',
       '- Approve schema\n- Launch stack\n- Create first Appsmith page',
       '- None yet',
       '- Confirm target date\n- Confirm whether mobile is explicitly out of scope for v1',
       '- Stop adding scope\n- Start implementation\n- Continue weekly review cadence'
from owners o
where o.role = 'chief_of_staff'
  and not exists (
    select 1 from weekly_reviews wr
    where wr.review_week_start = date_trunc('week', current_date)::date
  );

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
  notes
)
select p.id,
       true,
       'not_started',
       'not_started',
       'not_required',
       'not_required',
       'none',
       'pending',
       false,
       'Internal-only v1 still requires secure-by-design review and release gate.'
from projects p
where p.slug = 'mission-control-v1'
  and not exists (select 1 from security_reviews sr where sr.project_id = p.id);
