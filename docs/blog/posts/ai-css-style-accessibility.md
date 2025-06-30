---
title: "AI CSS Style Accessibility"
date: 
  created: 2025-06-26
  updated: 2025-06-30
authors: 
  - grobauskas
categories:
  - accessibility
  - CSS
  - AI
---

> Updated June 30th, 2025

A few days ago, I used GitHub Copilot to help create a custom dark theme for a MkDocs Material site.

Copilot did a good job interpreting CSS selectors, but the resulting theme’s accessibility was poor. Even when I nudged it toward better choices, some text ended up barely readable with low contrast to the background.

<!-- more -->
I took this on as an experiment for a few reasons:

1. I’m not great at choosing color palettes.

2. The MkDocs Material theme exposes a lot of selectors for customization.

3. I’ve built a custom dark theme for MkDocs before and remember it being tricky.

After sharing the experience on LinkedIn, I found I wasn’t alone. Others had run into similar issues but were able to improve things with trial and error.

### My Second Attempt
Taking that feedback to heart, I gave it another go. I generated my site with `mkdocs build` and fed the output into Copilot for context. That didn’t seem to influence results much.

So I took a more hands-on approach: I reviewed the documentation, inspected the HTML, and identified the specific selectors I wanted to style. When I asked Copilot for suggestions with more specific prompts including the selector names, the results improved.

I also found I could ask Copilot to pick colors that met WCAG (Web Content Accessibility Guidelines) contrast standards.

Even then, I often had to provide a base color and ask Copilot to adjust it (e.g., "make this darker" or "suggest a contrasting color for this background").

One area where Copilot really shined was styling code blocks. I provided a single selector and a background color, and it filled in the rest with sensible, readable styles. That was a pleasant surprise.

In the end, Copilot isn’t an “easy button” or magic; it’s an assistant. That wasn’t a surprise, but I had hoped for a bit more. Ultimately, my expectations were too high.

### The Result
If you're interested in the result, you can view the [custom stylesheet](https://github.com/chrisgrobauskas/chrisgrobauskas.github.io/blob/master/docs/assets/stylesheets/extra.css) on Github where I host my blog.



