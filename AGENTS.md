# AGENTS.md

Personal Hugo site (PaperMod theme) with source in `content/` and build output in `public/`.

## Source of truth

- Edit `content/`.
- `public/` is generated output only (`hugo --minify`).
- Important! Do not treat `public/` as source unless explicitly asked.

## Safety

Before non-trivial changes, run:

```bash
bash scripts/backup-site.sh
```

After changes, build and preview:

```bash
hugo server -D    # local preview (includes drafts)
hugo --minify     # production build → public/
```

## Core commands

```bash
# Local development server (includes drafts)
# -D (--buildDrafts) renders posts with `draft: true` in front matter.
# Without -D, draft posts are excluded — use this for production-like preview.
hugo server -D

# Production build
hugo --minify

# Create a new blog post from archetype
hugo new blog/2026/my-post-title.md

# Back up content
bash scripts/backup-site.sh

# Audit excerpt markers
python scripts/audit-more-tags.py

# Audit non-ASCII characters
python scripts/audit-unicode.py [--fix]
```

## Structure

- `content/blog/YYYY/*.md` → blog post source files
- `content/about.md` → about page
- `content/resume.md` → resume page
- `content/site-guide.md` → site guide
- `content/search.md` → search page (PaperMod Fuse.js)
- `content/_index.md` → homepage
- `content/blog/_index.md` → blog section page
- `hugo.toml` → site configuration
- `assets/css/extended/custom.css` → theme colour overrides
- `assets/css/extended/syntax.css` → code syntax token colours
- `layouts/` → Hugo template overrides and render hooks
- `archetypes/blog.md` → new post template
- `static/favicon.svg` → site favicon
- `static/images/grobauskas-profile-small.jpg` → profile avatar
- `themes/PaperMod/` → PaperMod theme (git submodule)
- `alignment/` → writing style alignment for editor review (git submodule: writing-editor)

Front matter keys are normalized to lowercase at parse time. Scripts and templates may use any key casing; all comparisons must be case-insensitive or lowercased.

If directory structure changes, update scripts immediately.

## Blog rules

- Sort by front matter `date` descending.
- Skip `draft: true`.
- Excerpt is text above `<!-- more -->` (Hugo's native `.Summary` split).
- URL format: `/blog/YYYY/post-slug/`.
- RSS feed generated automatically at `/index.xml`.
- Tags taxonomy at `/tags/`.

## New post

```bash
hugo new blog/2026/my-post-title.md
```

This creates a new post from `archetypes/blog.md` with pre-filled front matter and `draft: true`.

## Editing rules

- Keep edits minimal and focused.
- Preserve existing behavior unless change is requested.
- Keep CSS token-driven in `assets/css/extended/custom.css`.
- Preserve accessibility (focus styles, contrast, readability).

## Documentation rules

- Keep writing concise and practical.
- Update `hugo.toml` menu when pages change.
- Use `<!-- more -->` in blog posts to define the excerpt.

## CI / deploy

- GitHub Pages publishes from `public/` via GitHub Actions.
- `.github/workflows/deploy.yml` checks out submodules, runs `hugo --minify`, copies CNAME, deploys.
- PaperMod theme and alignment/ are git submodules — use `git submodule update --init --recursive` after clone.

## Guardrails

- Keep changes small and reversible.
- When working from a checklist, mark items done (`- [x]`) and ~~strikethrough~~ as you complete them.
- Avoid unnecessary dependencies.
- Prefer stable relative paths (GitHub Pages compatibility).
- Keep CSS token-driven in `assets/css/extended/custom.css`.
- Keep content and scripts in sync.
- Record major structure/style decisions in `content/site-guide.md`.
- Treat front matter keys and boolean values as case-insensitive; never hardcode case-sensitive matches against front matter fields.
- Always capitalize "Mainframe" and "Internet" as proper nouns when referring to the platform or network.
- Never store credentials or secrets in the repository; use environment variables or GitHub Actions secrets instead.

## Voice

- This is a personal project, so the tone is informal, conversational, and friendly.
- Use first-person pronouns ("I", "my") when referring to the project or personal experiences.
- Use second-person pronouns ("you") when giving instructions or advice to the reader.
- Avoid technical jargon or explain it clearly when necessary.
- Use humor and anecdotes to make the content engaging and relatable.
- Be concise and to the point, but also provide enough context for clarity.
- Use active voice and direct language to create a sense of immediacy and connection with the reader.

## Style

- See: `content/site-guide.md` for detailed style guidelines.
- See: `alignment/grobauskas.md` for personal writing style preferences.
