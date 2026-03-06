-- Mission Control v1 core schema
-- Review before production use.

create extension if not exists pgcrypto;

create or replace function set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

create table if not exists owners (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  role text not null check (role in ('owner','chief_of_staff','main_orchestrator','security_agent','subagent','human_collaborator')),
  email text,
  is_active boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists initiatives (
  id uuid primary key default gen_random_uuid(),
  name text not null unique,
  description text,
  status text not null default 'planned'
    check (status in ('planned','active','paused','completed','cancelled')),
  target_quarter text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists projects (
  id uuid primary key default gen_random_uuid(),
  initiative_id uuid references initiatives(id) on delete set null,
  owner_id uuid references owners(id) on delete set null,
  title text not null,
  slug text not null unique,
  description text,
  category text not null
    check (category in ('software','business','learning','content','operations','personal')),
  project_type text not null
    check (project_type in ('web_app','mobile_app','backend_service','internal_tool','content_program','learning_plan','ops_program','portfolio_project','other')),
  status text not null default 'idea'
    check (status in ('idea','planned','active','blocked','paused','completed','cancelled')),
  health text not null default 'unknown'
    check (health in ('green','yellow','red','unknown')),
  priority text not null default 'p2'
    check (priority in ('p0','p1','p2','p3')),
  sponsor text,
  strategic_value integer not null default 3 check (strategic_value between 1 and 5),
  effort_size text default 'medium'
    check (effort_size in ('xs','small','medium','large','xl')),
  start_date date,
  target_date date,
  next_milestone text,
  next_action text,
  next_action_due date,
  owner_decision_needed boolean not null default false,
  software_security_required boolean not null default false,
  release_readiness_status text not null default 'not_applicable'
    check (release_readiness_status in ('not_applicable','not_started','in_progress','at_risk','ready','released')),
  notes text,
  risk_summary text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists idx_projects_status on projects(status);
create index if not exists idx_projects_category on projects(category);
create index if not exists idx_projects_owner on projects(owner_id);
create index if not exists idx_projects_target_date on projects(target_date);
create index if not exists idx_projects_owner_decision_needed on projects(owner_decision_needed);

create table if not exists milestones (
  id uuid primary key default gen_random_uuid(),
  project_id uuid not null references projects(id) on delete cascade,
  title text not null,
  milestone_date date,
  status text not null default 'planned'
    check (status in ('planned','in_progress','done','missed','cancelled')),
  notes text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists tasks (
  id uuid primary key default gen_random_uuid(),
  project_id uuid not null references projects(id) on delete cascade,
  title text not null,
  status text not null default 'todo'
    check (status in ('todo','in_progress','blocked','done','cancelled')),
  priority text not null default 'p2'
    check (priority in ('p0','p1','p2','p3')),
  due_date date,
  assignee_owner_id uuid references owners(id) on delete set null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists decisions (
  id uuid primary key default gen_random_uuid(),
  project_id uuid references projects(id) on delete set null,
  decision_date date not null default current_date,
  summary text not null,
  rationale text,
  decided_by text not null,
  follow_up_action text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists risks (
  id uuid primary key default gen_random_uuid(),
  project_id uuid not null references projects(id) on delete cascade,
  title text not null,
  severity text not null default 'medium'
    check (severity in ('low','medium','high','critical')),
  status text not null default 'open'
    check (status in ('open','mitigating','accepted','closed')),
  mitigation text,
  owner text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists weekly_reviews (
  id uuid primary key default gen_random_uuid(),
  review_week_start date not null,
  owner_id uuid references owners(id) on delete set null,
  summary text,
  priorities text,
  blockers text,
  decisions_needed text,
  stop_start_continue text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (review_week_start)
);

create table if not exists security_reviews (
  id uuid primary key default gen_random_uuid(),
  project_id uuid not null references projects(id) on delete cascade,
  review_required boolean not null default false,
  owasp_top10_status text not null default 'not_required'
    check (owasp_top10_status in ('not_required','not_started','in_progress','complete','issues_open')),
  asvs_mapping_status text not null default 'not_required'
    check (asvs_mapping_status in ('not_required','not_started','in_progress','complete','issues_open')),
  api_top10_status text not null default 'not_required'
    check (api_top10_status in ('not_required','not_started','in_progress','complete','issues_open')),
  masvs_status text not null default 'not_required'
    check (masvs_status in ('not_required','not_started','in_progress','complete','issues_open')),
  highest_open_severity text not null default 'none'
    check (highest_open_severity in ('none','low','medium','high','critical')),
  release_security_decision text not null default 'pending'
    check (release_security_decision in ('pending','go','conditional_go','no_go')),
  risk_acceptance_required boolean not null default false,
  risk_acceptance_owner text,
  notes text,
  reviewed_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (project_id)
);

create table if not exists project_status_history (
  id uuid primary key default gen_random_uuid(),
  project_id uuid not null references projects(id) on delete cascade,
  old_status text,
  new_status text,
  old_health text,
  new_health text,
  old_priority text,
  new_priority text,
  changed_at timestamptz not null default now(),
  changed_by text
);

create or replace function log_project_state_change()
returns trigger
language plpgsql
as $$
begin
  if old.status is distinct from new.status
     or old.health is distinct from new.health
     or old.priority is distinct from new.priority then
    insert into project_status_history (
      project_id,
      old_status,
      new_status,
      old_health,
      new_health,
      old_priority,
      new_priority,
      changed_by
    ) values (
      new.id,
      old.status,
      new.status,
      old.health,
      new.health,
      old.priority,
      new.priority,
      current_user
    );
  end if;
  return new;
end;
$$;

drop trigger if exists trg_set_updated_at_owners on owners;
create trigger trg_set_updated_at_owners
before update on owners
for each row execute function set_updated_at();

drop trigger if exists trg_set_updated_at_initiatives on initiatives;
create trigger trg_set_updated_at_initiatives
before update on initiatives
for each row execute function set_updated_at();

drop trigger if exists trg_set_updated_at_projects on projects;
create trigger trg_set_updated_at_projects
before update on projects
for each row execute function set_updated_at();

drop trigger if exists trg_set_updated_at_milestones on milestones;
create trigger trg_set_updated_at_milestones
before update on milestones
for each row execute function set_updated_at();

drop trigger if exists trg_set_updated_at_tasks on tasks;
create trigger trg_set_updated_at_tasks
before update on tasks
for each row execute function set_updated_at();

drop trigger if exists trg_set_updated_at_decisions on decisions;
create trigger trg_set_updated_at_decisions
before update on decisions
for each row execute function set_updated_at();

drop trigger if exists trg_set_updated_at_risks on risks;
create trigger trg_set_updated_at_risks
before update on risks
for each row execute function set_updated_at();

drop trigger if exists trg_set_updated_at_weekly_reviews on weekly_reviews;
create trigger trg_set_updated_at_weekly_reviews
before update on weekly_reviews
for each row execute function set_updated_at();

drop trigger if exists trg_set_updated_at_security_reviews on security_reviews;
create trigger trg_set_updated_at_security_reviews
before update on security_reviews
for each row execute function set_updated_at();

drop trigger if exists trg_log_project_state_change on projects;
create trigger trg_log_project_state_change
after update on projects
for each row execute function log_project_state_change();
