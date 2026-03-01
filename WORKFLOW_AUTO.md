# WORKFLOW_AUTO.md

## Purpose
Automatic operating checklist after context resets/compactions.

## Required startup reads (direct chat)
1. `SOUL.md`
2. `USER.md`
3. `memory/YYYY-MM-DD.md` (today)
4. `memory/YYYY-MM-DD.md` (yesterday)
5. `MEMORY.md`

## If files are missing
- Create today’s `memory/YYYY-MM-DD.md` with a session bootstrap note.
- Continue safely; do not block normal execution.

## Working norms
- Prefer implementation-first updates for internal workspace tasks.
- Use checkpoint commit before non-trivial edits.
- Keep secrets out of chat and out of committed files.
- For memory/history questions, run `memory_search` first.
