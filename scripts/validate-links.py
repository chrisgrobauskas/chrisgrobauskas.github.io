#!/usr/bin/env python3
"""
Temporary link validator for local Hugo site.

Crawls the local Hugo dev server, discovers all internal pages,
and checks every <a href> and <img src> link — both internal and external.

Usage:
    python scripts/validate-links.py [--base http://localhost:1313]
"""

import argparse
import sys
from collections import defaultdict
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

import requests


class LinkExtractor(HTMLParser):
    """Extract href and src attributes from HTML."""

    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "a" and "href" in attrs_dict:
            self.links.append(("a", attrs_dict["href"]))
        elif tag == "img" and "src" in attrs_dict:
            self.links.append(("img", attrs_dict["src"]))
        elif tag == "link" and "href" in attrs_dict:
            self.links.append(("link", attrs_dict["href"]))
        elif tag == "script" and "src" in attrs_dict:
            self.links.append(("script", attrs_dict["src"]))


# Set of all netlocs considered "internal" (local server + production baseURL).
_internal_netlocs = set()


def add_internal_netloc(url):
    """Register a URL's netloc as internal."""
    netloc = urlparse(url).netloc
    if netloc:
        _internal_netlocs.add(netloc)


def is_internal(url, base):
    """Check if a URL is internal to the site."""
    parsed = urlparse(url)
    if not parsed.netloc:
        return True
    return parsed.netloc in _internal_netlocs


def rewrite_to_local(url, base):
    """Rewrite a production-domain URL to the local server for fetching."""
    parsed = urlparse(url)
    base_parsed = urlparse(base)
    if parsed.netloc and parsed.netloc != base_parsed.netloc and parsed.netloc in _internal_netlocs:
        return parsed._replace(scheme=base_parsed.scheme, netloc=base_parsed.netloc).geturl()
    return url


def normalise(url, base):
    """Resolve a URL against the base and strip fragments."""
    resolved = urljoin(base, url)
    parsed = urlparse(resolved)
    # Strip fragment
    return parsed._replace(fragment="").geturl()


def crawl_internal_pages(base, session):
    """Discover all internal HTML pages by crawling from the root."""
    to_visit = {base.rstrip("/") + "/"}
    visited = set()
    page_links = {}  # page_url -> [(tag, raw_href)]

    while to_visit:
        url = to_visit.pop()
        if url in visited:
            continue
        visited.add(url)

        # Always fetch from the local server
        fetch_url = rewrite_to_local(url, base)
        try:
            resp = session.get(fetch_url, timeout=10)
        except requests.RequestException as e:
            print(f"  [CRAWL ERROR] {url}: {e}")
            continue

        content_type = resp.headers.get("content-type", "")
        if "text/html" not in content_type:
            continue

        parser = LinkExtractor()
        parser.feed(resp.text)
        page_links[url] = parser.links

        # Queue internal HTML links for crawling
        for _tag, href in parser.links:
            if not href or href.startswith(("#", "mailto:", "javascript:", "tel:")):
                continue
            abs_url = normalise(href, url)
            if is_internal(abs_url, base) and abs_url not in visited:
                to_visit.add(abs_url)

    return page_links


def check_url(url, session, cache):
    """Check a single URL. Returns (status_code, error_string_or_None)."""
    if url in cache:
        return cache[url]

    try:
        # Use HEAD first for efficiency; fall back to GET on 405/other.
        resp = session.head(url, timeout=15, allow_redirects=True)
        if resp.status_code == 405:
            resp = session.get(url, timeout=15, allow_redirects=True)
        result = (resp.status_code, None)
    except requests.ConnectionError:
        result = (0, "Connection refused / DNS failure")
    except requests.Timeout:
        result = (0, "Timeout")
    except requests.RequestException as e:
        result = (0, str(e))

    cache[url] = result
    return result


def classify_noise(tag, raw_href, abs_url, status):
    """Return a noise category string if this is a known false-positive, else None."""
    parsed = urlparse(abs_url)
    path = parsed.path

    # Theme favicon/icon references that PaperMod emits but the site may not provide
    favicon_suffixes = (
        "favicon.ico", "favicon-16x16.png", "favicon-32x32.png",
        "apple-touch-icon.png", "safari-pinned-tab.svg",
    )
    if tag == "link" and any(path.endswith(s) for s in favicon_suffixes):
        return "missing-favicon"

    # Font preconnect links (HEAD to origin returns 404 but they're just hints)
    if tag == "link" and parsed.netloc in ("fonts.googleapis.com", "fonts.gstatic.com"):
        return "font-preconnect"

    # Sites that block automated requests
    bot_block_domains = {
        "www.linkedin.com": 999,
        "linkedin.com": 999,
    }
    if parsed.netloc in bot_block_domains and status == bot_block_domains[parsed.netloc]:
        return "bot-blocked"

    # Sites that return 403 to automated HEAD/GET
    if status == 403 and parsed.netloc in (
        "www.acm.org", "acm.org",
        "www.hhs.gov", "hhs.gov",
    ):
        return "bot-blocked"

    return None


def main():
    parser = argparse.ArgumentParser(description="Validate links on local Hugo site")
    parser.add_argument("--base", default="http://localhost:1313", help="Base URL of Hugo server")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show noise categories too")
    args = parser.parse_args()

    base = args.base.rstrip("/")
    session = requests.Session()
    session.headers["User-Agent"] = "HugoLinkValidator/1.0"

    # Register the local server as internal
    add_internal_netloc(base)

    # Verify server is reachable
    try:
        r = session.get(base, timeout=5)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"ERROR: Cannot reach Hugo server at {base}: {e}")
        print("Start hugo server first:  hugo server -D")
        sys.exit(1)

    # Auto-detect Hugo's production baseURL from canonical link on homepage
    from html.parser import HTMLParser as _HP
    class _CanonicalFinder(_HP):
        def __init__(self):
            super().__init__()
            self.canonical = None
        def handle_starttag(self, tag, attrs):
            d = dict(attrs)
            if tag == "link" and d.get("rel") == "canonical" and "href" in d:
                self.canonical = d["href"]
    _cf = _CanonicalFinder()
    _cf.feed(r.text)
    if _cf.canonical:
        prod_parsed = urlparse(_cf.canonical)
        if prod_parsed.netloc and prod_parsed.netloc != urlparse(base).netloc:
            add_internal_netloc(_cf.canonical)
            print(f"Detected production baseURL: {prod_parsed.scheme}://{prod_parsed.netloc}")

    print(f"Crawling {base} …")
    page_links = crawl_internal_pages(base, session)
    print(f"Found {len(page_links)} internal pages.\n")

    # Collect all unique links to check
    broken = []  # (page, tag, raw_href, status, error, noise_cat)
    cache = {}
    external_count = 0
    internal_count = 0
    skipped = {"#", "mailto:", "javascript:", "tel:", "data:"}

    for page_url, links in sorted(page_links.items()):
        for tag, raw_href in links:
            if not raw_href or any(raw_href.startswith(s) for s in skipped):
                continue

            abs_url = normalise(raw_href, page_url)

            if is_internal(abs_url, base):
                internal_count += 1
            else:
                external_count += 1

            # For internal URLs rendered with production domain, check via local server
            check_target = rewrite_to_local(abs_url, base) if is_internal(abs_url, base) else abs_url
            status, error = check_url(check_target, session, cache)

            if status == 0 or status >= 400:
                noise_cat = classify_noise(tag, raw_href, abs_url, status)
                broken.append((page_url, tag, raw_href, status, error, noise_cat))

    # Separate noise from real issues
    real_broken = [b for b in broken if b[5] is None]
    noise = [b for b in broken if b[5] is not None]

    # Count noise by category
    noise_counts = defaultdict(int)
    for *_, cat in noise:
        noise_counts[cat] += 1

    total_checked = len(cache)
    print(f"Checked {total_checked} unique URLs ({internal_count} internal refs, {external_count} external refs).")
    print()

    # Print noise summary
    if noise_counts:
        print("Known noise (suppressed):")
        labels = {
            "missing-favicon": "Missing favicon/icon files (theme default, not provided)",
            "font-preconnect": "Font preconnect <link> (HEAD returns 404, expected)",
            "bot-blocked": "Bot-blocked external sites (LinkedIn 999, ACM/HHS 403)",
        }
        for cat, count in sorted(noise_counts.items()):
            print(f"  {labels.get(cat, cat)}: {count} occurrence(s)")
        print()

    if args.verbose and noise:
        print("--- Noise details (--verbose) ---")
        for page, tag, href, status, error, cat in noise:
            rel = page.replace(base, "") or "/"
            detail = f"HTTP {status}" if status else error
            print(f"  [{cat}] {rel}  <{tag}> {href}  →  {detail}")
        print()

    # Print real broken links
    if not real_broken:
        print("✅ All content links are valid!")
        sys.exit(0)

    by_page = defaultdict(list)
    for page, tag, href, status, error, _ in real_broken:
        by_page[page].append((tag, href, status, error))

    print(f"❌ Found {len(real_broken)} broken content link(s) on {len(by_page)} page(s):\n")
    for page_url in sorted(by_page):
        rel = page_url.replace(base, "") or "/"
        print(f"  Page: {rel}")
        for tag, href, status, error in by_page[page_url]:
            detail = f"HTTP {status}" if status else error
            print(f"    <{tag}> {href}  →  {detail}")
        print()

    sys.exit(1)


if __name__ == "__main__":
    main()
