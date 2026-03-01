#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# Purpose:
#   Download and refresh vendored Docsify and Mermaid client-side assets into
#   docs/vendor for deterministic local and deploy rendering.
# Author:
#   Site Maintainers
# Date:
#   2026-02-22
# Initial Issuance Reason:
#   Added to avoid runtime CDN dependency and keep site assets versioned with
#   repository maintenance workflows.
# -----------------------------------------------------------------------------

set -euo pipefail

VENDOR="$(cd "$(dirname "$0")/.." && pwd)/docs/vendor"
mkdir -p "$VENDOR"

download() {
  local url="$1"
  local out="$VENDOR/$2"
  echo "  -> $2"
  curl -sL --fail --retry 3 -o "$out" "$url"
}

echo "Fetching Docsify vendor assets into $VENDOR ..."

# CSS – default Docsify Vue theme
download "https://cdn.jsdelivr.net/npm/docsify/themes/vue.css" \
         "docsify-theme.css"

# Core
download "https://cdn.jsdelivr.net/npm/docsify@4/lib/docsify.min.js" \
         "docsify.min.js"

# Plugins
download "https://cdn.jsdelivr.net/npm/docsify@4/lib/plugins/search.min.js" \
         "docsify-search.min.js"
download "https://cdn.jsdelivr.net/npm/docsify@4/lib/plugins/front-matter.min.js" \
         "docsify-front-matter.min.js"
download "https://cdn.jsdelivr.net/npm/docsify-mustache/dist/docsify-mustache.min.js" \
         "docsify-mustache.min.js"
download "https://cdn.jsdelivr.net/npm/docsify-copy-code@2/dist/docsify-copy-code.min.js" \
         "docsify-copy-code.min.js"
download "https://cdn.jsdelivr.net/npm/docsify-pagination/dist/docsify-pagination.min.js" \
         "docsify-pagination.min.js"

# Mermaid
download "https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js" \
         "mermaid.min.js"
download "https://cdn.jsdelivr.net/npm/docsify-mermaid@latest/dist/docsify-mermaid.js" \
         "docsify-mermaid.js"


echo ""
echo "Done. Files written to $VENDOR/"
ls -1 "$VENDOR"
