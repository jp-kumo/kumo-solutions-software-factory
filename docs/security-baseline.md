# Security Baseline (OpenClaw VPS)

## Current Snapshot (2026-02-11)
- `openclaw status`: healthy
- Gateway bind: loopback
- Telegram plugin: healthy
- Security audit warning: reverse proxy headers not trusted (acceptable while local-only)

## Guardrails
1. Keep gateway local-only unless explicit remote access need.
2. Do not expose gateway token in chat, screenshots, or repo.
3. Rotate tokens/API keys immediately if leakage is suspected.
4. Keep plugins least-privilege: only enable what is actively used.
5. Do not enable high-risk automations without explicit user approval.

## Weekly Hardening Checklist (15 min)
- [ ] Run `openclaw status`
- [ ] Run `openclaw security audit --deep`
- [ ] Confirm gateway bind/auth still secure
- [ ] Confirm only required channels/plugins are enabled
- [ ] Review recent cron jobs for external-action risk
- [ ] Confirm no secrets were committed to git

## Reverse Proxy Note
If using reverse proxy later, set `gateway.trustedProxies` to proxy IP/CIDR to prevent client-IP spoofing semantics.
