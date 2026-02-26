# Taste & Power Phase 1 Wrapper

One-command wrapper for running new episode generation using the **existing** `taste_and_power_system` pipeline.

## Command

```bash
./scripts/run_episode_pipeline.sh --topic "The Salt Tax"
```

Optional marketing outputs (if supported by underlying pipeline CLI):

```bash
./scripts/run_episode_pipeline.sh --topic "The Salt Tax" --marketing
```

Dry run (print detected CLI shape + command only):

```bash
./scripts/run_episode_pipeline.sh --topic "The Salt Tax" --dry-run
```

## What it does

1. Detects how `taste_and_power_system/main.py` expects input (flags/positionals).
2. Runs the pipeline using best-fit invocation.
3. Falls back to interactive stdin mode if direct CLI invocation fails.
4. Writes `taste_and_power_system/output/last_run_manifest.json` with:
   - topic
   - timestamp
   - latest output folder path

## Files added

- `scripts/run_episode_pipeline.sh`
- `scripts/run_taste_power_episode.py`
- `scripts/sync_taste_power_tracker.py`

## Tracker sync automation

After runs complete, sync episode status fields in `docs/taste-power-episodes-tracker.csv` from generated output artifacts:

```bash
python3 scripts/sync_taste_power_tracker.py
```

Preview changes without writing:

```bash
python3 scripts/sync_taste_power_tracker.py --dry-run
```

The sync currently updates matched episode rows (`title` ↔ output folder slug) with:

- `status`: `Needs QA` when final script exists, else `Planned`
- `script_status`: `Ready` / `Draft` / `Not Started`
- `edit_status`: `Ready` when final script exists
- `thumb_status`: `Needs Pass` when visual prompts exist
- `notes`: latest synced output folder

## Notes

- This is a **reuse-first** wrapper. It does not replace the existing pipeline.
- It is designed to avoid duplication and work with minor CLI differences in `main.py`.
