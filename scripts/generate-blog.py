#!/usr/bin/env python3
"""
Purpose:
    Generate docs/blog.md and docs/index.xml (RSS) from markdown posts in
    docs/blog/YYYY/*.md.
Author:
    Site Maintainers
Date:
    2026-02-22
Initial Issuance Reason:
    Added to automate blog listing and RSS feed generation from front matter and
    post excerpts as part of local and CI deploy flows.
"""

from __future__ import annotations

import html
import re
import sys
from dataclasses import dataclass
from datetime import UTC, datetime, time
from email.utils import format_datetime
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"
BLOG_DIR = DOCS_DIR / "blog"
BLOG_INDEX_PATH = DOCS_DIR / "blog.md"
RSS_PATH = DOCS_DIR / "index.xml"
TAGS_PATH = DOCS_DIR / "tags.md"
SITE_URL_CANDIDATES = [
    ROOT / "_site.url",
    ROOT / ".site_url",
    DOCS_DIR / "_site.url",
    DOCS_DIR / ".site_url",
]
MORE_MARKER = "<!-- more -->"


@dataclass
class Post:
    source_path: Path
    route_path: str
    title: str
    date: datetime
    updated: datetime | None
    year: int
    slug: str
    summary: str
    description: str
    author: str
    tags: list[str]


class GenerationError(Exception):
    pass


def warn(message: str) -> None:
    print(f"Warning: {message}", file=sys.stderr)


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "post"


def parse_front_matter(markdown_text: str) -> tuple[dict, str]:
    lines = markdown_text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, markdown_text

    end_index = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            end_index = index
            break

    if end_index is None:
        return {}, markdown_text

    fm_lines = lines[1:end_index]
    body = "\n".join(lines[end_index + 1 :]).lstrip("\n")

    data: dict[str, object] = {}
    current_key: str | None = None

    for raw_line in fm_lines:
        line = raw_line.rstrip()
        if not line.strip():
            continue

        list_match = re.match(r"^\s*-\s+(.*)$", line)
        if list_match and current_key:
            existing = data.get(current_key)
            if not isinstance(existing, list):
                existing = []
            existing.append(unquote(list_match.group(1).strip()))
            data[current_key] = existing
            continue

        kv_match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not kv_match:
            continue

        key, raw_value = kv_match.groups()
        key = key.strip().lower()
        value = raw_value.strip()
        current_key = key

        if value == "":
            data[key] = []
            continue

        parsed_value: object = unquote(value)
        low = str(parsed_value).lower()
        if low == "true":
            parsed_value = True
        elif low == "false":
            parsed_value = False

        data[key] = parsed_value

    return data, body


def unquote(value: str) -> str:
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    return value


def parse_date(raw: object, fallback_year: int | None = None) -> tuple[datetime, bool]:
    if isinstance(raw, str) and raw.strip():
        for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M:%S"):
            try:
                return datetime.strptime(raw.strip(), fmt), True
            except ValueError:
                pass
    if fallback_year:
        return datetime(fallback_year, 1, 1), False
    return datetime(1970, 1, 1), False


def format_date_short(value: datetime) -> str:
    return value.date().isoformat()


def extract_summary(body: str) -> str:
    excerpt = body.split(MORE_MARKER, 1)[0]
    excerpt = excerpt.strip()

    excerpt_lines = excerpt.splitlines()
    while excerpt_lines and excerpt_lines[0].strip().startswith("#"):
        excerpt_lines.pop(0)
        while excerpt_lines and not excerpt_lines[0].strip():
            excerpt_lines.pop(0)

    cleaned = "\n".join(excerpt_lines).strip()
    return cleaned


def first_paragraph(markdown_text: str) -> str:
    for block in re.split(r"\n\s*\n", markdown_text.strip()):
        candidate = block.strip()
        if candidate:
            return candidate
    return ""


def get_site_url() -> str:
    for candidate in SITE_URL_CANDIDATES:
        if candidate.exists():
            try:
                site_url = candidate.read_text(encoding="utf-8").strip()
            except OSError as error:
                warn(f"Cannot read site URL file {candidate}: {error}")
                continue
            if site_url:
                return site_url.rstrip("/")

    generated = "https://example.invalid"
    warn(f"No _site.url/.site_url found; using fallback URL: {generated}")
    return generated


def normalize_site_url(site_url: str) -> str:
    cleaned = site_url.strip()
    if not cleaned:
        raise GenerationError("Site URL is empty. Set _site.url or .site_url.")

    if cleaned.startswith("//"):
        cleaned = f"https:{cleaned}"
    elif not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", cleaned):
        cleaned = f"https://{cleaned}"

    if "#" in cleaned:
        cleaned = cleaned.split("#", 1)[0]

    cleaned = cleaned.rstrip("/")
    parsed = urlparse(cleaned)
    if not parsed.scheme or not parsed.netloc:
        raise GenerationError(f"Invalid site URL: {site_url}")

    return cleaned


def docsify_base_url(site_url: str) -> str:
    return f"{normalize_site_url(site_url)}/#/"


def load_blog_header() -> tuple[str, str]:
    default_title = "Blog"
    default_intro = "Posts are listed newest first."

    if not BLOG_INDEX_PATH.exists():
        return default_title, default_intro

    try:
        text = BLOG_INDEX_PATH.read_text(encoding="utf-8")
    except OSError as error:
        warn(f"Cannot read {BLOG_INDEX_PATH}: {error}; using default blog header")
        return default_title, default_intro
    lines = text.splitlines()

    title = default_title
    for line in lines:
        if line.startswith("# "):
            title = line[2:].strip() or default_title
            break

    intro = default_intro
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped == "---" or stripped.startswith("<!--"):
            continue
        intro = stripped
        break

    return title, intro


def collect_posts() -> tuple[list[Post], int]:
    if not BLOG_DIR.exists():
        warn(f"Blog directory not found: {BLOG_DIR}; generating empty blog index and feed")
        return [], 0

    if not BLOG_DIR.is_dir():
        raise GenerationError(f"Blog path is not a directory: {BLOG_DIR}")

    posts: list[Post] = []
    skipped_drafts = 0
    used_slugs: set[str] = set()

    for md_path in sorted(BLOG_DIR.rglob("*.md")):
        try:
            raw = md_path.read_text(encoding="utf-8")
        except OSError as error:
            warn(f"Skipping unreadable file {md_path}: {error}")
            continue

        front_matter, body = parse_front_matter(raw)

        if bool(front_matter.get("draft", False)):
            skipped_drafts += 1
            continue

        title = str(front_matter.get("title") or md_path.stem).strip()
        if not title:
            warn(f"Missing title in {md_path}; using filename stem")
            title = md_path.stem

        fallback_year = None
        if md_path.parent.name.isdigit() and len(md_path.parent.name) == 4:
            fallback_year = int(md_path.parent.name)

        post_date, has_valid_date = parse_date(front_matter.get("date"), fallback_year)
        if not has_valid_date:
            if front_matter.get("date"):
                warn(f"Invalid date in {md_path}: {front_matter.get('date')}; using fallback")
            else:
                warn(f"Missing date in {md_path}; using fallback")

        updated_date = None
        updated_raw = front_matter.get("updated")
        if isinstance(updated_raw, str) and updated_raw.strip():
            parsed_updated, has_valid_updated = parse_date(updated_raw)
            if has_valid_updated:
                updated_date = parsed_updated
            else:
                warn(f"Invalid updated date in {md_path}: {updated_raw}; ignoring updated value")

        summary = extract_summary(body)
        if MORE_MARKER not in body:
            warn(f"Missing '{MORE_MARKER}' marker in {md_path}; summary uses full content before first section break")

        description = str(front_matter.get("description") or first_paragraph(summary) or "")
        author = str(front_matter.get("author") or "")

        tags_raw = front_matter.get("tags", [])
        tags = [str(tag).strip() for tag in tags_raw] if isinstance(tags_raw, list) else []

        if not isinstance(tags_raw, list) and tags_raw not in (None, ""):
            warn(f"Tags in {md_path} are not a list; ignoring tags")

        base_slug = slugify(title)
        slug = base_slug
        suffix = 2
        while slug in used_slugs:
            slug = f"{base_slug}-{suffix}"
            suffix += 1

        if slug != base_slug:
            warn(f"Duplicate slug '{base_slug}' detected; using '{slug}' for {md_path}")
        used_slugs.add(slug)

        posts.append(
            Post(
                source_path=md_path,
                route_path=md_path.relative_to(BLOG_DIR).with_suffix("").as_posix(),
                title=title,
                date=post_date,
                updated=updated_date,
                year=post_date.year,
                slug=slug,
                summary=summary,
                description=description,
                author=author,
                tags=tags,
            )
        )

    posts.sort(key=lambda post: (post.date, post.title.lower()), reverse=True)
    return posts, skipped_drafts


def build_blog_md(posts: list[Post], site_url: str, title: str, intro: str) -> str:
    if not title.strip():
        warn("Blog title is empty; falling back to 'Blog'")
        title = "Blog"
    if not intro.strip():
        warn("Blog intro is empty; falling back to default intro")
        intro = "Posts are listed newest first."

    lines: list[str] = ["<!-- generated -->", "", f"# {title}", "", "---", "", intro, "", "---", ""]

    if not posts:
        lines.extend(["No published posts yet.", ""])
        return "\n".join(lines)

    current_year = None
    for post in posts:
        if post.year != current_year:
            if current_year is not None:
                lines.append("")
            lines.append(f"# {post.year}")
            lines.append("")
            current_year = post.year

        lines.append(f"## {post.title}")
        lines.append("")

        meta_line = f"<small>Published: {format_date_short(post.date)}"
        if post.updated and post.updated > post.date:
            meta_line += f" · Updated: {format_date_short(post.updated)}"
        meta_line += "</small>"
        lines.append(meta_line)
        lines.append("")

        if post.summary:
            lines.append(post.summary)
            lines.append("")
        else:
            lines.append("_No summary available._")
            lines.append("")

        lines.append(f"<a href=\"#/{post.route_path}\">Read More</a>")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def build_rss(posts: list[Post], site_url: str, title: str, intro: str) -> str:
    if not title.strip():
        title = "Blog"
    if not intro.strip():
        intro = "Posts are listed newest first."

    now = format_datetime(datetime.now(UTC))
    app_base = docsify_base_url(site_url)
    channel_title = html.escape(title)
    channel_link = html.escape(app_base)
    channel_desc = html.escape(intro)
    rss_link = f"{site_url.rstrip('/')}/index.xml"

    items: list[str] = []
    for post in posts:
        link = f"{app_base}{post.route_path}"
        escaped_title = html.escape(post.title)
        escaped_link = html.escape(link)
        # The example uses the full summary, not the description.
        # It also wraps it in CDATA.
        escaped_desc = f"<![CDATA[{post.summary}]]>"
        pub_date = format_datetime(datetime.combine(post.date.date(), time.min, UTC))

        item_parts = [
            "    <item>",
            f"      <title>{escaped_title}</title>",
            f"      <link>{escaped_link}</link>",
            f"      <guid>{escaped_link}</guid>",
            f"      <pubDate>{pub_date}</pubDate>",
            f"      <description>{escaped_desc}</description>",
        ]

        item_parts.append("    </item>")
        items.append("\n".join(item_parts))

    items_xml = "\n".join(items)

    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<!-- generated -->\n'
        '<rss xmlns:atom="http://www.w3.org/2005/Atom" version="2.0">\n'
        "  <channel>\n"
        f"    <title>{channel_title}</title>\n"
        f"    <link>{channel_link}</link>\n"
        f"    <description>{channel_desc}</description>\n"
        f"    <generator>scripts/generate-blog.py</generator>\n"
        f"    <language>en</language>\n"
        f"    <lastBuildDate>{now}</lastBuildDate>\n"
        f'    <atom:link href="{rss_link}" rel="self" type="application/rss+xml"/>\n'
        f"{items_xml}\n"
        "  </channel>\n"
        "</rss>\n"
    )


def build_tags_md(posts: list[Post]) -> str:
    """Build a tags index page grouped alphabetically by tag."""
    tag_map: dict[str, list[Post]] = {}
    for post in posts:
        for tag in post.tags:
            if tag:
                tag_map.setdefault(tag, []).append(post)

    if not tag_map:
        return "<!-- generated -->\n\n# Tags\n\nNo tags found.\n"

    lines: list[str] = ["<!-- generated -->", "", "# Tags", ""]
    sorted_tags = sorted(tag_map.keys(), key=str.lower)

    nav_parts = [f"[{tag}](#{slugify(tag)})" for tag in sorted_tags]
    lines.append(" · ".join(nav_parts))
    lines.append("")
    lines.append("---")
    lines.append("")

    for tag in sorted_tags:
        lines.append(f"## {tag}")
        lines.append("")
        tag_posts = sorted(tag_map[tag], key=lambda p: (p.date, p.title.lower()), reverse=True)
        for post in tag_posts:
            lines.append(
                f"- [{post.title}](#{post.route_path}) "
                f"<small>{format_date_short(post.date)}</small>"
            )
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def write_text_file(path: Path, content: str) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    except OSError as error:
        raise GenerationError(f"Failed to write {path}: {error}") from error


def main() -> None:
    try:
        if not DOCS_DIR.exists() or not DOCS_DIR.is_dir():
            raise GenerationError(f"Docs directory not found: {DOCS_DIR}")

        site_url = get_site_url()
        normalized_site_url = normalize_site_url(site_url)
        blog_title, blog_intro = load_blog_header()
        posts, skipped_drafts = collect_posts()

        write_text_file(
            BLOG_INDEX_PATH,
            build_blog_md(
                posts=posts,
                site_url=normalized_site_url,
                title=blog_title,
                intro=blog_intro,
            ),
        )

        write_text_file(
            RSS_PATH,
            build_rss(
                posts=posts,
                site_url=normalized_site_url,
                title=blog_title,
                intro=blog_intro,
            ),
        )

        write_text_file(TAGS_PATH, build_tags_md(posts))

        print(f"Generated blog index: {BLOG_INDEX_PATH}")
        print(f"Generated RSS feed:  {RSS_PATH}")
        print(f"Generated tags index: {TAGS_PATH}")
        print(f"Using site URL:      {normalized_site_url}")
        print(f"Docsify base URL:    {docsify_base_url(normalized_site_url)}")
        print(f"Published posts:     {len(posts)}")
        print(f"Skipped drafts:      {skipped_drafts}")
    except GenerationError as error:
        print(f"Error: {error}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
