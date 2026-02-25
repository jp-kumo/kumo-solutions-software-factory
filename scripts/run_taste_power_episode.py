#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone


def detect_cli_shape(main_py: Path):
    text = main_py.read_text(encoding="utf-8", errors="ignore")

    # crude but resilient parsing for argparse-style declarations
    opt_flags = set(re.findall(r"add_argument\(\s*['\"](--[a-zA-Z0-9_-]+)['\"]", text))
    pos_args = re.findall(r"add_argument\(\s*['\"]([a-zA-Z0-9_]+)['\"]", text)

    return {
        "flags": sorted(opt_flags),
        "positionals": pos_args,
    }


def newest_run_dir(output_dir: Path):
    if not output_dir.exists():
        return None
    dirs = [p for p in output_dir.iterdir() if p.is_dir()]
    if not dirs:
        return None
    return sorted(dirs, key=lambda p: p.stat().st_mtime, reverse=True)[0]


def main():
    ap = argparse.ArgumentParser(description="Run Taste & Power episode pipeline with one command")
    ap.add_argument("--topic", required=True, help="Episode topic/title")
    ap.add_argument("--marketing", action="store_true", help="Include marketing outputs when supported")
    ap.add_argument("--system-dir", default="taste_and_power_system", help="Path to taste_and_power_system")
    ap.add_argument("--python", default=sys.executable or "python3", help="Python executable")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    system_dir = Path(args.system_dir).resolve()
    main_py = system_dir / "main.py"
    output_dir = system_dir / "output"

    if not main_py.exists():
        print(f"ERROR: main.py not found at {main_py}", file=sys.stderr)
        sys.exit(2)

    shape = detect_cli_shape(main_py)
    flags = set(shape["flags"])

    # choose best command strategy
    cmd = [args.python, str(main_py)]

    if "--topic" in flags:
        cmd += ["--topic", args.topic]
    elif "--title" in flags:
        cmd += ["--title", args.topic]
    elif "topic" in shape["positionals"]:
        cmd += [args.topic]

    if args.marketing:
        if "--marketing" in flags:
            cmd.append("--marketing")
        elif "--with-marketing" in flags:
            cmd.append("--with-marketing")

    print("CLI detection:")
    print(json.dumps(shape, indent=2))
    print("\nCommand:")
    print(" ".join(cmd))

    if args.dry_run:
        return

    # attempt 1: direct CLI args
    run = subprocess.run(cmd, cwd=str(system_dir))

    # attempt 2: interactive fallback
    if run.returncode != 0:
        print("\nDirect invocation failed. Retrying with interactive stdin fallback...", file=sys.stderr)
        fallback_cmd = [args.python, str(main_py)]
        inp = args.topic + "\n"
        if args.marketing:
            inp += "y\n"
        run = subprocess.run(fallback_cmd, cwd=str(system_dir), input=inp, text=True)

    if run.returncode != 0:
        print("ERROR: pipeline run failed", file=sys.stderr)
        sys.exit(run.returncode)

    latest = newest_run_dir(output_dir)
    print("\nRun complete.")
    if latest:
        print(f"Latest output: {latest}")

        manifest = {
            "topic": args.topic,
            "marketing": args.marketing,
            "system_dir": str(system_dir),
            "latest_output": str(latest),
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        }
        manifest_path = output_dir / "last_run_manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        print(f"Manifest updated: {manifest_path}")


if __name__ == "__main__":
    main()
