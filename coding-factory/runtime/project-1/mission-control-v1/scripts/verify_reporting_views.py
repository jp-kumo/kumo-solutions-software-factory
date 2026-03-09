#!/usr/bin/env python3
"""
Verify required Mission Control reporting views exist and are queryable.

Usage:
  python3 scripts/verify_reporting_views.py \
    --dsn postgresql://postgres:postgres@localhost:15432/mission_control

Optional:
  --out-json path/to/report.json
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import List

import psycopg

REQUIRED_VIEWS = [
    "vw_project_summary",
    "vw_blocked_projects",
    "vw_due_soon",
    "vw_owner_decisions",
    "vw_security_posture",
    "vw_weekly_review_snapshot",
]


@dataclass
class ViewCheck:
    name: str
    exists: bool
    queryable: bool
    row_count: int | None
    error: str | None = None


def check_view(conn: psycopg.Connection, view_name: str) -> ViewCheck:
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT EXISTS (
                  SELECT 1
                  FROM information_schema.views
                  WHERE table_schema = 'public' AND table_name = %s
                )
                """,
                (view_name,),
            )
            exists = cur.fetchone()[0]

            if not exists:
                return ViewCheck(view_name, False, False, None, "view_missing")

            cur.execute(f"SELECT COUNT(*) FROM {view_name}")
            row_count = cur.fetchone()[0]
            return ViewCheck(view_name, True, True, int(row_count), None)
    except Exception as e:  # pragma: no cover - runtime protection
        return ViewCheck(view_name, True, False, None, str(e))


def run(dsn: str) -> dict:
    checks: List[ViewCheck] = []
    with psycopg.connect(dsn) as conn:
        for view in REQUIRED_VIEWS:
            checks.append(check_view(conn, view))

    ok = all(c.exists and c.queryable for c in checks)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "ok": ok,
        "required_views": REQUIRED_VIEWS,
        "checks": [asdict(c) for c in checks],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify Mission Control reporting views")
    parser.add_argument("--dsn", default=os.getenv("DATABASE_URL", ""), help="Postgres DSN")
    parser.add_argument("--out-json", default="", help="Optional output json path")
    args = parser.parse_args()

    if not args.dsn:
        print("ERROR: missing --dsn (or DATABASE_URL)")
        return 2

    report = run(args.dsn)
    print(json.dumps(report, indent=2))

    if args.out_json:
        os.makedirs(os.path.dirname(args.out_json), exist_ok=True)
        with open(args.out_json, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
