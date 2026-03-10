---
title: Where the Collapsed Lifecycle Breaks
description: "AI agents are collapsing the SDLC for code. But most deployments immediately affect state, opening a corruption window that no deployment strategy closes."
author: "Chris Grobauskas"
date: "2026-03-07"
tags:
  - AI
  - GenAI
  - Database
  - Data Corruption
  - Data Recovery
  - Automation
---

Boris Tane argues in [The Software Development Lifecycle is Dead](https://boristane.com/blog/the-software-development-lifecycle-is-dead/) that AI agents have collapsed the traditional staged software development lifecycle (SDLC) into a single intent-build-observe loop, and that the classic lifecycle is dead.

The tinkerer in me who spent the weekend experimenting with OpenCode and GitHub Copilot wants to believe.

But most systems that matter store state. And the former DBA in me is not convinced we are ready for a fully collapsed lifecycle.

<!-- more -->

The core argument: "AI agents didn't make the SDLC faster. They killed it." The new lifecycle is "Intent. Build. Observe. Repeat." with agents monitoring rollouts, adjusting traffic, and rolling back automatically on errors.

For code, I see it. Agents that compress the feedback loop from days to minutes are already changing how we build software. And maybe Tane is only talking about code deployment.

But in most systems, code deployment changes state. The moment new code handles its first request, it's writing to databases, publishing to queues, and triggering downstream processes. 

> There's no such thing as a code-only deployment for a system that stores state.

What the article doesn't address is what I'll call the **corruption window**: the time between when bad code starts executing and when it's detected and rolled back. During that window, every write is suspect ... corrupted data in databases, communications already sent to customers, and downstream effects that no rollback can undo.

Tane is right that observability is the last line of defense ... and the most important one. The faster you detect a regression, the smaller the corruption window. For code, fast detection means fast rollback and minimal user impact. For data, fast detection is the difference between correcting a few hundred rows and triaging millions. Time to detect is the variable that matters most, for code and data alike.

## Development Is Not Production

For getting code into an integration testing environment, I'm all for it. For low-risk deployments to test, the "intent, build, observe, repeat" cycle works today.

But GenAI-generated code isn't magical. Anyone who has used these tools has encountered code that looked perfect but hid subtle logic errors or missed edge cases.

The real challenge is volume: if we choose, agents can generate code far faster than humans can responsibly review it. Human review doesn't catch every bug, but completely removing it just to unblock the agent's velocity is a dangerous tradeoff. When you collapse the lifecycle and let AI deploy to production without review, you are accepting a higher rate of flawed logic hitting your system.

And most production systems exist to maintain state. Someone, not something, has to be accountable for what ships to those systems. I wrote about why in [Human in the Loop](/blog/2023/human-in-the-loop/). In regulated industries, a human reviewing and approving deployments isn't just prudent ... it's a compliance expectation. [HIPAA](https://www.hhs.gov/hipaa/for-professionals/security/index.html) governs healthcare data, [PCI DSS](https://www.pcisecuritystandards.org/standards/pci-dss/) covers payment systems, and [Sarbanes-Oxley](https://en.wikipedia.org/wiki/Sarbanes%E2%80%93Oxley_Act#Section_404:_Assessment_of_internal_control) mandates internal controls over financial reporting, including IT change management.

## Code Rollbacks Don't Fix State

Sophisticated deployment strategies ... blue/green deployments, canary rollouts (routing a small percentage of traffic to the new version first), feature flags (enabling new behavior for a controlled subset of users), automatic rollbacks ... limit the blast radius of a bad code release. They shrink the corruption window. They don't eliminate it.

This is the [reversibility test](/blog/2025/willing-to-fail/) the piece doesn't address: code can be rolled back. Corrupted data frequently cannot.

The consequences extend well beyond outages. Insurance systems affect whether someone can get to work after their car is totaled. Broken healthcare systems can delay treatment or expose deeply sensitive histories. Financial platforms move money people depend on. For systems like these, a poorly executed automated deployment risks real harm to real people.

And some failures are completely irreversible. Leaked sensitive data can lead to identity theft years later. You can roll back a deployment. You cannot un-leak data.

The organizational costs compound beyond engineering time. Data corruption and breach incidents erode customer trust, invite regulatory scrutiny, and create legal exposure. A breach notification or audit finding doesn't just cost money ... it costs reputation that takes years to rebuild. The engineering team's ability to surgically recover corrupted data is something leadership should understand before changing what reviews are required for changes.

### Corruption Propagates

The article asks us to imagine agents that "detect the regression and fix it." But someone still has to decide which corrupted data needs remediation and how to do it safely.

Corrupted data doesn't stay in one place. It propagates across systems, gets saved, transmitted, and consumed downstream. You can't fix it with a system rollback or database restore because that also undoes the good updates that happened in the same window. The failure modes get more complex when transactions span services ... I wrote about that in [Distributed Transactions](/blog/2025/transactions/).

Backups are essential, but they're a blunt instrument for corruption caused by a bad deployment. A restore rolls the entire database back. Every valid write after that point ... new customer orders, payment confirmations, status updates ... is lost along with the corrupted data. Good and bad updates happen during the same window, and a restore cannot selectively revert only the bad data.

The only way around this is surgical: identify exactly which rows were affected and correct only those. Today, that requires human triage.

### Deployment and Audit Strategies Don't Close the Corruption Window

Blue/green deployments, dark launches (running new code against production traffic without exposing results to users), and feature flags control which code path serves a request. For stateless services, they work as designed. But when these code paths share a database, writes from the new path are committed to shared state during the corruption window. Switching traffic back reverts the code path ... it doesn't undo the writes.

Change Data Capture (CDC) streams a record for every database change. That sounds like it should solve the problem. In practice, CDC gives you logs, not answers. A production database might see thousands of writes per second. Identifying which writes were caused by a bug versus normal operations requires understanding the business logic, the failure mode, and the downstream effects. No current system does this automatically.

Patterns like append-only ledgers, saga-based compensation, and event-sourced architectures can narrow the exposure further. But they narrow it; they don't close it. Each requires careful design upfront, and none automatically determine which writes were corrupted versus correct. These tools are valuable for compliance and forensics. They are not automatic recovery mechanisms.

## Before You Collapse the Lifecycle

Before adopting an agent-driven deploy loop for production systems that store state, ask these questions:

- **Does your system write state?** Stateless services and read-only systems are better candidates.
- **Can that state be surgically recovered?** If a bad deployment corrupts data, do you have the tooling and expertise to identify exactly what changed, roll back _only_ the bad writes, and verify integrity?
- **Are there external systems involved?** If your system is linked to others, you may not be able to control recovery in downstream systems. What consequences will there be for your customers if you cannot fix everything?
- **Who is accountable?** When the agent gets it wrong, someone still has to explain what happened and fix it. If that person doesn't exist or no longer holds the context, you have a gap no amount of automation closes.
- **What is your regulatory environment?** If your system holds sensitive healthcare or financial data, you have a higher standard to meet for reviewing what goes into your production environments.

## GenAI Won't Close the Corruption Window

The obvious next move is to reach for GenAI: let an agent analyze the change stream, identify the bad writes, and propose corrections. I hope to see cases where automated reasoning can assist data engineers and DBAs during a recovery.

But GenAI tools shouldn't be the sole decision-makers here. The data needed to determine what to fix is situational, shaped by business rules, system history, and context that isn't in the change stream. GenAI's confidence can exceed its accuracy, and when it gets a recovery wrong, no one is automatically accountable for what breaks next.

The collaborative loop that works well in coding ... try something, observe the result, iterate ... is dangerous when applied to production databases. A wrong attempt doesn't just fail to fix the problem. It compounds the original damage, layering new inconsistencies that make eventual human intervention significantly harder.

## Context Requires Stewardship

In [The GenAI Arc](/blog/2025/genai-arc/), I argued that what makes agentic AI's blast radius larger than earlier automation is that it reaches data, not just code. If you automate reasoning about a system, you also stop building mental models of it. The knowledge that comes from design reviews, reading code, and supporting systems in production doesn't transfer automatically. When a serious data issue eventually arrives, the human nominally in the loop may no longer have the context to fix it.

Recovery requires someone who owns the data ... not just the schema, but the meaning. Someone who knows which values are valid, which relationships must hold, and what downstream systems assume about consistency.

Data lineage, quality, and metadata tools can help trace where corruption spread and what went wrong. But they map the blast radius ... they don't decide what to fix. That judgment isn't a skill you can acquire during an incident. It's built over time by the people who design, build, and operate the system.

You can automate code generation. You can accelerate delivery. You can compress the lifecycle.

> You cannot automate accountability.

## Links

- [The Software Development Lifecycle is Dead - Boris Tane](https://boristane.com/blog/the-software-development-lifecycle-is-dead/) - the original piece this post responds to
- [Distributed Transactions](/blog/2025/transactions/) - transaction strategies and failure behavior across distributed systems
- [The GenAI Arc](/blog/2025/genai-arc/) - why agentic AI's blast radius is larger when it reaches data, not just code
- [Human in the Loop](/blog/2023/human-in-the-loop/) - why accountability requires a human reviewing and approving what ships
- [Willing to Fail](/blog/2025/willing-to-fail/) - the reversibility test: know whether a change is reversible before you make it
- [Bridging the Knowledge Chasm](/blog/2025/bridging-knowledge-chasm/) - what happens when institutional knowledge walks out the door
- [Sarbanes-Oxley Act Section 404 - Wikipedia](https://en.wikipedia.org/wiki/Sarbanes%E2%80%93Oxley_Act#Section_404:_Assessment_of_internal_control) - internal control requirements over financial reporting systems, including IT change management
- [HIPAA Security Rule - HHS](https://www.hhs.gov/hipaa/for-professionals/security/index.html) - safeguard requirements for electronic protected health information
- [PCI DSS - PCI Security Standards Council](https://www.pcisecuritystandards.org/standards/pci-dss/) - data security standards for organizations handling payment card data
- [Systems Development Life Cycle - Wikipedia](https://en.wikipedia.org/wiki/Systems_development_life_cycle) - the classical SDLC, where the final phase is maintenance
