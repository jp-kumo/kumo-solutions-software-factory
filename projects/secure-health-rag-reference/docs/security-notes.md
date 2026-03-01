# Security Notes

## Threat assumptions
- Untrusted input can arrive from users, integrations, and retrieval context.
- Prompt context may contain hostile instructions.

## Controls in place
- Role + scope checks (`reports:read` required)
- Tenant/patient boundary enforcement in handler logic
- Sanitize-before-embed preprocessing
- ID-only audit logging with redaction

## Known gaps (intentional for MVP)
- No production JWT verification yet (mock headers used for dev)
- No real Bedrock Guardrails integration yet
- No immutable external audit sink yet

## Do not do
- Do not log payload bodies, tokens, or raw PHI
- Do not index unsanitized patient records
