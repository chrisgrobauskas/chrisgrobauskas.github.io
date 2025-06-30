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

While Copilot did a solid job interpreting CSS selectors, the accessibility of the resulting theme was poor. Even when I steered Copilot to color choices the contrast was often too low, leaving some text barely readable.

<!-- more -->

I took this on as an experiment for a few reasons:

1. I’m not great at choosing color palettes.
2. The MkDocs Material theme exposes a lot of selectors for customization.
3. I’ve built a custom dark theme for MkDocs before and remember it being finicky.

After sharing my experience on LinkedIn, I learned I wasn't alone. Others had encountered similar issues, but they found that with trial and error they could improve on their results.

### What I found

Taking that feedback to heart, I gave it another go. I generated the site using `mkdocs build` and fed the output into Copilot as context. This didn’t seem to influence the results much.

Next, I dug into the documentation and reviewed the generated HTML to identify the selectors I wanted to style. By providing Copilot specific tags for styling suggestions the results were better. I also found I could ask for help choosing colors to meet WCAG (Web Content Accessibility Guidelines) standards for contrast. 

Providing these hints was more effective, but it was still far from seamless. In the end, I had to choose the colors I wanted to start with, and I could then ask for copilot to make the color darker or lighter. Or to provide a contrasting color for a given background.

The one section it was very good at was providing styling for code blocks. I was able to provide one selector, and then copilot filled out the rest when given a background. The choices were all "sane" and readable which was a pleasant surprise..

Copilot is not an "easy button" or magical; it is an assistant. While this was not a surprise, it was disappointing. So, in the end I learned that my expectation were too high.