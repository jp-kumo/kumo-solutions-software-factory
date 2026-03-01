#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Tuple

WORKSPACE = Path('/home/jpadmin/.openclaw/workspace')
CFG_PATH = WORKSPACE / 'configs' / 'skills_allowlist.json'
BASELINE_PATH = WORKSPACE / 'data' / 'skills_integrity_baseline.json'
REPORT_PATH = WORKSPACE / 'data' / 'skills_security_report.json'

CODE_EXTS = {'.py', '.sh', '.js', '.ts', '.mjs', '.cjs', '.json', '.yaml', '.yml', '.toml', '.ini', '.md', '.txt'}

PATTERNS = {
    'shell_exec': re.compile(r'\b(subprocess\.|os\.system\(|child_process|exec\(|spawn\(|popen\()'),
    'network_call': re.compile(r'\b(requests\.|urllib\.|fetch\(|axios|httpx|curl\s|wget\s|Invoke-WebRequest)'),
    'eval_obfus': re.compile(r'\b(eval\(|exec\(|Function\(|atob\(|b64decode\()'),
    'secret_access': re.compile(r'\b(os\.environ|getenv\(|process\.env|API_KEY|TOKEN|SECRET|AUTH)\b', re.I),
    'sensitive_files': re.compile(r'(~/.ssh|\.ssh/|id_rsa|/etc/passwd|/etc/shadow|\.aws/|\.npmrc|\.git-credentials)'),
    'exfil_endpoints': re.compile(r'discord\.com/api/webhooks|hooks\.slack\.com/services|pastebin|transfer\.sh|ngrok', re.I),
}

HIGH_KINDS = {'sensitive_files', 'exfil_endpoints'}
MEDIUM_KINDS = {'eval_obfus'}

@dataclass
class Finding:
    kind: str
    severity: str
    file: str
    line: int
    snippet: str


def load_cfg() -> Dict:
    if not CFG_PATH.exists():
        raise SystemExit(f'Missing config: {CFG_PATH}')
    return json.loads(CFG_PATH.read_text(encoding='utf-8'))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def list_skill_files(scan_roots: List[str]) -> Tuple[List[Path], List[str]]:
    files: List[Path] = []
    skills_seen: set[str] = set()
    for r in scan_roots:
        root = Path(r)
        if not root.exists():
            continue
        for p in root.rglob('*'):
            if not p.is_file():
                continue
            if p.suffix.lower() not in CODE_EXTS and p.name not in {'Dockerfile', 'Makefile'}:
                continue
            files.append(p)
            rel = p.relative_to(root)
            if rel.parts:
                skills_seen.add(rel.parts[0])
    return sorted(files), sorted(skills_seen)


def quarantine_unapproved(scan_roots: List[str], unapproved_skills: List[str], quarantine_dir: Path) -> List[Dict[str, str]]:
    actions: List[Dict[str, str]] = []
    if not unapproved_skills:
        return actions

    quarantine_dir.mkdir(parents=True, exist_ok=True)
    for r in scan_roots:
        root = Path(r)
        if not root.exists():
            continue
        for skill in unapproved_skills:
            src = root / skill
            if not src.exists() or not src.is_dir():
                continue
            dst = quarantine_dir / skill
            if dst.exists():
                suffix = 1
                while (quarantine_dir / f"{skill}-{suffix}").exists():
                    suffix += 1
                dst = quarantine_dir / f"{skill}-{suffix}"
            shutil.move(str(src), str(dst))
            actions.append({"from": str(src), "to": str(dst)})
    return actions


def scan_file(path: Path) -> List[Finding]:
    out: List[Finding] = []
    try:
        text = path.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return out

    lines = text.splitlines()
    for i, line in enumerate(lines, start=1):
        for kind, rx in PATTERNS.items():
            if rx.search(line):
                sev = 'high' if kind in HIGH_KINDS else ('medium' if kind in MEDIUM_KINDS else 'info')
                out.append(Finding(kind=kind, severity=sev, file=str(path), line=i, snippet=line.strip()[:240]))
    return out


def build_baseline(files: List[Path]) -> Dict[str, str]:
    return {str(p): sha256_file(p) for p in files}


def compare_baseline(current: Dict[str, str], baseline: Dict[str, str]) -> Dict[str, List[str]]:
    cur_keys = set(current)
    base_keys = set(baseline)
    added = sorted(cur_keys - base_keys)
    removed = sorted(base_keys - cur_keys)
    modified = sorted(k for k in (cur_keys & base_keys) if current[k] != baseline[k])
    return {'added': added, 'removed': removed, 'modified': modified}


def main() -> int:
    ap = argparse.ArgumentParser(description='Scan skills for supply-chain risk and integrity drift')
    ap.add_argument('--baseline', action='store_true', help='Create/refresh integrity baseline')
    ap.add_argument('--verify', action='store_true', help='Verify current files against baseline')
    ap.add_argument('--quarantine', action='store_true', help='Move unapproved skills to quarantine dir')
    args = ap.parse_args()

    if not args.baseline and not args.verify:
        args.verify = True

    cfg = load_cfg()
    approved = set(cfg.get('approved_skills', []))
    scan_roots = cfg.get('scan_roots', [str(WORKSPACE / 'skills')])

    files, skills_seen = list_skill_files(scan_roots)
    current_hashes = build_baseline(files)

    findings: List[Finding] = []
    for p in files:
        findings.extend(scan_file(p))

    high_findings = [f for f in findings if f.severity == 'high']

    unapproved = sorted([s for s in skills_seen if s not in approved])

    quarantine_actions: List[Dict[str, str]] = []
    quarantine_enabled = bool(cfg.get('quarantine_enabled', False))
    quarantine_dir = Path(cfg.get('quarantine_dir', str(WORKSPACE / 'skills_quarantine')))
    if args.quarantine and quarantine_enabled and unapproved:
        quarantine_actions = quarantine_unapproved(scan_roots, unapproved, quarantine_dir)
        # Recompute after quarantine move
        files, skills_seen = list_skill_files(scan_roots)
        current_hashes = build_baseline(files)
        findings = []
        for p in files:
            findings.extend(scan_file(p))
        high_findings = [f for f in findings if f.severity == 'high']
        unapproved = sorted([s for s in skills_seen if s not in approved])

    baseline = {}
    drift = {'added': [], 'removed': [], 'modified': []}
    if BASELINE_PATH.exists():
        baseline = json.loads(BASELINE_PATH.read_text(encoding='utf-8'))
        drift = compare_baseline(current_hashes, baseline)

    if args.baseline:
        BASELINE_PATH.parent.mkdir(parents=True, exist_ok=True)
        BASELINE_PATH.write_text(json.dumps(current_hashes, indent=2) + '\n', encoding='utf-8')

    report = {
        'ok': True,
        'skills_seen': skills_seen,
        'approved_skills': sorted(approved),
        'unapproved_skills_seen': unapproved,
        'file_count': len(files),
        'findings_total': len(findings),
        'findings_high': len(high_findings),
        'findings_medium': len([f for f in findings if f.severity == 'medium']),
        'integrity_drift': drift,
        'findings': [asdict(f) for f in findings[:250]],
        'quarantine_actions': quarantine_actions,
    }

    deny_unapproved = bool(cfg.get('deny_if_unapproved_skill_present', True))
    deny_high = bool(cfg.get('deny_if_high_findings', True))

    if deny_unapproved and unapproved:
        report['ok'] = False
    if deny_high and high_findings:
        report['ok'] = False

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')

    print(json.dumps({
        'ok': report['ok'],
        'skills_seen': len(skills_seen),
        'unapproved_skills_seen': len(unapproved),
        'file_count': len(files),
        'findings_total': report['findings_total'],
        'findings_high': report['findings_high'],
        'findings_medium': report['findings_medium'],
        'drift_added': len(drift['added']),
        'drift_removed': len(drift['removed']),
        'drift_modified': len(drift['modified']),
        'quarantined': len(quarantine_actions),
        'report_path': str(REPORT_PATH),
        'baseline_path': str(BASELINE_PATH),
    }, indent=2))

    return 0 if report['ok'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
