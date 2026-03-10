#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# Purpose:
#   Create a timestamped tar.gz backup archive of the content source directory.
# Author:
#   Site Maintainers
# Date:
#   2026-02-22
# Updated:
#   2026-03-02  Migrated from Docsify (docs/) to Hugo (content/).
# -----------------------------------------------------------------------------

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BACKUP_DIR="$ROOT_DIR/backups"
SOURCE_DIR="${BACKUP_SOURCE_DIR:-$ROOT_DIR/content}"
TIMESTAMP="$(date +"%Y%m%d-%H%M%S")"
ARCHIVE_NAME="content-backup-${TIMESTAMP}.tar.gz"
ARCHIVE_PATH="$BACKUP_DIR/$ARCHIVE_NAME"

mkdir -p "$BACKUP_DIR"

if [[ ! -d "$SOURCE_DIR" ]]; then
  echo "Error: backup source directory not found: $SOURCE_DIR" >&2
  exit 1
fi

echo "Creating backup archive..."
echo "  Source:  $SOURCE_DIR"
echo "  Output:  $ARCHIVE_PATH"

tar \
  -czf "$ARCHIVE_PATH" \
  -C "$SOURCE_DIR" \
  .

echo "Backup complete: $ARCHIVE_PATH"
