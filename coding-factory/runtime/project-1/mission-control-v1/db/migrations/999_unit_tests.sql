-- Unit tests for Mission Control v1 DB logic (PostgreSQL)
-- Developed 'as-you-go' per CoS Directive 2026-03-16

begin;

-- 1. Test Owner Role Constraints
insert into owners (name, role, email) values ('Test User', 'owner', 'test@kumo.so');

do $$
begin
    begin
        insert into owners (name, role) values ('Bad User', 'hacker');
        raise exception 'Role check constraint failed to block invalid role';
    exception when check_violation then
        -- success
    end;
end $$;

-- 2. Test Initiative Status Defaults
insert into initiatives (name) values ('Test Initiative');
do $$
declare
    v_status text;
begin
    select status into v_status from initiatives where name = 'Test Initiative';
    if v_status != 'planned' then
        raise exception 'Default initiative status is not planned';
    end if;
end $$;

-- 3. Test Project Health Constraints
insert into projects (title, slug, category, project_type) 
values ('Test Project', 'test-project', 'software', 'internal_tool');

do $$
begin
    begin
        update projects set health = 'blue' where slug = 'test-project';
        raise exception 'Health check constraint failed to block invalid health status';
    exception when check_violation then
        -- success
    end;
end $$;

-- 4. Test Reporting View (vw_project_summary)
do $$
declare
    v_count int;
begin
    select count(*) into v_count from vw_project_summary where slug = 'test-project';
    if v_count != 1 then
        raise exception 'Reporting view vw_project_summary failed to return created project';
    end if;
end $$;

rollback; -- Ensure tests don't pollute migration state
