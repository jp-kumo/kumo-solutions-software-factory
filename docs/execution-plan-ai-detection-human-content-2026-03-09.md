# Execution Plan Draft: Human-Like AI Content Workflow (Detection-Resilient)

**Date:** 2026-03-09  
**Source transcript:** `knowledge-capture-how-to-beat-ai-detection-and-create-human-content-even-with-ai-2026-03-09.md`  
**Goal:** Build a repeatable writing pipeline that produces useful, audience-native content that reads human, passes quality checks, and preserves brand trust.

---

## 1) Core takeaway to implement

The transcript’s practical point is: **“beating detection” = writing better, not gaming tools**.  
Primary levers are sentence variety, specificity, story, factual integrity, and editorial polish.

Use AI as a drafting engine, then apply human optimization.

---

## 2) Actionable checklist (operational)

## A. Pre-write (5–10 min)
- [ ] Define audience persona + pain point for this piece.
- [ ] Define one clear reader outcome (“after reading, they can ___”).
- [ ] Collect 3–5 concrete specifics (examples, metrics, names, references).
- [ ] Set tone targets (e.g., direct, practical, non-hype, recruiter-friendly).

## B. AI draft generation
- [ ] Generate first draft with explicit structure request (hook → problem → method → example → CTA).
- [ ] Require concrete examples and avoid generic claims.
- [ ] Ask model to include short + long sentence mix.

## C. Human optimization pass (CRAFT-style)
- [ ] **Cut fluff:** remove redundancy, filler transitions, weak qualifiers.
- [ ] **Review/edit:** enforce flow, tighten topic sentences, strengthen transitions.
- [ ] **Add visuals/media cues:** insert chart/table/screenshot placeholders where useful.
- [ ] **Fact-check:** verify claims, numbers, and references.
- [ ] **Trust-build:** add personal viewpoint, scenario, and audience language.

## D. Human-sounding refinement pass
- [ ] Replace generic phrasing with domain-specific language.
- [ ] Add 1–2 short anecdotes/case snippets.
- [ ] Introduce sentence rhythm variation (punchy + explanatory).
- [ ] Remove repeated lexical patterns.
- [ ] Read aloud and edit for natural speech.

## E. QA + release gate
- [ ] Run detector(s) as **signal**, not authority.
- [ ] If “robotic” signal appears, revise by improving style/content quality (not token substitutions).
- [ ] Final checks: clarity, originality, factuality, usefulness, tone consistency.
- [ ] Publish + track outcome metrics.

---

## 3) Implementation steps (7-day rollout)

### Day 1: Build template + SOP
- Create a reusable markdown template for long-form content in `docs/templates/`.
- Add mandatory sections: audience, outcome, evidence points, story block, fact-check references.

### Day 2: Prompt pack v1
- Create prompt set for:
  1. Draft generation
  2. Fluff reduction
  3. Story injection
  4. Fact-check checklist extraction
  5. Final tone alignment

### Day 3: Editorial rubric
- Score each piece (1–5) on:
  - Specificity
  - Narrative credibility
  - Factual integrity
  - Readability rhythm
  - Audience fit

### Day 4: Pilot on 2 pieces
- Run one blog-style and one LinkedIn-style pilot using new flow.
- Compare draft time, edit time, and final quality score.

### Day 5: Detector calibration
- Choose 1–2 detectors only.
- Establish internal threshold rules (e.g., revise only when combined with weak rubric score).

### Day 6: KPI instrumentation
- Track per-piece:
  - production time
  - revision loops
  - detector signals
  - engagement metrics (CTR/read time/comments)

### Day 7: Retrospective + standardize
- Keep what improved quality and speed.
- Document final SOP for repeat use.

---

## 4) Guardrails (important)

- Do not optimize for “detector evasion” as a primary goal.
- Prioritize truthful, high-utility writing over synthetic “humanization hacks.”
- Keep claims attributable; avoid fabricated examples/stats.
- Treat detector output as noisy heuristic.

---

## 5) Suggested immediate next action for Jacques

- Run this workflow on one upcoming Kumo Solutions authority post:
  - Topic: **Why AI automations fail in production—and the 5 controls that prevent it**
- Produce:
  1. final post draft,
  2. short demo script,
  3. rubric scorecard,
  4. lessons-learned note for workflow iteration.
