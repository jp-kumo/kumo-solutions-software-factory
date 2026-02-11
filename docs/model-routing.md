# Model Routing (Cost Guardrail Profile v1)

## Objective
Maximize useful output while avoiding Opus-level spend.

## Defaults (Active)
- Primary: `openai-codex/gpt-5.3-codex`
- Fallback: `google/gemini-3-flash`
- Thinking default: `minimal`
- Heartbeat: `google/gemini-3-flash` every `60m`
- Sub-agents/cron jobs: `google/gemini-3-flash` with `thinking=minimal`

## Routing Rules
1. Use **Gemini Flash** for background checks, summaries, heartbeat, cron summaries, and low-risk drafting.
2. Use **Codex** for implementation tasks (coding, refactors, debug loops, CLI-heavy tasks).
3. Escalate reasoning/model only when quality gap is proven (repeat failures, complex architecture tradeoffs, or high-stakes deliverables).
4. Never set any Opus model as a default.

## Escalation Triggers (allowed)
- 2+ failed attempts on same technical task
- Critical blocker with no progress for >30 minutes
- High-stakes external deliverable explicitly approved by Jacques

## Cost Controls
- Prefer short prompts and compact summaries in loops.
- Keep heartbeat low-compute and infrequent unless needed.
- Avoid unnecessary browser sessions and deep research unless explicitly requested.
- Record major model/cost decisions in `memory/YYYY-MM-DD.md`.
