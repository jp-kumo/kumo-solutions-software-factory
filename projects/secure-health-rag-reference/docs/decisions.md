# Decisions

## D-001: Sanitize-before-embed
- Status: Accepted
- Reason: Prevent PHI from entering vector index and prompt context.

## D-002: Tenant/patient-scoped retrieval
- Status: Accepted
- Reason: Enforce ABAC boundaries to prevent cross-tenant leakage.

## D-003: Structured output validation
- Status: Accepted
- Reason: Ensure deterministic downstream behavior and reject malformed model responses.

## D-004: ID-only audit logging
- Status: Accepted
- Reason: Keep forensic traceability without logging PHI or tokens.
