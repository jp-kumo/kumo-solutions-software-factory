# Kumo Solutions — Protocol Pre-Screen MVP Architecture

## MVP goal
Ship a production-usable pre-screen pipeline in 2 weeks that reliably flags protocol issues for human review.

## Components
1. **Ingestion Layer**
   - Input: protocol PDF/Docx + optional SOP docs
   - Extraction: text + section segmentation

2. **Orchestrator**
   - Classifies protocol context (region, phase, therapeutic area)
   - Creates execution plan (parallel + sequential steps)
   - Enforces checkpointed state transitions

3. **Specialist Agents (v1 = 3)**
   - Regulatory Checker (FDA/EMA/local)
   - SOP Checker (internal policy)
   - Clinical Design Checker (endpoints/safety/population)

4. **Synthesis + Conflict Resolver**
   - Merges findings
   - Applies authority hierarchy:
     - External regulation > Internal SOP
   - Applies confidence-weighted ranking
   - Emits unresolved conflicts as explicit reviewer actions

5. **Output Generator**
   - Executive summary (Critical/Major/Minor)
   - Detailed findings with citations
   - Action queue for human reviewer

## Data model (minimal)
- Protocol metadata
- Findings table (agent, finding, confidence, source, severity)
- Conflict table (rule overlap + chosen authority)
- Review decisions log

## Guardrails
- Confidence is advisory, not final truth
- No silent conflict averaging
- Return partial outputs when a module fails
- Full traceability on every finding

## Deployment pattern
- Start as internal service (single tenant)
- Add tenant separation after pilot validation

## Phase 2 upgrades
- Confidence calibration using historical adjudication
- Region-specific rule packs
- Reviewer feedback loop for continuous tuning
