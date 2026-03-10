#!/usr/bin/env python3
"""
Purpose:
    Audit blog posts for missing or badly placed <!-- more --> excerpt markers.
    Flags posts where the excerpt shown on the listing page is too long or too
    short, and reports posts with no marker at all.
Author:
    Site Maintainers
Date:
    2026-02-24
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOG_DIR = ROOT / "content" / "blog"

# Non-empty body lines before <!-- more --> considered too few for a useful excerpt
TOO_FEW_BEFORE = 2
# Non-empty body lines before <!-- more --> considered an overly long excerpt
TOO_MANY_BEFORE = 12


def parse_post(path: Path) -> tuple[str, list[str], int]:
    content = path.read_text(encoding="utf-8")
    lines = content.splitlines()
    fm_end = 0
    if lines and lines[0].strip() == "---":
        for i, line in enumerate(lines[1:], 1):
            if line.strip() == "---":
                fm_end = i + 1
                break
    return content, lines[fm_end:], fm_end


def main() -> None:
    if not BLOG_DIR.exists():
        print(f"Blog directory not found: {BLOG_DIR}", file=sys.stderr)
        raise SystemExit(1)

    missing: list[tuple[str, int]] = []
    too_few: list[tuple[str, int, int]] = []
    too_many: list[tuple[str, int, int]] = []
    ok: list[tuple[str, int, int]] = []

    for md_path in sorted(BLOG_DIR.rglob("*.md")):
        rel = str(md_path.relative_to(BLOG_DIR))
        content, body_lines, fm_end = parse_post(md_path)

        if "<!-- more -->" not in content:
            total = len([l for l in body_lines if l.strip()])
            missing.append((rel, total))
        else:
            all_lines = content.splitlines()
            before_raw, after_raw = content.split("<!-- more -->", 1)
            before_body = [l for l in before_raw.splitlines()[fm_end:] if l.strip()]
            after_body = [l for l in after_raw.splitlines() if l.strip()]
            n = len(before_body)
            if n <= TOO_FEW_BEFORE:
                too_few.append((rel, n, len(after_body)))
            elif n >= TOO_MANY_BEFORE:
                too_many.append((rel, n, len(after_body)))
            else:
                ok.append((rel, n, len(after_body)))

    BAR = "=" * 70

    print(BAR)
    print("MISSING <!-- more --> tag")
    print(BAR)
    if missing:
        for rel, total in missing:
            print(f"  {rel}  ({total} body lines total)")
    else:
        print("  (none)")

    print()
    print(BAR)
    print(f"TOO LITTLE excerpt  (≤{TOO_FEW_BEFORE} non-empty lines before more)")
    print(BAR)
    if too_few:
        for rel, n, after in too_few:
            print(f"  before={n:2}  after={after:3}  {rel}")
    else:
        print("  (none)")

    print()
    print(BAR)
    print(f"TOO MUCH excerpt   (≥{TOO_MANY_BEFORE} non-empty lines before more)")
    print(BAR)
    if too_many:
        for rel, n, after in too_many:
            print(f"  before={n:2}  after={after:3}  {rel}")
    else:
        print("  (none)")

    print()
    print(BAR)
    print("OK posts")
    print(BAR)
    for rel, n, after in ok:
        print(f"  before={n:2}  after={after:3}  {rel}")


if __name__ == "__main__":
    main()
