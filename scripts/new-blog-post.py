#!/usr/bin/env python3
"""
Purpose:
    Scaffold a new dated blog post from templates/blog-template.md, prefill front
    matter, and optionally open the created file in VS Code.
Author:
    Site Maintainers
Date:
    2026-02-22
Initial Issuance Reason:
    Added to streamline post creation, enforce consistent metadata, and reduce
    manual setup effort for new blog entries.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = ROOT / "templates" / "blog-template.md"
BLOG_ROOT = ROOT / "docs" / "blog"


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "post"


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path

    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    counter = 2
    while True:
        candidate = parent / f"{stem}-{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a new blog post from templates/blog-template.md"
    )
    parser.add_argument("title", help="Post title")
    parser.add_argument(
        "--date",
        dest="post_date",
        default=date.today().isoformat(),
        help="Published date in YYYY-MM-DD format (default: today)",
    )
    parser.add_argument("--author", default="Your Name", help="Author name")
    parser.add_argument(
        "--description",
        default=None,
        help="One-line post description (default: generated from title)",
    )
    parser.add_argument("--category", default="Engineering", help="Category value")
    parser.add_argument(
        "--tags",
        default="docsify,blog",
        help="Comma-separated tags (default: docsify,blog)",
    )
    parser.add_argument(
        "--publish",
        action="store_true",
        help="Set draft to false for immediate publish",
    )
    parser.add_argument(
        "--no-open",
        action="store_true",
        help="Do not open created file in VS Code",
    )
    raw_args = sys.argv[1:]
    if raw_args and all(not arg.startswith("-") for arg in raw_args):
        raw_args = [" ".join(raw_args)]

    return parser.parse_args(raw_args)


def validate_date(value: str) -> str:
    try:
        parsed = date.fromisoformat(value)
    except ValueError as error:
        raise SystemExit(f"Invalid --date value '{value}'. Use YYYY-MM-DD.") from error
    return parsed.isoformat()


def replace_first(pattern: str, replacement: str, text: str) -> str:
    updated, count = re.subn(pattern, replacement, text, count=1, flags=re.MULTILINE | re.IGNORECASE)
    if count == 0:
        raise SystemExit(f"Template is missing expected field: {pattern}")
    return updated


def replace_tags_block(text: str, tags: list[str]) -> str:
    lines = text.splitlines()
    start = None
    end = None

    for index, line in enumerate(lines):
        if re.match(r"^tags:\s*$", line, re.IGNORECASE):
            start = index
            end = index
            for scan in range(index + 1, len(lines)):
                if re.match(r"^\s+-\s+", lines[scan]):
                    end = scan
                    continue
                break
            break

    if start is None or end is None:
        raise SystemExit("Template is missing expected tags block")

    tag_lines = ["tags:"] + [f"  - {tag}" for tag in tags if tag]
    new_lines = lines[:start] + tag_lines + lines[end + 1 :]
    return "\n".join(new_lines) + ("\n" if text.endswith("\n") else "")


def open_in_vscode(path: Path) -> None:
    code_cmd = shutil.which("code") or shutil.which("code.cmd")
    if not code_cmd:
        print("VS Code CLI 'code' not found; created file only.")
        return

    try:
        subprocess.run([code_cmd, str(path)], check=False)
    except OSError:
        print("Failed to open VS Code automatically; created file only.")


def main() -> None:
    args = parse_args()
    post_date = validate_date(args.post_date)

    if not TEMPLATE_PATH.exists():
        raise SystemExit(f"Template not found: {TEMPLATE_PATH}")

    title = args.title.strip()
    if not title:
        raise SystemExit("Title cannot be empty")

    description = args.description or f"Notes on {title}."
    tags = [tag.strip() for tag in args.tags.split(",") if tag.strip()]
    if not tags:
        tags = ["docsify", "blog"]

    slug = slugify(title)
    year = post_date[:4]

    target_dir = BLOG_ROOT / year
    target_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{slug}-{post_date}.md"
    target_path = unique_path(target_dir / filename)

    content = TEMPLATE_PATH.read_text(encoding="utf-8")
    content = replace_first(
        r'^title:\s*".*"\s*$', f'title: "{title}"', content
    )
    content = replace_first(
        r'^description:\s*".*"\s*$', f'description: "{description}"', content
    )
    content = replace_first(
        r'^author:\s*".*"\s*$', f'author: "{args.author.strip()}"', content
    )
    content = replace_first(r'^date:\s*".*"\s*$', f'date: "{post_date}"', content)
    content = replace_first(r'^updated:\s*".*"\s*$', f'updated: "{post_date}"', content)
    content = replace_first(
        r'^category:\s*".*"\s*$', f'category: "{args.category.strip()}"', content
    )
    content = replace_first(
        r"^draft:\s*(true|false)\s*$",
        f"draft: {'false' if args.publish else 'true'}",
        content,
    )
    content = replace_first(r"^#\s+Your Blog Post Title\s*$", f"# {title}", content)
    content = replace_tags_block(content, tags)

    target_path.write_text(content, encoding="utf-8")

    print(f"Created: {target_path}")
    print(f"Route:   /#/{year}/{target_path.stem}")
    print("Next:    edit the post, then run: python scripts/generate-blog.py")

    if not args.no_open:
        open_in_vscode(target_path)


if __name__ == "__main__":
    main()
