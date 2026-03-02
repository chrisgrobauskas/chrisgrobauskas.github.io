# Writing Style Guide — Chris Grobauskas

Actionable instructions for Staff+ communication. Influence decision-makers. Share experience across domains. Stay human.

**Topics**: Leadership, Systems Thinking, Systems Design, Database Engineering, AI, Knowledge Transfer, Modernization, Technical History
**Audience**: Architects, leaders making investment decisions, and practitioners. Write so both can act.
**Influences**: Seth Godin (brevity), Michael Lopp/Rands (conversational depth), Bruce Schneier (expert amplification with judgment)

---

## Voice

- Technical precision with approachable analogies. Explain, never gatekeep.
- Teacher-practitioner: 25+ years shared without ego.
- Dry humor, historical parallels, memorable quotes. Never sarcasm.
- Professional and kind. No profanity. No alarmism.
- Formality: 7/10. Authoritative with personality.
- Emojis: avoid, except ♥️ and ☺️ sparingly.
- First person ("I", "my") for experience. Second person ("you") for advice.

**Voice examples:**
- "Beware the 'cake in the break area' trap."
- "Database contention is vexing because it is normally NOT a database issue!"
- "Legacy engineers keep the present running while the future is still being built."
- "How do you make space for safe exploration on your team? More importantly, how do you help people feel safe doing it?"

---

## Rules

### Always

- **Show reasoning, not just conclusions.** "I recommend X because Y. The cost of not doing it is Z."
- **Connect technical decisions to organizational and business outcomes.** Every technical post needs at least one paragraph a non-technical leader can follow.
- **Steelman the opposing view** before taking a position. Every post that takes a technical stance.
- **Name your frameworks.** Unnamed advice doesn't propagate. ("cake in the break area trap", "reversibility test") Target 1-2 named concepts per quarter.
- **Provide decision criteria, not "it depends."** Give readers the questions to ask so they can decide for their context.
- **Prose for analysis, bullets for enumeration only.** Bullets list items, steps, options. Prose shows how you got there.
- **Hook in the first 100 words.** Scenario, question, historical parallel, or emphatic declaration.
- **End when the thought completes.** No sign-off. No signature. No filler close.
- **Attribute all quotes. Explain jargon on first use.**
- **Link generously** to experts, resources, and your own related posts. Every post has at least one external link.

### Never

- Buzzwords without substance
- Jargon without explanation
- Euphemisms that hide problems
- Academic verbosity
- Ending with just "it depends" or "choose what is best"
- Overstating a case; seek balance
- Em-dashes or en-dashes; use ellipsis (...) for pauses

### When sharing others' work

- Add your position: what's right, what's missing, what you'd add from experience.
- Your judgment is the value-add, not the link.
- Close with a one-sentence takeaway beyond the link.

### When writing technical posts

- Frame as an organizational problem, not just a technical one.
- Name the tradeoffs explicitly: the cost of each option.
- Include a blockquote callout for the key decision-maker takeaway.

### When writing leadership posts

- Address both audiences with separate H2 sections: "If You're Leading..." / "If You Support..."
- Specific actions for each group (4-6 bullets).
- Acknowledge constraints honestly.

---

## Structure

- **Paragraphs**: 1-2 sentences for emphasis. 3-5 sentences for analytical reasoning.
- **Headers**: H2 for major sections. H3 for subsections.
- **Blockquotes**: `>` for key takeaways scannable by decision-makers.
- **White space**: Generous. Fast, scannable reading.
- **Sentences**: ~17 words average. Active voice 85%+. Mix punchy declarations with technical explanations.
- **Read time**: 1-12 minutes. Most posts 2-6 min. 2-3 deep posts per quarter (8-12 min).

---

## Rhetorical Toolkit

Use deliberately. Not every post needs all of these.

1. **Historical Parallel** — Past event illuminates present challenge. Makes technical topics accessible through story.
2. **Setup-then-Challenge** — State common belief, then question it. ("The platform is out-of-date" ... "But is that the real problem?")
3. **Revealing Question** — A question that reframes the problem. "Why was it so slow?" leads to systems thinking, not just debugging.
4. **Steelman** — Acknowledge the strongest opposing view, then show where it breaks. Builds trust with decision-makers who look for holes.
5. **Organizational Bridge** — Connect a technical decision to org cost. "Contention doesn't just cause timeouts ... it causes on-call fatigue that burns out your best engineers."
6. **Named Framework** — Package reusable concepts with memorable names. Named frameworks propagate; unnamed advice doesn't.
7. **Decision Framework** — Give structured questions that resolve "it depends." "Ask: (1) What's the blast radius? (2) Do I have a fallback? (3) Is the failure recoverable? The answers pick the strategy."
8. **Serial Arc** — Link related posts. Name the arc. Shows you hold the full technical narrative.
9. **Dual Question Close** — Practical question, then deeper one. Use only when it adds value.
10. **Twist Ending** — Unexpected angle in the final lines. Rewards reading to the end.
11. **Quote as Principle** — Memorable quote that crystallizes the point. Attribute always.

---

## Post Templates

### Synthesis (250-400 words, 2-3 min)

1. Why it matters now (1-2 sentences)
2. Your position: what's right, what's missing, what you'd add (3-5 sentences)
3. Connect to reader's context (2-4 sentences)
4. Attribution + link
5. One-sentence takeaway

### Technical with Org Context (600-1000 words, 4-6 min)

1. Scenario framed as an organizational problem (50 words)
2. Revealing question about why it persists
3. 2-3 H2 sections with prose reasoning
4. Steelman the opposing approach
5. Organizational impact (3-5 sentences)
6. Decision framework (structured questions)
7. Blockquote takeaway for decision-makers
8. Stated position with reasoning
9. Links to related posts

### Dual-Audience Leadership (300-500 words, 2 min)

1. Observation about common challenge (50-100 words)
2. Blockquote key insight
3. H2: "If You're [Leading]..." with 4-6 bullet actions
4. H2: "If You're [Practicing]..." with 4-6 bullet actions
5. Inclusive close acknowledging both perspectives

### Cross-Domain Deep Dive (1200-2000 words, 8-12 min)

1. Technical problem most treat as purely technical (50-100 words)
2. Reveal the organizational dimension (100-150 words)
3. Technical argument in prose: reasoning chain, steelman, named tradeoffs (300-500 words)
4. Bridge to organizational impact (200-300 words)
5. Decision framework (100-200 words)
6. Named concept + stated position (50-100 words)
7. Links to related posts in the arc

Write 2-3 of these per quarter.

---

## Content Mix Target

- Synthesis + Link: 30%
- Technical (with org context): 25%
- Leadership/Culture: 20%
- Cross-Domain: 15%
- Historical Lessons: 10%

---

## Quality Check

Before publishing:

- [ ] Reasoning is visible — chain that led to the position, not just the position
- [ ] Technical decisions connected to org/business outcomes
- [ ] Steelman present for any technical position taken
- [ ] Prose for analysis, bullets only for enumeration
- [ ] First 100 words establish relevance
- [ ] Ends when thought completes — no filler close
- [ ] At least one paragraph a non-technical leader can follow
- [ ] At least one external link
- [ ] Active voice 85%+
- [ ] Jargon explained on first use
- [ ] Decision framework provided (not "it depends")
- [ ] Named concept where applicable
- [ ] Scannable: short paragraphs, headers, blockquote takeaways
- [ ] Make writing generic; no company internal references that should not be shared

---