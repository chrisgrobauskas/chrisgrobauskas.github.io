---
title: Site Guide
author: Maintainers
layout: "single"
---

# Site Guide

This guide describes the current [Hugo](https://gohugo.io/) + [PaperMod](https://github.com/adityatelange/hugo-PaperMod) layout, maintenance scripts, blog generation flow, and publishing behavior.

## Source of Truth

- Edit source files in `content/`.
- `public/` is generated output only (`hugo --minify`).
- Run backup before non-trivial updates:

```bash
bash scripts/backup-site.sh
```

## Current Structure

- `content/blog/YYYY/*.md` → blog post source files grouped by year
- `content/about.md` → about page
- `content/resume.md` → resume page
- `content/site-guide.md` → this guide
- `content/search.md` → search page (PaperMod Fuse.js)
- `content/_index.md` → homepage
- `content/blog/_index.md` → blog section page
- `hugo.toml` → site configuration (menu, params, taxonomies)
- `assets/css/extended/custom.css` → theme colour overrides
- `assets/css/extended/syntax.css` → code syntax token colours
- `layouts/` → Hugo template overrides and render hooks
- `layouts/_default/_markup/render-link.html` → cross-post link rewriter (temporary)
- `layouts/_default/_markup/render-codeblock-mermaid.html` → Mermaid diagram support
- `layouts/partials/extend_head.html` → favicon + fonts
- `layouts/partials/extend_footer.html` → site footer + Mermaid JS
- `layouts/404.html` → custom 404 page
- `archetypes/blog.md` → new post template
- `static/favicon.svg` → site favicon
- `static/images/grobauskas-profile-small.jpg` → profile avatar
- `themes/PaperMod/` → PaperMod theme (git submodule)
- `alignment/` → AI writing style alignment (not site content)

## Scripts

- Create a new blog post:

```bash
hugo new blog/2026/my-post-title.md
```

This creates a post from `archetypes/blog.md` with pre-filled front matter and `draft: true`.

- Local development server (includes drafts):

```bash
hugo server -D
```

- Production build:

```bash
hugo --minify
```

- Backup source:

```bash
bash scripts/backup-site.sh
```

- Audit `<!-- more -->` excerpt markers across all posts:

```bash
python scripts/audit-more-tags.py
```

- Audit non-ASCII characters:

```bash
python scripts/audit-unicode.py [--fix]
```

## Blog Post Requirements

Each post file should include front matter similar to `archetypes/blog.md`.

Recommended fields:

- `title`
- `description`
- `author`
- `date` (`YYYY-MM-DD`)
- `updated` (`YYYY-MM-DD`, optional — Hugo reads this as `lastmod`)
- `tags` (list)
- `draft` (`true` or `false`)

Behavior:

- `draft: true` posts are excluded from production builds (visible with `hugo server -D`).
- Posts are sorted by `date` descending.
- Excerpt is content above `<!-- more -->` (Hugo's native `.Summary` split).
- If `updated` is present, Hugo displays it as the last modified date.
- RSS feed generated automatically at `/index.xml`.
- Tags taxonomy at `/tags/`.

## Route and Link Behavior

- Blog post URLs: `/blog/YYYY/post-slug/`
- About: `/about/`
- Resume: `/resume/`
- Tags: `/tags/`
- Search: `/search/`
- RSS: `/index.xml`

## CI / Deploy

- `.github/workflows/deploy.yml` runs `hugo --minify` and publishes on every push to `main`.
- GitHub Pages publishes from `public/` via the `actions/deploy-pages` action.
- PaperMod theme is a git submodule — the workflow checks out submodules automatically.
- CNAME file is copied into `public/` during build.
- Enable publishing in the repo under **Settings → Pages → Source → GitHub Actions**.

## Editing Standards

- Keep CSS and theme changes in `assets/css/extended/custom.css`.
- Keep syntax highlighting in `assets/css/extended/syntax.css`.
- Preserve accessibility (contrast, readable type, visible focus states).
- Update this guide if structure, scripts, or route behavior changes.

## Style Review Sandbox

Use this collapsible block when testing content rendering during style changes.

<details>
  <summary>Markdown cheat sheet</summary>

### Headings

# H1 Heading

## H2 Heading

### H3 Heading

#### H4 Heading

### Text styles

Regular text, **bold text**, _italic text_, and ~~strikethrough~~.

Inline code example: `hugo server -D`

### Links

- Standard link: [Hugo Project](https://gohugo.io/)
- Auto-style check: [Chris Grobauskas Site](https://www.grobauskas.com)

### Lists

- Unordered item 1
  - Nested item 1.1
  - Nested item 1.2
- Unordered item 2

1. Ordered item 1
2. Ordered item 2
3. Ordered item 3

### Task list

- [x] Completed item
- [ ] Pending item

### Blockquote

> This is a blockquote for spacing, border, and contrast checks.
>
> It can span multiple lines.

### Horizontal rule

---

### Table

| Left | Center | Right |
| :--- | :----: | ----: |
| A    |   B    |     C |
| 10   |   20   |    30 |

### Code blocks

```bash
bash scripts/backup-site.sh
hugo --minify
```

```python
def hello(name: str) -> str:
    return f"Hello, {name}"
```

```json
{
  "site": "hugo",
  "theme": "PaperMod"
}
```

### HTML block

<div style="padding:0.5rem; border:1px dashed currentColor; border-radius:6px;">
  HTML preview block for rendering checks.
</div>

### Escaped markdown (literal)

\# Literal heading text

\- Literal list item

</details>

## References

- Hugo: https://gohugo.io/
- PaperMod theme: https://github.com/adityatelange/hugo-PaperMod/
