#!/usr/bin/env python3
"""envdoctor — validate .env keys against .env.example (and friends)."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

KEY_RE = re.compile(r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=")


def parse_keys(path: Path) -> tuple[set[str], list[str]]:
    if not path.exists():
        return set(), [f"missing file: {path}"]
    keys: set[str] = set()
    for i, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        m = KEY_RE.match(line)
        if not m:
            continue
        keys.add(m.group(1))
    return keys, []


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="envdoctor",
        description="Compare .env to .env.example and report missing / extra keys.",
    )
    p.add_argument("-e", "--env", default=".env", help="env file (default: .env)")
    p.add_argument(
        "-x",
        "--example",
        default=".env.example",
        help="example file (default: .env.example)",
    )
    p.add_argument(
        "--strict",
        action="store_true",
        help="also fail when .env has keys not in the example",
    )
    p.add_argument("--version", action="version", version="envdoctor 1.0.0")
    args = p.parse_args(argv)

    env_path = Path(args.env)
    ex_path = Path(args.example)

    env_keys, env_err = parse_keys(env_path)
    ex_keys, ex_err = parse_keys(ex_path)
    for err in env_err + ex_err:
        print(f"error: {err}", file=sys.stderr)
    if env_err or ex_err:
        return 2

    missing = sorted(ex_keys - env_keys)
    extra = sorted(env_keys - ex_keys)

    print(f"example: {ex_path} ({len(ex_keys)} keys)")
    print(f"env:     {env_path} ({len(env_keys)} keys)")

    ok = True
    if missing:
        ok = False
        print("\nmissing in .env (required by example):")
        for k in missing:
            print(f"  - {k}")
    else:
        print("\n✓ all example keys present in .env")

    if extra:
        print("\nextra in .env (not in example):")
        for k in extra:
            print(f"  - {k}")
        if args.strict:
            ok = False

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
