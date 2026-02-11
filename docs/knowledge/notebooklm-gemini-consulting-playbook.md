# Resource Knowledge Card: NotebookLM + Gemini Deep Research for Consulting

## Source
User-shared PDF excerpt (2026-02-11): NotebookLM as a transformation-oriented consulting system.

## Core Thesis
Deliverables (slides/reports/videos) are not the end goal; **behavior change and transformation** are. 
Use a structured workflow so outputs drive action rather than sit unread.

## Practical Workflow (distilled)
1. Run Gemini Deep Research from a detailed meta prompt.
2. Create a NotebookLM knowledge hub with report + source URLs.
3. Apply Pyramid Principle before producing deliverables:
   - 1 main message
   - 3 supporting arguments
   - evidence for each
4. Create engagement assets (slide deck, short video, infographics, tables) to build buy-in.
5. Sequence change with ADKAR:
   - Awareness → Desire → Knowledge → Ability → Reinforcement

## Prompt Engineering Lessons
- Prefer action-oriented prompts over history/landscape filler.
- Review and edit the research plan once before execution.
- Push for concrete implementation timelines and decision frameworks.
- Capture and preserve source URLs for grounded outputs.

## How this maps to Jacques’s goals
- **Portfolio:** Build transformation-centric artifacts, not only technical demos.
- **Fiverr/consulting offers:** Position services around measurable behavior change and implementation.
- **Pipeline:** Use short engagement assets (video/slides) as trust accelerators.

## Immediate Implementation Plan (for our system)
1. Add a reusable "action-first deep research" prompt template in docs/prompts.
2. For each new research topic, create a matching Knowledge Card in `docs/knowledge/`.
3. Require each deliverable to include:
   - decision target
   - next 3 actions
   - owner/timeframe
4. In `#fiverr-offers`, test a new framing:
   - "from insight to implementation" package ladder (starter/standard/premium).

## Quality Gate (before sharing any client-facing output)
- Is the main message one sentence?
- Are there exactly 3 supporting points?
- Is every point tied to evidence or a source?
- Are next actions specific (owner, timeline, first step)?
