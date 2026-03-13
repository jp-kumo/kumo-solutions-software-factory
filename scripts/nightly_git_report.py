#!/usr/bin/env python3
"""Generate a compact status report for git repositories in the workspace.

Usage:
  python scripts/nightly_git_report.py
  python scripts/nightly_git_report.py --root /path/to/workspace --json
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


@dataclass
class RepoStatus:
    path: str
    branch: str
    ahead: int
    behind: int
    staged: int
    unstaged: int
    untracked: int
    dirty: bool


def run_git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout.strip()


def find_repos(root: Path) -> Iterable[Path]:
    # Include root if it is a repo.
    if (root / ".git").exists():
        yield root

    # Find nested repos but skip heavy/generated folders.
    skip_dirs = {
        ".git",
        "node_modules",
        ".venv",
        ".next",
        "__pycache__",
        ".mypy_cache",
    }

    for current_root, dirnames, _ in os.walk(root):
        current = Path(current_root)

        if current != root and (current / ".git").exists():
            yield current
            # Don't descend further inside nested repo.
            dirnames[:] = []
            continue

        dirnames[:] = [d for d in dirnames if d not in skip_dirs]


def get_repo_status(repo: Path, workspace_root: Path) -> RepoStatus:
    try:
        branch = run_git(repo, "symbolic-ref", "--short", "HEAD")
    except RuntimeError:
        branch = "detached"
    porcelain = run_git(repo, "status", "--porcelain", "--branch").splitlines()

    ahead = behind = 0
    staged = unstaged = untracked = 0

    if porcelain:
        head = porcelain[0]
        if "ahead" in head:
            ahead = int(head.split("ahead ", 1)[1].split("]", 1)[0].split(",", 1)[0])
        if "behind" in head:
            behind = int(head.split("behind ", 1)[1].split("]", 1)[0].split(",", 1)[0])

    for line in porcelain[1:]:
        if not line:
            continue
        if line.startswith("??"):
            untracked += 1
            continue
        x, y = line[0], line[1]
        if x != " ":
            staged += 1
        if y != " ":
            unstaged += 1

    rel = str(repo.relative_to(workspace_root)) if repo != workspace_root else "."
    dirty = bool(staged or unstaged or untracked)

    return RepoStatus(
        path=rel,
        branch=branch,
        ahead=ahead,
        behind=behind,
        staged=staged,
        unstaged=unstaged,
        untracked=untracked,
        dirty=dirty,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate nightly git repo status report")
    parser.add_argument("--root", default=".", help="Workspace root (default: current directory)")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of plain text")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()

    repos = sorted(set(find_repos(root)))
    statuses = []
    for repo in repos:
        try:
            statuses.append(get_repo_status(repo, root))
        except Exception as exc:  # pragma: no cover - keep report robust
            statuses.append(
                RepoStatus(
                    path=str(repo.relative_to(root)) if repo != root else ".",
                    branch="error",
                    ahead=0,
                    behind=0,
                    staged=0,
                    unstaged=0,
                    untracked=0,
                    dirty=True,
                )
            )
            print(f"WARN: {repo}: {exc}")

    payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "root": str(root),
        "repos": [asdict(s) for s in statuses],
        "totals": {
            "repos": len(statuses),
            "dirty_repos": sum(1 for s in statuses if s.dirty),
            "clean_repos": sum(1 for s in statuses if not s.dirty),
            "staged": sum(s.staged for s in statuses),
            "unstaged": sum(s.unstaged for s in statuses),
            "untracked": sum(s.untracked for s in statuses),
        },
    }

    if args.json:
        print(json.dumps(payload, indent=2))
        return 0

    print(f"Nightly Git Report ({payload['generated_at_utc']})")
    print(f"Root: {payload['root']}")
    print(
        "Totals: "
        f"repos={payload['totals']['repos']} "
        f"dirty={payload['totals']['dirty_repos']} "
        f"staged={payload['totals']['staged']} "
        f"unstaged={payload['totals']['unstaged']} "
        f"untracked={payload['totals']['untracked']}"
    )
    print()

    for s in statuses:
        state = "DIRTY" if s.dirty else "clean"
        diverged = []
        if s.ahead:
            diverged.append(f"ahead {s.ahead}")
        if s.behind:
            diverged.append(f"behind {s.behind}")
        diverged_txt = f" ({', '.join(diverged)})" if diverged else ""
        print(
            f"- {s.path}: {state} | branch={s.branch}{diverged_txt} | "
            f"staged={s.staged} unstaged={s.unstaged} untracked={s.untracked}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
