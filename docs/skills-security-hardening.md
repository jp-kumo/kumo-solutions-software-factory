# Skills Security Hardening

## What this adds

- Skill allowlist policy: `configs/skills_allowlist.json`
- Integrity baseline (checksums): `data/skills_integrity_baseline.json`
- Security scan report: `data/skills_security_report.json`
- Scanner script: `scripts/skills_security_scan.py`

## Commands

Create/refresh baseline:
```bash
python3 scripts/skills_security_scan.py --baseline
```

Verify current state vs baseline:
```bash
python3 scripts/skills_security_scan.py --verify
```

Default action (if no args): verify.

## Enforcement behavior

The scan returns non-zero if either is true:
- unapproved skills are detected (based on `approved_skills`), or
- high-severity findings are detected.

## Suggested daily job

Run daily and alert on non-zero exit:
```bash
python3 /home/jpadmin/.openclaw/workspace/scripts/skills_security_scan.py --verify
```

## Review workflow for new skills

1. Install/download skill
2. Keep it disabled operationally
3. Run scanner (`--verify`)
4. Inspect `data/skills_security_report.json`
5. If clean and approved, add skill name to `configs/skills_allowlist.json`
6. Refresh baseline (`--baseline`)
