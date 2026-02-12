# Resource Knowledge Card: API Cost Audit & Optimization (Claudebot/OpenClaw)

## Source
User-shared long-form note (Nick Puruczky / Reprise AI): "85% of API spend is invisible waste".

## Core Thesis
Most spend is hidden in background overhead (heartbeats + bloated context), not user-requested work.

## 3-Layer Cost Framework

### Layer 1: Stop Invisible Drain
- Move heartbeat checks to cheap/local model where possible.
- Keep startup context minimal (only essential files).
- Retrieve historical data on-demand rather than preloading everything.

### Layer 2: Spend Smarter
- Route routine tasks to cheaper/faster model.
- Escalate to premium model only for high-complexity tasks.
- Add pacing and budget guardrails.
- Keep core context files concise.

### Layer 3: Multiplier
- Use prompt caching for stable content.
- Separate stable vs dynamic context.
- Avoid editing core instructions mid-session unless needed.

## What maps to Jacques's current setup
Already aligned:
- Heartbeat reduced to 60m and routed to low-cost model.
- Minimal thinking default and low-cost cron model routing.
- Cost-aware operating stance is already active.

Gaps / Next improvements:
1. Add explicit per-task cost reporting convention in output templates.
2. Add strict context-loading rule in core operating docs (essential files only, rest on-demand).
3. Add hard budget guardrails with alert thresholds and weekly review ritual.
4. Document one-shot fallback rule for setup/integration tasks (to avoid terminal loops).

## One-shot rule (operational)
If setup task fails once with repeated manual steps, stop loop and switch to a fallback path (shared links/manual ingest/async handoff) to protect user time.

## Immediate Actionable Checklist
- [ ] Add cost review section to weekly summary output.
- [ ] Add context-minimization clause to AGENTS/ops docs.
- [ ] Define explicit daily/weekly spend thresholds and response playbook.
- [ ] Keep non-essential reference docs in `docs/knowledge/` and load only when relevant.
