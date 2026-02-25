# Productivity Playbook v1 (Proactive Ops)

Date: 2026-02-25
Owner: Liam

## Objective
Increase throughput and reduce rework across all active projects (Taste & Power, Kumo, review_app, security/ops) by standardizing reusable workflows.

## Operating Principles
1. **Reuse before rebuild** — extend existing systems first.
2. **One-command execution** — every repeatable flow gets a wrapper.
3. **Stage outputs + manifests** — deterministic, resumable pipelines.
4. **Board-driven work** — daily movement, weekly closeout.
5. **Security-first skills** — no unreviewed third-party skills in production.
6. **Proactive delivery** — execute obvious next steps without waiting for prompts.

## Standard Workflow Pattern
For any project workflow:
- `input/`
- `run.sh` (single entrypoint)
- `output/<run_id>/`
- `last_run_manifest.json`
- `checks/` (validation scripts)
- `README.md` (operator instructions)

## Immediate Cross-Project Implementations

### A) Taste & Power
- ✅ Phase 1 wrapper added:
  - `scripts/run_episode_pipeline.sh`
  - `scripts/run_taste_power_episode.py`
- Next: add resumable mode and stage validation checks.

### B) Kumo Pipeline
- Add one-command proposal workflow wrapper:
  - `scripts/run_kumo_proposal.sh --lead <name>`
- Standard output:
  - proposal markdown
  - email draft
  - follow-up sequence

### C) review_app
- Migrate nightly test bootstrap to `uv` for deterministic env setup.
- Keep unit tests + offline checks in a single nightly entrypoint.

### D) Ops/Security
- Weekly deep audit already scheduled.
- Add machine-readable JSON nightly summary artifact for dashboarding.

## Mission Control Operating Cadence
- **Daily (10 min)**: move top 1 item per board to In Progress.
- **Monday (20 min)**: security/audit review and patch decisions.
- **Wednesday (20 min)**: Kumo outreach/proposal push.
- **Friday (30 min)**: close one Taste & Power deliverable and plan next week.

## WIP Limits
- Max 1 active card per board per day.
- Anything blocked must include explicit blocker reason and owner.

## Quality Gates
- Every automation change must include:
  - smoke test command
  - rollback note
  - commit message with scope

## Security Controls
- Allowed skills:
  - OpenClaw stock skills
  - self-authored skills
  - reviewed and pinned third-party skills only
- Secrets never in Drive or shared docs; use server-local secret env files.

## Definition of Done (for wrappers)
- One command runs the flow.
- Manifest written with timestamp and output path.
- Failure exits non-zero with readable error.
- README usage examples included.
