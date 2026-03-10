"""
Audit blog posts for non-ASCII characters.
- Reports each occurrence with file, line, char, and Unicode name.
- Auto-replaces horizontal ellipsis U+2026 (…) with ...
- Auto-replaces left/right single/double curly quotes with straight equivalents.
- Everything else is reported but left alone for human review.

Usage:
    python scripts/audit-unicode.py [--fix]

    --fix   Apply safe auto-replacements (ellipsis, curly quotes).
            Without --fix, runs in dry-run mode and reports only.
"""

import sys
import glob
import unicodedata

# Safe auto-replacements: unicode char -> ascii replacement
AUTO_REPLACE = {
    "\u2026": "...",      # horizontal ellipsis
    "\u2018": "'",        # left single quotation mark
    "\u2019": "'",        # right single quotation mark / apostrophe
    "\u201C": '"',        # left double quotation mark
    "\u201D": '"',        # right double quotation mark
    "\u2013": "-",        # en dash
    "\u2014": "--",       # em dash
    "\u00A0": " ",        # non-breaking space
}

fix_mode = "--fix" in sys.argv

blog_files = sorted(glob.glob("content/blog/**/*.md", recursive=True))

total_issues = 0
files_changed = 0

for filepath in blog_files:
    with open(filepath, "r", encoding="utf-8") as f:
        original = f.read()

    lines = original.splitlines(keepends=True)
    file_issues = []

    for lineno, line in enumerate(lines, 1):
        for col, ch in enumerate(line, 1):
            if ord(ch) > 127:
                name = unicodedata.name(ch, f"U+{ord(ch):04X}")
                auto = AUTO_REPLACE.get(ch)
                file_issues.append((lineno, col, ch, name, auto))

    if file_issues:
        print(f"\n{'='*60}")
        print(f"FILE: {filepath}")
        print(f"{'='*60}")
        for lineno, col, ch, name, auto in file_issues:
            action = f"-> auto-replace with {repr(auto)}" if auto else "-> MANUAL REVIEW NEEDED"
            print(f"  Line {lineno:4d}, Col {col:3d}: U+{ord(ch):04X} {name!r:40s} {action}")
        total_issues += len(file_issues)

    if fix_mode:
        fixed = original
        for ch, replacement in AUTO_REPLACE.items():
            fixed = fixed.replace(ch, replacement)

        if fixed != original:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(fixed)
            count = sum(original.count(ch) for ch in AUTO_REPLACE)
            print(f"  [FIXED] {count} replacement(s) applied.")
            files_changed += 1

print(f"\n{'='*60}")
print(f"SUMMARY")
print(f"{'='*60}")
print(f"Files scanned : {len(blog_files)}")
print(f"Total issues  : {total_issues}")
if fix_mode:
    print(f"Files modified: {files_changed}")
else:
    print(f"Mode          : dry-run (pass --fix to apply safe auto-replacements)")
