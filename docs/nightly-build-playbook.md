# Nightly Build Playbook

## Goal
Ship concrete progress nightly with low cost and clear morning handoff.

## Runtime Constraints
- Model: `google/gemini-3-flash`
- Thinking: `minimal`
- No risky external actions without explicit approval

## Priority Order
1. Highest-impact coding/build task in active project
2. Reliability improvements (tests, validation, error handling)
3. Docs updates for continuity
4. Small automation that removes future manual work

## Definition of Done (nightly)
- Tangible artifact produced (code/docs/config)
- Files changed are clean and coherent
- Commit created with clear message when appropriate
- Morning summary includes:
  - What changed
  - Why it matters
  - What’s next

## Anti-Drift Rules
- No random research rabbit holes
- No speculative rewrites without clear payoff
- Keep scope realistic for one run
