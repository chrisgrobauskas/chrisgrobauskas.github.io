#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# Purpose:
#   Generate derived blog artifacts and copy docs source into the public deploy
#   directory for hosting.
# Author:
#   Site Maintainers
# Date:
#   2026-02-22
# Initial Issuance Reason:
#   Added to standardize local and CI publish preparation for GitLab Pages.
# -----------------------------------------------------------------------------

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SOURCE_DIR="${SOURCE_DIR:-$ROOT_DIR/docs}"
TARGET_DIR="${TARGET_DIR:-$ROOT_DIR/public}"

GENERATOR_SCRIPT="$ROOT_DIR/scripts/generate-blog.py"

if [[ ! -d "$SOURCE_DIR" ]]; then
  echo "Error: source directory not found: $SOURCE_DIR" >&2
  exit 1
fi

echo "Preparing deploy output..."
echo "  Source: $SOURCE_DIR"
echo "  Target: $TARGET_DIR"

if [[ -f "$GENERATOR_SCRIPT" ]]; then
  echo "Generating blog index + RSS feed..."
  if command -v python3 >/dev/null 2>&1 && python3 -V >/dev/null 2>&1; then
    python3 "$GENERATOR_SCRIPT"
  elif command -v python >/dev/null 2>&1 && python -V >/dev/null 2>&1; then
    python "$GENERATOR_SCRIPT"
  elif command -v py >/dev/null 2>&1 && py -3 -V >/dev/null 2>&1; then
    py -3 "$GENERATOR_SCRIPT"
  else
    echo "Error: Python not found; cannot run $GENERATOR_SCRIPT" >&2
    exit 1
  fi
fi

rm -rf "$TARGET_DIR"
mkdir -p "$TARGET_DIR"
cp -R "$SOURCE_DIR"/. "$TARGET_DIR"/

echo "Deploy directory ready at: $TARGET_DIR"
