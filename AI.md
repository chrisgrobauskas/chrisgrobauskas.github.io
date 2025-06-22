# Context for Editing Blog Articles

This document provides essential context and guidelines for editing blog articles on this site. Follow these instructions to ensure consistency, clarity, and quality in all published content.

## 1. Purpose

- Maintain a high standard of technical accuracy and readability.
- Ensure articles align with the site's style and objectives.
- Facilitate collaboration among contributors.

## 2. Prerequisites

- Familiarity with Markdown syntax.
- Access to the site's repository and editing permissions.
- Understanding of the target audience and blog topics.

## 3. Editing Guidelines

- **Clarity:** Use clear, concise language. Avoid jargon unless necessary, and explain technical terms. 
- **Acronyms:** Always put the meaning for acronyms in parentheses after the acronym. For example: PWA (Progressive Web Application).
- **Structure:** Organize articles with headings, subheadings, and bullet points where appropriate.
- **Code:** Format code blocks properly and test all code snippets for accuracy. Include the language for the markdown to enhance highlighting.
- **Links:** Use descriptive text for links and verify that all URLs are valid.
- **Tone:** Maintain a professional and approachable tone.

## 4. Site Formatting
- **MkDocs Blog Headers:** This is an mkdocs based blog. Use appropriate headers for all blog entries

```
---
title: the title
date: 
  created: YYYY-MM-DD
  updated: YYYY-MM-DD
authors: 
  - grobauskas
categories:
  - the category
---
```

- **MkDocs Blog More Tag:** Use a more tag to separate the lead from the body of each blog entry.

```
<!-- more -->
```
- **Style Considerations:**
  - Do not use emojis for bullet points, prefer markdown formatting as needed.
  - If emoji's are used changed them to appropriate mkdocs placeholders for the emojis.
  - DB2 should be Db2 with a lower-case b per IBM.
  - Z/OS, ZOS, OS/390, OS390, MVS should be changes to z/OS unless used in a historical context.
  - Mainframe commands should normally be capitalized, for example: ISPF, JCL, etc.
  - The word Mainframe should be capitalized.
  - Remove hashtags when not used inline in a paragraph or bullet point.
  - Do not duplicate a blog header as a H1 markdown tag. The title should be used instead and the H1 should only be present as a sub-header if it provieds additional context.
  
## 4. Best Practices

- Proofread for grammar, spelling, and formatting errors.
- Update outdated information and remove redundant content.
- Add relevant images or diagrams to enhance understanding.
- Attribute sources where necessary.

## 5. Troubleshooting

- If you encounter issues with formatting or rendering, preview the article before publishing.
- For repository access or permission problems, contact the site maintainer.
- Refer to the [Markdown Guide](https://www.markdownguide.org/) for syntax help.

---

For further assistance, reach out to the site maintainer or consult the contributor documentation.

---

# Blog Author Background

- Chris Grobauskas, Senior Technology Engineer at State Farm Insurance

Chris Grobauskas is a senior technology engineer with 25 years of experience working across Linux, Mainframe, AWS, and a variety of other platforms. His background is in enterprise system development and modernization. 

Over the years, Chris has moved from development into architecture, framework support, infrastructure, and database roles — including managing Linux clusters and working as a Db2 z/OS DBA. 

More recently, he’s been focused on platform modernization, helping to re-platform the world’s largest property and casualty claim system. 

Chris aims to keep things clear and approachable, sharing insights from his journey in tech without making things overly formal. His style is approachable, helpful, and friendly.

Chris also beleives in keeping things lighthearted and enjoying work individually and as a team. Humor is OK and _is professional_.


