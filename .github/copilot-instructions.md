# Copilot Instructions

Personal Docsify site with source/deploy split.

## Repository model

- Source: `docs/`
- Deploy output: `public/` (generated)
- Do not treat `public/` as source unless explicitly asked.

## Mandatory workflow

Before major edits:

```bash
bash scripts/backup-site.sh
```

After changes:

```bash
bash scripts/deploy-site.sh
```

## Script expectations

- `scripts/vendor-js.sh` populates `docs/vendor/`
- `scripts/generate-blog.py` rebuilds `docs/blog.md`, `docs/index.xml`, and `docs/tags.md` from `docs/blog/**/*.md`
- Generated `docs/blog.md` uses plain H2 titles and an HTML `Read More` route link below each excerpt
- `scripts/new-blog-post.py` creates a new dated post from `templates/blog-template.md`
- `scripts/deploy-site.sh` runs generation, then copies `docs/` to `public/`
- `scripts/backup-site.sh` backs up `docs/` by default

`scripts/new-blog-post.py` supports unquoted multi-word titles when no options are passed.
When using options (`--date`, `--tags`, etc.), quote multi-word titles.

Front matter keys are normalized to lowercase at parse time. Scripts and templates may use any key casing; all comparisons must be case-insensitive or lowercased.

If directory structure changes, update scripts immediately.

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

## Deployment rules

- Keep `.gitlab-ci.yml` simple and publish from `public/`.
- Ensure blog generation runs before publish.
- Ensure `public/` reflects latest `docs/` before deployment checks.

## Guardrails

- Avoid unnecessary dependencies.
- Prefer stable relative paths (GitLab Pages compatibility).
- Keep scripts and docs in sync.
- Treat front matter keys and boolean values as case-insensitive; never hardcode case-sensitive matches against front matter fields.
- Always capitalize "Mainframe" and "Internet" as proper nouns when referring to the platform or network.
- Never stored credentials or secrets in the repository; use environment variables or GitLab CI/CD secrets instead.

# Voice

- This is a personal project, so the tone is informal, conversational, and friendly.
- Use first-person pronouns ("I", "my") when referring to the project or personal experiences.
- Use second-person pronouns ("you") when giving instructions or advice to the reader.
- Avoid technical jargon or explain it clearly when necessary.
- Use humor and anecdotes to make the content engaging and relatable.
- Be concise and to the point, but also provide enough context for clarity.
- Use active voice and direct language to create a sense of immediacy and connection with the reader.

# Style

- See: `style-guide.md` for detailed style guidelines.
- See: `styles/grobauskas.md` for personal writing style preferences.
