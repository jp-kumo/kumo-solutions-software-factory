# Security Notes

## Threat assumptions
- Legacy data interfaces may expose sensitive records if not bounded.

## Controls
- Principle of least privilege for runtime access.
- Avoid plaintext credential handling in scripts.
- Keep audit-friendly logs for migration operations.

## Known gaps
- Further hardening needed as adapters are expanded.
