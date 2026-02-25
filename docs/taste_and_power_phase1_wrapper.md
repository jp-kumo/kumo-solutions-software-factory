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

## Notes

- This is a **reuse-first** wrapper. It does not replace the existing pipeline.
- It is designed to avoid duplication and work with minor CLI differences in `main.py`.
