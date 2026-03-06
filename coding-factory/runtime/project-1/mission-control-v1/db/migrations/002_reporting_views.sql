create or replace view vw_project_summary as
select
  p.id,
  p.title,
  p.slug,
  p.category,
  p.project_type,
  p.status,
  p.health,
  p.priority,
  p.strategic_value,
  p.effort_size,
  o.name as owner_name,
  p.target_date,
  p.next_action,
  p.next_action_due,
  p.owner_decision_needed,
  p.software_security_required,
  p.release_readiness_status,
  p.updated_at
from projects p
left join owners o on o.id = p.owner_id;

create or replace view vw_blocked_projects as
select * from vw_project_summary
where status = 'blocked'
order by priority asc, target_date asc nulls last;

create or replace view vw_due_soon as
select * from vw_project_summary
where target_date is not null
  and target_date <= current_date + interval '30 day'
  and status not in ('completed','cancelled')
order by target_date asc;

create or replace view vw_owner_decisions as
select * from vw_project_summary
where owner_decision_needed = true
order by priority asc, updated_at desc;

create or replace view vw_security_posture as
select
  p.id,
  p.title,
  p.slug,
  p.project_type,
  p.status as project_status,
  sr.review_required,
  sr.owasp_top10_status,
  sr.asvs_mapping_status,
  sr.api_top10_status,
  sr.masvs_status,
  sr.highest_open_severity,
  sr.release_security_decision,
  sr.risk_acceptance_required,
  sr.reviewed_at
from projects p
left join security_reviews sr on sr.project_id = p.id
where p.software_security_required = true;

create or replace view vw_portfolio_rollup as
select
  category,
  count(*) as project_count,
  count(*) filter (where status = 'active') as active_count,
  count(*) filter (where status = 'blocked') as blocked_count,
  count(*) filter (where health = 'red') as red_count,
  count(*) filter (where owner_decision_needed = true) as owner_decision_count
from projects
group by category
order by category;

create or replace view vw_weekly_review_snapshot as
select
  wr.review_week_start,
  o.name as owner_name,
  wr.summary,
  wr.priorities,
  wr.blockers,
  wr.decisions_needed,
  wr.stop_start_continue,
  wr.updated_at
from weekly_reviews wr
left join owners o on o.id = wr.owner_id
order by wr.review_week_start desc;
