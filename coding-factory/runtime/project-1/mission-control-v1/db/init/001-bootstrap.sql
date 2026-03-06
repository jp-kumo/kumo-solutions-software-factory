-- Bootstrap supporting roles/databases.
-- This runs only on first initialization of the PostgreSQL volume.

\set ON_ERROR_STOP on

SELECT 'CREATE ROLE metabase_app LOGIN PASSWORD ''change_this_now_too'''
WHERE NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'metabase_app')
\gexec

SELECT 'CREATE DATABASE metabase_app OWNER metabase_app'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'metabase_app')
\gexec
