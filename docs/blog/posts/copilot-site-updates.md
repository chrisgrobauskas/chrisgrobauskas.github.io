---
title: Automating Blog Updates with GitHub Copilot (Agent Mode)
date:
    created: 2025-06-22
authors:
    - grobauskas
categories:
    - Automation
    - AI
---

I've been writing more on LinkedIn lately and use Ulysses to keep a local record of those posts.

Recently, I decided to bring that content into my blog. At first, the idea of adding MkDocs headers, setting titles, organizing categories, cleaning up formatting, and splitting content into multiple files felt like a chore!

But GitHub Copilot, running in **agent mode**, turned the process into something fast, iterative, and semi-enjoyable.

> **Note:** Copilot’s agent mode allows it to take actions on your behalf like creating project files, applying custom rules, and responding like an assistant to ask for clarification on steps to take. It does much more than code completion or even suggesting blocks of code.

What pleasantly surprised me was that I wasn’t dealing with code at all, and I plan to explore how this might support other documentation workflows, too.

<!-- more -->

### How Copilot Streamlined My Blog Import Workflow

---

#### Exporting Content

This step was manual. I exported all my LinkedIn posts from Ulysses as a single markdown file, `linkedin.md`, where each post began with an H1 header containing the date. The formatting mostly matched what was in Ulysses, as I already formatted my saved posts this way.

> I had already tagged dates appropriately, which saved some effort. If it hadn’t, I would have needed to add them manually (or figure out how to get Ulysses to do it).

---

#### Creating Context with `AI.md`

I started by asking Copilot to generate a rough draft of an `AI.md` file to be used to document site quality, style, and tone guidelines. I then tailored it to fit my blog, including an author bio to guide tone and context.

The following is a summary:

- **Clarity:** Use concise language, explain technical terms, and avoid unnecessary jargon.
- **Acronyms:** Define acronyms with their full meaning in parentheses (e.g., PWA (Progressive Web Application)).
- **Structure:** Organize articles using headings, subheadings, and bullet points for better readability.
- **Code Blocks:** Format code properly for Markdown, and specify the language for syntax highlighting.
- **Links:** Use descriptive text for links and verify all URLs for accuracy.
- **Tone:** Maintain a professional, approachable tone; humor is acceptable but should align with the site's style.
- **MkDocs Formatting:** Include metadata headers and a "more" tag to separate the lead from the body of the article.
- **Style:** Avoid emoji bullets, proofread for errors, and update outdated information.
- **Author:** A description of the author of the site.

This input gave Copilot a reliable reference point for consistent output and tone.

---

#### Editing the Blog Entries

I asked Copilot to convert the `linkedin.md` content into properly formatted blog posts, using the rules in `AI.md` as a guide. I referenced the rules directly with a file hash (e.g., `#AI.md`) to make sure it obeyed the rules.

> Note: It will show up as `#file:AI.md` in the prompt window as Copilot adds the file: prefix on its own.

**The process was iterative**: 

When I noticed emojis used as list bullets, I updated the rules in `AI.md` and reran the edits. I followed the same pattern for other style issues: refine the rules, then ask Copilot to reprocess the file.

---

#### Creating and Organizing Missing Posts

Once the formatting was consistent, I asked Copilot to analyze the `#posts` and compare existing blog entries against the newly converted content. For any posts missing from the `#posts` directory, I instructed it to create new markdown files, named and formatted according to the latest `AI.md` rules.

This step was surprisingly smooth and saved me a significant amount of time.

---

#### Review and Editing

Of course, I proofread the output manually and reviewed everything locally using `mkdocs serve`. But Copilot handled the repetitive formatting and restructuring tasks with precision.

Using agent mode in this context turned what could have been a tedious migration into a structured, manageable process.

---

### Want to See the Rules?

You can view the actual [`AI.md`](https://github.com/chrisgrobauskas/chrisgrobauskas.github.io/blob/master/AI.md) file I used to guide Copilot.

---

### The Prompts I Used

Here are the rough prompts I gave Copilot throughout the process:

- Reformat the posts in `#linkedin.md` as a set of posts based on the date headers.
- Correct any formatting that does not match the `#AI.md` rules.
- Review the `#linkedin.md` file and make the language and tone consistent with the `#posts` entries already present. Apply `#AI.md` rules as well.
- For the list of posts in `#linkedin.md` take them and if they are not a duplicate to a `#posts` entry then create a new appropriately named markdown file for each blog post created.

> I cleaned these up slightly for grammar, but Copilot isn't concerned with perfect punctuation or capitalization. What matters most is that you express what you want.

--- 

### Final Thoughts

It’s always up to you to approve, refine, or reject Copilot’s suggestions.

If you don't want Copilot to edit something, you can ask for suggestions instead without letting it make automatic changes.

In my case, the editing of actual text was light, whereas the tedious bits were almost completely automated.