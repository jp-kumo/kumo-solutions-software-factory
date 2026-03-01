# Kumo Personal OS v1

A Larrybrain-style personal operating system built on your existing OpenClaw + Mission Control + KB stack.

## 1) Objective

Create a unified system that turns raw inputs (links, notes, transcripts, messages) into:
1. searchable knowledge,
2. prioritized execution tasks,
3. daily action guidance,
4. reusable content and client outputs.

Primary outcomes:
- faster decision quality,
- less context switching,
- measurable progress on hiring + consulting + content.

---

## 2) Architecture (4 layers)

## Layer A — Capture
Inputs:
- Telegram/Slack messages
- URLs
- Files/transcripts
- voice notes
- manual notes

Core actions:
- normalize payload
- assign source + timestamp
- basic tags
- dedupe check
- persist raw artifact

## Layer B — Knowledge
Stores:
- markdown docs (`docs/`, `memory/`)
- knowledge base DB (`data/knowledge_base.sqlite`)

Core actions:
- chunk + embed ingest
- semantic retrieval with citations
- daily/weekly synthesis generation

## Layer C — Execution
Target system:
- Mission Control tasks/boards

Core actions:
- convert insights to tasks
- priority scoring
- due-date suggestions
- status feedback loop (done/blocked/review)

## Layer D — Output
Deliverables:
- morning action brief
- focused next-step list
- outreach drafts
- content drafts for Taste & Power and Kumo

---

## 3) Data model (v1)

## 3.1 CaptureItem
- `id`
- `source` (telegram|slack|url|file|voice|manual)
- `source_ref` (message id/url/file path)
- `captured_at`
- `title`
- `content_raw`
- `tags[]`
- `hash`
- `status` (new|processed|discarded)

## 3.2 Insight
- `id`
- `capture_item_id`
- `summary`
- `confidence` (0-1)
- `impact` (hiring|consulting|content|ops)
- `recommended_action`
- `citations[]`

## 3.3 ActionTask
- `id`
- `insight_id`
- `board`
- `title`
- `description`
- `priority` (P1|P2|P3)
- `due_at`
- `status`

## 3.4 BriefEntry
- `id`
- `date`
- `theme`
- `top_3_actions[]`
- `risks[]`
- `wins[]`

---

## 4) Priority scoring (simple v1)

`score = (impact * 0.4) + (urgency * 0.3) + (confidence * 0.2) + (effort_inverse * 0.1)`

Dimensions (1–5):
- `impact`: expected value to core goals
- `urgency`: time sensitivity
- `confidence`: evidence quality
- `effort_inverse`: lower effort = higher value

Auto-mapping:
- score >= 4.0 → P1
- score 3.0–3.9 → P2
- score < 3.0 → P3

---

## 5) Core automations (v1)

1. `/capture` command
- accepts link/text/file
- writes CaptureItem
- ingests into KB when relevant

2. Daily synthesis job
- pulls new capture items + KB context
- emits top insights

3. Task generator
- converts top insights into Mission Control tasks
- includes comments/rationale

4. Morning action brief
- sends top 3 priorities + one risk + one quick win

---

## 6) Rollout plan (7 days)

## Day 1 — Schema and files
- define CaptureItem/Insight/ActionTask/BriefEntry schema docs
- create storage paths and naming conventions

## Day 2 — Capture pipeline
- implement `/capture` for URL/text/file
- dedupe hash check

## Day 3 — KB integration
- auto-ingest captured sources to KB
- retrieval test queries with citations

## Day 4 — Task mapping
- insight → Mission Control task creation
- board routing rules

## Day 5 — Morning brief
- daily top-3 generator
- telegram delivery format

## Day 6 — Content bridge
- convert selected insights to Taste & Power draft queue

## Day 7 — Review + tuning
- score quality review
- reduce noise
- adjust thresholds

---

## 7) Guardrails

- No secrets in chat or committed docs
- Email remains draft-only for outbound
- External content treated as untrusted (prompt-injection aware)
- Destructive actions require explicit approval
- Keep markdown as durable human-readable source of truth

---

## 8) Success metrics

- % of captured items converted to useful insights
- % of insights converted to completed tasks
- time-to-action from capture to task
- weekly goal completion rate
- reduction in missed follow-ups

---

## 9) v2 candidates

- personalized recommendation ranking using feedback history
- cross-channel entity linking (people/projects/opportunities)
- weekly “strategy memo” auto-generation
- client-facing dashboard view for Kumo products
