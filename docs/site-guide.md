---
title: Site Guide
author: Maintainers
tags:
  - docsify
  - contributing
  - site-guide
---

# Site Guide <!-- {docsify-ignore} -->

This guide describes the current [Docsify](https://github.com/docsifyjs/docsify) layout, maintenance scripts, blog generation flow, and publishing behavior.

## Source of Truth

- Edit source files in `docs/`.
- `public/` is generated output only.
- Run backup before non-trivial updates:

```bash
bash scripts/backup-site.sh
```

## Current Structure

- `docs/index.html` -> Docsify bootstrap and route aliases
- `docs/_sidebar.md` -> sidebar navigation (includes avatar, LinkedIn, GitHub, and Resume link)
- `docs/blog/` -> blog post source files grouped by year (`docs/blog/YYYY/*.md`)
- `docs/blog.md` -> generated blog listing (do not hand-edit; starts with `<!-- generated -->`)
- `docs/index.xml` -> generated RSS feed (do not hand-edit; starts with `<!-- generated -->`)
- `docs/tags.md` -> generated tags index (do not hand-edit; starts with `<!-- generated -->`)
- `docs/_site.url` -> canonical site base URL for RSS links
- `docs/resume.md` -> resume page
- `docs/assets/docs/custom.css` -> theme overrides
- `docs/assets/docs/favicon.svg` -> site favicon
- `docs/assets/docs/grobauskas-profile-small.jpg` -> profile avatar used in sidebar
- `docs/assets/docs/generated-pipelines/` -> pipeline diagram images
- `docs/vendor/` -> vendored Docsify/mermaid assets

## Scripts

- Refresh vendor assets:

```bash
bash scripts/vendor-js.sh
```

- Generate blog list + RSS:

```bash
python scripts/generate-blog.py
```

- Create a new post from template (auto-fills front matter and opens editor):

```bash
python scripts/new-blog-post.py "Post Title"
# Also valid when no options are used:
python scripts/new-blog-post.py Post Title
```

Notes:

- Unquoted multi-word titles are supported only when no options are provided.
- If you pass options (for example `--date` or `--tags`), quote multi-word titles.

- Build deploy output (`docs/` -> `public/`):

```bash
bash scripts/deploy-site.sh
```

- Backup source:

```bash
bash scripts/backup-site.sh
```

- Audit `<!-- more -->` excerpt markers across all posts:

```bash
python scripts/audit-more-tags.py
```

## Blog Post Requirements

Each post file should include front matter similar to `templates/blog-template.md`.

Recommended fields:

- `title`
- `description`
- `author`
- `date` (`YYYY-MM-DD`)
- `updated` (`YYYY-MM-DD`, optional)
- `tags` (list)
- `draft` (`true` or `false`)

Behavior:

- `draft: true` posts are excluded.
- Posts are sorted by `date` descending.
- Excerpt is content above `<!-- more -->`.
- If `updated` is newer than `date`, blog listing shows both Published and Updated.
- Generated listing uses plain H2 post titles and a `Read More` route link below each excerpt.

## Route and Link Behavior

- Blog links are generated as Docsify hash routes:
  - `/#/YYYY/post-file-name-without-md`
- Docsify alias rules in `docs/index.html` map those routes to files in `docs/blog/YYYY/*.md`.
- RSS links are absolute and built from `docs/_site.url`.

## CI / Deploy

- `.github/workflows/deploy.yml` runs blog generation and publishes on every push to `main`.
- `scripts/deploy-site.sh` also runs generation locally, then copies `docs/` to `public/`.
- GitHub Pages publishes from `public/` via the `actions/deploy-pages` action.
- Enable publishing in the repo under **Settings → Pages → Source → GitHub Actions**.

## Migrated Content

Posts from [www.grobauskas.com](https://www.grobauskas.com) have been migrated into year subdirectories under `docs/blog/`. Front matter has been converted from MkDocs format to Docsify format:

- `date.created` → `date`
- `date.updated` → `updated`
- `authors` → `author`
- `categories` → `tags`
- Image paths updated from `../../assets/` to `../../assets/docs/` to match this repo's structure.

## Editing Standards

- Keep CSS and theme changes in `docs/assets/docs/custom.css`.
- Preserve accessibility (contrast, readable type, visible focus states).
- Update this guide if structure, scripts, or route behavior changes.

## Style Review Sandbox

Use this collapsible block when testing content rendering during style changes.

<details>
  <summary>Markdown cheat sheet + Mustache snippets</summary>

### Headings

# H1 Heading
## H2 Heading
### H3 Heading
#### H4 Heading

### Text styles

Regular text, **bold text**, *italic text*, and ~~strikethrough~~.

Inline code example: `scripts/deploy-site.sh`

### Links

- Standard link: [Docsify Project](https://github.com/docsifyjs/docsify)
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
|:-----|:------:|------:|
| A    | B      | C     |
| 10   | 20     | 30    |

### Code blocks

```bash
bash scripts/backup-site.sh
bash scripts/deploy-site.sh
```

```python
def hello(name: str) -> str:
    return f"Hello, {name}"
```

```json
{
  "site": "docsify",
  "theme": "custom"
}
```

### HTML block

<div style="padding:0.5rem; border:1px dashed currentColor; border-radius:6px;">
  HTML preview block for docsify rendering checks.
</div>

### Callout (Docsify theme)

> [!WARNING]
> Verify contrast in both light and dark modes.

### Escaped markdown (literal)

\# Literal heading text

\- Literal list item

### Mustache (docsify-mustache)

Live token example:

Site title from package metadata: {{ package.name }}

Section example:

{{#site}}
Author: {{author}}
{{/site}}

Literal mustache syntax (not rendered):

`{{ package.name }}`

`{{#site}}...{{/site}}`

Notes:

- Mustache values come from `window.$docsify.mustache` config in `docs/index.html`.
- If a token is missing, it renders empty.
</details>

## References

- Docsify main project: https://github.com/docsifyjs/docsify/
- Docsify Mustache plugin: https://docsify-mustache.github.io/#/

