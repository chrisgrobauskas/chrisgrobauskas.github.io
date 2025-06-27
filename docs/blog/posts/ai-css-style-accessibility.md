---
title: "AI CSS Style Accessibility"
date: 
  created: 2025-06-26
  updated: 2025-06-27
authors: 
  - grobauskas
categories:
  - accessibility
  - css
  - ai
---

Tonight I used Copilot to create a custom dark theme for a MkDocs Material site.

It understood the CSS selectors well, but the accessibility of the result was poor. Despite guiding it toward specific colors, the contrast was so low in places that text became unreadable.

<!-- more -->

I took this on as an experiment because:

1. I’m not great at choosing color palettes.
2. The MkDocs Material theme has plenty of selectors to tune.
3. I’ve created a custom dark theme with MkDocs before and know it’s tricky.

Seeking feedback on LinkedIn, I found that others had similar issues. However, with iteration and refining their prompts, they achieved better results.

### Future Efforts
I plan to try feeding the actual MkDocs build output into Copilot as context. It feels like a bit of a workaround, but it might give Copilot the structure it needs to make better styling decisions.

I will update this blog post after I have time to give it a try.