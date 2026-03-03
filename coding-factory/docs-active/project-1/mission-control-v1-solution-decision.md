# Mission Control v1 Solution Decision

## Recommended v1 solution
- PostgreSQL for source-of-truth data
- Appsmith for operational UI and CRUD workflows
- Metabase for dashboards and analytics

## Why this is the recommended v1
This gives a strong balance of:
- self-hosting
- speed of delivery
- flexibility
- visual management
- low subscription cost
- future extensibility

## Why PostgreSQL
PostgreSQL is the durable operational database and should own the canonical data model.

## Why Appsmith
Appsmith is best suited to the operational layer:
- create and update project records
- run weekly reviews
- manage status changes
- maintain decisions and risks
- expose internal workflows quickly

## Why Metabase
Metabase is best suited to the visual reporting layer:
- dashboards
- portfolio health
- timelines
- aging items
- blocked work
- owner decision queue

## Why not build a custom Next.js front end first
A custom front end is still a valid long-term direction, but it increases:
- build time
- maintenance load
- auth and CRUD surface area
- reporting effort

For v1, the fastest path is to get the data model and operational workflows right first.

## Alternative path if you want less builder-style UI
An alternative is:
- PostgreSQL
- NocoDB
- Metabase

This is attractive when the team wants a spreadsheet-like interface with built-in grid / kanban / calendar patterns.

## Decision
Build Mission Control v1 on:
- PostgreSQL
- Appsmith
- Metabase

Revisit a custom Next.js UI only after the data model and workflows are proven.
