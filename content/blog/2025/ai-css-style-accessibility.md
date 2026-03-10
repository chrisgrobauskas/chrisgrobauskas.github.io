---
title: "AI, CSS, and Accessibility"
description: "AI-generated CSS can fail basic accessibility standards. Specific inputs and explicit constraints produce better results."
author: "Chris Grobauskas"
date: "2025-06-26"
updated: "2026-02-27"
tags:
  - Accessibility
  - CSS
  - AI
  - GenAI
---

I used GitHub Copilot to help create a custom dark theme for a MkDocs Material site. Copilot did a good job interpreting CSS selectors (the rules that target specific HTML elements for styling), but the resulting theme's accessibility was poor. Even when I nudged it toward better choices, some text ended up barely readable with low contrast to the background.

<!-- more -->

I took this on as an experiment because I'm not great at choosing color palettes, the MkDocs Material theme exposes a lot of selectors for customization, and I've built a custom dark theme for MkDocs before and remember it being tricky. After sharing the experience on LinkedIn, I found I wasn't alone. Others had run into similar issues but were able to improve things with trial and error.

That experience is a proxy for any developer working outside their design expertise. GenAI lowers the barrier to entry into UI work. Developers who would never have attempted a custom theme before will now. That's genuinely good. But it also means the person reviewing the output often doesn't have the design eye to catch what went wrong.

## What Didn't Work

My first instinct was to give Copilot broad instructions: "create a dark theme for MkDocs Material." The output looked reasonable at a glance, but failed basic contrast checks. Text on dark backgrounds was muddy. Link colors blended into surrounding text.

I tried generating the site with `mkdocs build` and feeding the output into Copilot for more context. That didn't seem to influence results much.

## Be Specific

The results improved when I stopped asking for a theme and started asking about specific selectors. I reviewed the documentation, inspected the HTML, and identified the exact selectors I wanted to style. When I asked Copilot for suggestions with those selector names in the prompt, the output got noticeably better.

I also found I could ask Copilot to pick colors that met WCAG (Web Content Accessibility Guidelines) contrast standards. Even then, I often had to provide a base color and ask Copilot to adjust it (e.g., "make this darker" or "suggest a contrasting color for this background").

When we give our AI assistant a specific target, an explicit constraint, and verify the result, we get better output from fewer rounds. We also avoid the back-and-forth of "no, not that ... I meant *this*."

## Why This Matters Beyond My Blog

> **For decision-makers:** If your team uses AI to generate front-end code, the output may not meet accessibility standards. WCAG violations are not just a design preference; it's also a duty of care and in some jurisdictions a legal requirement. 

We should care whether all people can easily use our products. Someone needs to verify the output, and that someone needs to know what to check.

The deeper issue is who is in the loop. The same democratization that makes GenAI appealing to developers like me who aren't designers also means the human reviewing the output often lacks the expertise to catch what's wrong. A [human in the loop](/blog/2023/human-in-the-loop/) needs enough competence in the domain they're reviewing to recognize a failure. If no one on your team would have caught a contrast failure before using AI, they still won't after.

The fair pushback is that I got better results when I gave better inputs. That's true. But the default output still failed basic accessibility checks, and most users won't know enough CSS to course-correct. GenAI is an assistant, not an easy button ... a human still needs to validate and own the outcomes.

## Before You Ship AI-Generated Styles

- **Name your selectors.** Don't ask for "a dark theme." Identify the specific selectors you want to change and include them in the prompt.
- **State the constraint explicitly.** Ask for WCAG AA or higher contrast compliance. If you don't ask, the model won't prioritize it.
- **Verify the output.** Run the result through a contrast checker. Browser dev tools have [built-in contrast audits](https://learn.microsoft.com/en-us/microsoft-edge/devtools/accessibility/color-picker).
- **Provide a base color.** Giving the model a starting point ("use `#1a1a2e` as the background, suggest a readable text color") produces better results than open-ended requests.

AI-assisted styling works, but only when you bring enough knowledge to steer it. The pattern keeps showing up: the more specific your input, the more useful the output.

## Links

- [Human in the Loop](/blog/2023/human-in-the-loop/) - when AI decisions need human oversight and why the reviewer needs domain competence to catch failures
- [The GenAI Arc](/blog/2025/genai-arc/) - the democratization promise and threat vector of GenAI systems
- [WCAG Contrast Checker - WebAIM](https://webaim.org/resources/contrastchecker/) - verify color contrast against accessibility standards
- [Built-in contrast audits in Edge DevTools](https://learn.microsoft.com/en-us/microsoft-edge/devtools/accessibility/color-picker) - browser-based contrast checking without extra tools
- [MkDocs Material - Customization](https://squidfunk.github.io/mkdocs-material/customization/) - reference for CSS selectors and theme overrides