# Custom OpenClaw Setup for Jacques (Modeled from uploaded examples)

Date: 2026-02-26

## Goal
Implement an "OpenClaw as employee" system customized for Jacques's real priorities:
1. Taste & Power content production
2. Kumo consulting pipeline and lead follow-up
3. Daily/weekly operating rhythm with Mission Control visibility
4. Security-first automation (no unsafe marketplace dependency)

## What to copy from the examples (and what to skip)

### Keep
- Topic-based messaging contexts (narrow channels reduce drift)
- One-command pipelines with stage manifests
- Multi-layer daily cron cadence (staggered)
- Nightly council style reviews (ops/security/business)
- Aggressive logging and backup discipline
- Human approval gates for high-risk actions

### Skip / downscope
- Full autonomous outbound sponsor negotiation until confidence is high
- Broad social platform automation before core workflows are stable
- Unreviewed third-party skills

## Recommended architecture for Jacques

### A) Interfaces
- Primary: Telegram topics (already in use)
- Secondary: Mission Control boards (execution visibility)
- Optional: Slack only for selected channels later

### B) Core systems (phase-ordered)
1. **Content Engine** (Taste & Power)
   - Existing `taste_and_power_system` retained as core
   - Run via `scripts/run_episode_pipeline.sh`
   - Stage outputs 1-10 + `last_run_manifest.json`
2. **Lead Engine** (Kumo)
   - Email/CRM triage with scoring + approval
   - Proposal wrapper + follow-up sequence generation
3. **Ops Engine**
   - Security audit watchdog
   - Nightly health checks and failure summaries

### C) Data stores
- Local SQLite + vector columns where needed
- Keep secrets off Drive; server-only secret env files

### D) Security controls
- Quarantine + scan external text before ingestion
- Human approval for external sends and irreversible actions
- Daily security review digest

## Telegram topic map (customized)
- `taste-power-pipeline`
- `kumo-leads`
- `ops-security`
- `nightly-build-log`
- `morning-brief`
- `knowledge-ingest`

## Mission Control board policy
- Boards:
  - Taste & Power – Pipeline
  - Kumo – Lead Pipeline
  - Ops – Security & Automation
- WIP rule: max 1 active card per board/day
- Daily movement rule: move at least one card toward Done per board

## Phase implementation plan

### Phase 1 (now)
- Keep gateway-2 as canonical Mission Control gateway
- Use existing episode wrapper for one-command runs
- Publish daily board delta summary

### Phase 2
- Add `--resume-latest` to episode wrapper
- Add stage validators for artifacts 1–10
- Add Kumo one-command proposal workflow

### Phase 3
- Add automated inbox triage (with approval) for consulting/sponsor intake
- Add council digest (business/security/ops) nightly

## Success criteria (2-week)
- 3 successful one-command episode runs with manifests
- 100% morning briefs delivered on schedule
- 0 critical security findings
- Lead pipeline has weekly movement and proposal throughput
