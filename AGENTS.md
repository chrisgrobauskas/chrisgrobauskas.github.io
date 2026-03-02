# AGENTS.md

Personal Docsify site with source/deploy split.

## Source of truth

- Edit `docs/`.
- `public/` is generated output only.
- Important! Do not treat `public/` as source unless explicitly asked.

## Safety

Before non-trivial changes, run:

```bash
bash scripts/backup-site.sh
```

After changes:

```bash
bash scripts/deploy-site.sh
```

## Core commands

```bash
# Refresh vendored assets
bash scripts/vendor-js.sh

# Generate blog listing + RSS
python scripts/generate-blog.py

# Build deploy output (also runs generation)
bash scripts/deploy-site.sh

# Create a new post from template
python scripts/new-blog-post.py "Post Title"
# Also valid when no options are used
python scripts/new-blog-post.py Post Title
```

## Script expectations

- `scripts/vendor-js.sh` populates `docs/vendor/`
- `scripts/generate-blog.py` rebuilds `docs/blog.md`, `docs/index.xml`, and `docs/tags.md` from `docs/blog/**/*.md`
- Generated `docs/blog.md` uses plain H2 titles and an HTML `Read More` route link below each excerpt
- `scripts/new-blog-post.py` creates a new dated post from `templates/blog-template.md`
- `scripts/deploy-site.sh` runs generation, then copies `docs/` to `public/`
- `scripts/backup-site.sh` backs up `docs/` by default

If directory structure changes, update scripts immediately.

## Structure

- `docs/blog/YYYY/*.md` -> post source files
- `docs/blog.md` -> generated listing (do not hand-edit)
- `docs/index.xml` -> generated RSS (do not hand-edit)
- `docs/tags.md` -> generated tags index (do not hand-edit)
- `docs/_site.url` -> canonical URL for RSS links

## Blog generation rules

- Sort by front matter `date` descending.
- Skip `draft: true`.
- Excerpt is text above `<!-- more -->`.
- Listing uses plain H2 titles + HTML `Read More` route links.
- Route format: `/#/YYYY/post-file-name-without-md`.
- RSS links are absolute and based on `_site.url`.

## New post helper

- Unquoted multi-word titles work only when no options are passed.
- If options are used (`--date`, `--tags`, `--publish`, etc.), quote multi-word titles.
- Front matter keys are normalised to lowercase on parse; post files may use any key casing.

## Editing rules

- Keep edits minimal and focused.
- Preserve existing behavior unless change is requested.
- Keep CSS token-driven in `docs/assets/docs/custom.css`.
- Preserve accessibility (focus styles, contrast, readability).

## Documentation rules

- Keep writing concise and practical.
- Update `_sidebar.md` when pages change.
- Use `<!-- {docsify-ignore} -->` for pages that should not be indexed.
- Use `<!-- more -->` in blog posts to show the above-the-fold content.

## CI / deploy

- GitLab Pages publishes from `public/`.
- Keep `.gitlab-ci.yml` simple and publish from `public/`.
- CI runs `scripts/generate-blog.py` before publish.
- Ensure `public/` reflects latest `docs/` before deployment checks.
- Rebuild output before relying on local previews.

## Guardrails

- Keep changes small and reversible.
- Avoid unnecessary dependencies.
- Prefer stable relative paths (GitLab Pages compatibility).
- Keep CSS token-driven in `docs/assets/docs/custom.css`.
- Keep docs and scripts in sync.
- Record major structure/style decisions in `docs/site-guide.md`.
- Treat front matter keys and boolean values as case-insensitive; script comparisons must use lowercase or `re.IGNORECASE`.
- Always capitalize "Mainframe" and "Internet" as proper nouns when referring to the platform or network.
- Never store credentials or secrets in the repository; use environment variables or GitLab CI/CD secrets instead.

## Voice

- This is a personal project, so the tone is informal, conversational, and friendly.
- Use first-person pronouns ("I", "my") when referring to the project or personal experiences.
- Use second-person pronouns ("you") when giving instructions or advice to the reader.
- Avoid technical jargon or explain it clearly when necessary.
- Use humor and anecdotes to make the content engaging and relatable.
- Be concise and to the point, but also provide enough context for clarity.
- Use active voice and direct language to create a sense of immediacy and connection with the reader.

## Style

- See: `style-guide.md` for detailed style guidelines.
- See: `styles/grobauskas.md` for personal writing style preferences.
