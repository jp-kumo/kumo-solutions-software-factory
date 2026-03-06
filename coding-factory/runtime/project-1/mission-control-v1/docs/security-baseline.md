# Mission Control Security Baseline

Mission Control is internal software, but it still follows **security by design**.

## Baselines to apply

- OWASP Top 10:2025
- OWASP ASVS 5.0.0
- OWASP API Security Top 10 2023 when APIs are introduced
- OWASP MASVS when a mobile client is introduced
- NIST SSDF 1.1 for secure development process
- CISA Secure by Design principles

## Minimum controls for v1

1. **Secrets**
   - Do not keep production secrets committed in Git.
   - Move off `.env` before real production-internal use.

2. **Transport**
   - Add TLS before multi-user internal deployment.
   - Keep the stack off the public internet.

3. **Auth**
   - Use product-native auth initially.
   - Add SSO only when the internal user set expands.

4. **Data**
   - Restrict database credentials to least privilege.
   - Keep Metabase on a separate application database.

5. **Backups**
   - Daily logical backups.
   - Restore test at least monthly.

6. **Security review gates**
   - Internal release is blocked when critical or high unresolved issues remain unless explicitly accepted by the owner.

## Release-blocking findings

Default **NO-GO**:
- unresolved critical issue
- unresolved high issue on auth, authorization, secrets, injection, or data exposure
- missing backup/restore validation for the first internal production release
- missing owner-approved risk acceptance when conditional release is proposed
