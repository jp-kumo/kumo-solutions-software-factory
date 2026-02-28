#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
from pathlib import Path

SLICE = {
    "customer_id": (0, 10),
    "account_type": (10, 12),
    "full_name": (12, 42),
    "status": (42, 43),
    "balance_cents": (43, 53),
    "open_date": (53, 61),
    "risk_code": (61, 63),
}


def parse_line(line: str) -> dict:
    rec = {k: line[a:b] for k, (a, b) in SLICE.items()}

    customer_id = rec["customer_id"].strip()
    account_type = rec["account_type"].strip()
    full_name = rec["full_name"].rstrip()
    status = rec["status"].strip()

    cents_raw = rec["balance_cents"].strip() or "0"
    balance = int(cents_raw) / 100.0

    date_raw = rec["open_date"].strip()
    open_date_iso = dt.datetime.strptime(date_raw, "%Y%m%d").date().isoformat()

    risk_code = rec["risk_code"].strip()

    return {
        "customer_id": customer_id,
        "account_type": account_type,
        "full_name": full_name,
        "status": status,
        "balance": round(balance, 2),
        "open_date": open_date_iso,
        "risk_code": risk_code,
        "is_delinquent": status == "D" or risk_code == "05",
    }


def parse_file(path: Path) -> list[dict]:
    rows: list[dict] = []
    for i, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw.strip():
            continue
        if len(raw) < 63:
            raise ValueError(f"Line {i} too short ({len(raw)} chars, expected >=63)")
        rows.append(parse_line(raw))
    return rows


def write_json(rows: list[dict], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")


def write_csv(rows: list[dict], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        out_path.write_text("", encoding="utf-8")
        return
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    ap = argparse.ArgumentParser(description="Parse fixed-width COBOL-style file into JSON/CSV")
    ap.add_argument("--input", required=True, help="Path to fixed-width input file")
    ap.add_argument("--out-json", required=True, help="Output JSON path")
    ap.add_argument("--out-csv", required=True, help="Output CSV path")
    args = ap.parse_args()

    rows = parse_file(Path(args.input))
    write_json(rows, Path(args.out_json))
    write_csv(rows, Path(args.out_csv))

    print(f"Parsed {len(rows)} records")
    print(f"JSON: {args.out_json}")
    print(f"CSV:  {args.out_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
