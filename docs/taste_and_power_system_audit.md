# Taste & Power System Audit (Reuse-First)

Date: 2026-02-25

## Scope
Audited Google Drive folder `taste_and_power_system` and inventories exported to workspace:
- `docs/taste_and_power_system_inventory.txt`
- `docs/taste_and_power_agents_inventory.txt`
- `docs/taste_and_power_output_inventory.txt`

## What already exists (do not rebuild)

### Core app
- `main.py` (CLI orchestrator for episode generation)
- `production_app.py` (Streamlit production manager for launch calendar)
- `requirements.txt`, `requirements_app.txt`

### Agent framework
- `agents/base_agent.py`
- `agents/registry.py`
- `agents/prompts.py`
- `agents/utils.py`
- `agents/__init__.py`

### Output pipeline artifacts (already standardized)
Per episode run, outputs are generated as numbered stages:
1. `1_strategy_brief.json`
2. `2_research_pack.json`
3. `3_outline.json`
4. `4_script_draft.md`
5. `5_final_script.md`
6. `6_visual_prompts.json`
7. `7_map_pack.json`
8. `8_shorts_scripts.md` (optional)
9. `9_social_posts.md` (optional)
10. `10_launch_calendar.csv` (optional)

### Existing episode runs
- Pepper
- Cinnamon (multiple runs)
- Nutmeg

## Key findings

1. **System is already capable** of generating end-to-end episode artifacts.
2. **No need to create a new agent architecture**; reuse existing `agents/` framework.
3. `main.py` appears to contain duplicated method definitions (`run_marketing`, `run`) that should be cleaned to avoid maintenance drift.
4. Drive folder contains sensitive/runtime artifacts (`.env`, `venv`, `__pycache__`, `.DS_Store`) that should not be source-of-truth.

## Risks / cleanup recommended

- Remove secrets from Drive (`.env`) and rotate any exposed keys.
- Exclude `venv/`, caches, and OS junk files from shared source folders.
- Maintain one canonical code location (server workspace repo), and use Drive only for outputs/docs.

## Reuse-first implementation plan

### Phase 1 (immediate)
- Pull canonical code into workspace folder: `taste_and_power_system/` (done locally for audit).
- Create a thin wrapper command to run existing `main.py` with topic + optional marketing flag.
- Add mission-control task sync around existing stages (status updates, no code rewrite).

### Phase 2
- Refactor `main.py` to remove duplicate methods and improve reliability.
- Add resumable mode: skip already-existing stage files in run folder.
- Add strict output manifest for each run.

### Phase 3
- Integrate with nightly cron:
  - discover missing stages
  - generate only deltas
  - produce a morning summary of run health/artifacts

## Immediate next actions (no duplication)

1. Keep existing artifact schema as-is (1–10 files).
2. Build only wrappers/orchestration around current system.
3. Do not re-author prompts/agent roles unless a specific stage quality issue is proven.
4. Add secure secret handling outside Drive.
