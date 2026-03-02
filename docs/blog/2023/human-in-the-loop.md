---
title: "Human in the Loop"
description: "AI decisions with real consequences need human oversight. Speed is not a defense when being wrong causes real harm."
author: "Chris Grobauskas"
date: "2023-09-09"
updated: "2026-02-27"
tags:
  - AI
  - Standards
---
# Human in the Loop

What if an AI monitored whether you followed all rules and laws that applied to you ... and then acted on what it found?

Not flagged for review. Acted. Put you on a no-fly list. Accused you of fraud. No human involved.

<!-- more -->

That scenario is the subject of Jon Penney's guest post on Bruce Schneier's blog, [AI and Micro-directives](https://www.schneier.com/blog/archives/2023/07/ai-and-microdirectives.html). Penney focuses on the legal risks to the *targets* of AI-based decisions, but the legal exposure cuts both directions. 

> Businesses deploying GenAI systems need to consider whether their AI's outcomes are fair, explainable, and defensible in court.

## When AI Accuses

Consider an AI system that identifies potential fraud. Before anyone acts on its output, three questions matter:

- Is the model accurate and free of systematic bias?
- Can its recommendations be explained to a non-technical reviewer?
- Did a human make the final decision, or did the AI act autonomously?

Accusing someone of fraud is serious. It could end a career, freeze an account, or land someone on a watchlist. A human reviewing a recommendation against other information is far more defensible than an AI acting on its own. The human can catch errors.

## The Speed Objection

The fair objection: requiring a human in every decision loop slows things down and doesn't scale. That's true, and for low-risk, high-volume decisions ... spam filtering, content recommendations, inventory reordering ... full automation is the right call.

But when there are real risks to people, we need to have a human in the loop. Nuclear weapon launch procedures require multiple humans precisely because the consequences are irreversible. The same reasoning applies to any AI decision that could materially harm a person: flag someone as a fraud risk, add them to a no-fly list, or freeze their access to financial services. Speed is not a defense when being wrong causes real harm.

> The question isn't whether AI should make decisions. It's which decisions require a human to own the outcome.

## A Simple Test

When deciding whether a system needs a human in the loop, ask:

- What happens to a person if the AI is wrong?
- Is the decision reversible?
- Would you be comfortable explaining this decision in court?

> If the consequence is significant or the decision is hard to undo ... put a human in the loop.

And don't forget the audit trail. AI decisions need an audit trail the same as any other consequential business action. This is not a new concept; audit trails pre-date AI.

## Accountability

The ACM's [Principles for Responsible Algorithmic Systems](https://www.acm.org/binaries/content/assets/public-policy/ustpc-approved-generative-ai-principles) provide a broader governance framework. It is worth reading alongside Penney's piece because it addresses accountability at the organizational level, not just the technical one.

The most essential principle in the document is listed last:

> "Accountability and responsibility: Public and private bodies should be held accountable for decisions made by algorithms they use, even if it is not feasible to explain in detail how those algorithms produced their results."

## Links

- [AI and Micro-directives - Jon Penney, Schneier on Security](https://www.schneier.com/blog/archives/2023/07/ai-and-microdirectives.html) - the legal risks of AI-based enforcement
- [Principles for Responsible Algorithmic Systems - ACM](https://www.acm.org/binaries/content/assets/public-policy/ustpc-approved-generative-ai-principles) - governance framework for algorithmic accountability