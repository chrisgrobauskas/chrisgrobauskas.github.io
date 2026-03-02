---
title: The Seduction of a Collapsed Lifecycle
description: "The collapsed SDLC works for code. It breaks at the state boundary, where accountability can't be automated."
author: "Chris Grobauskas"
date: "2026-03-01"
draft: true
tags:
  - GenAI
  - Data Corruption
  - Automation
---

# The Seduction of a Collapsed Lifecycle

Boris Tane argues in [The Software Development Lifecycle is Dead](https://boristane.com/blog/the-software-development-lifecycle-is-dead/) that AI agents have collapsed the traditional staged software development lifecycle (SDLC) into a single intent-build-observe loop, and that the classic lifecycle is dead.

As Whitman wrote, I contain multitudes ... and we all want to agree, except the grumpy database administrator (DBA).

<!-- more -->

The systems analyst in me, who never enjoyed documenting requirements, wants to agree. So does the developer with a love-hate relationship with programming, the QA person who appreciates tools that simplify testing, and the operations person who would like to identify and fix issues more quickly.

The tinkerer who spent the weekend experimenting with Opencode and GitHub Copilot to see how little I can be involved and still produce good code wants to believe. I genuinely believe large language models (LLMs) have tremendous potential and practical use now.

Most systems that matter store state. And the DBA in me is not so easily convinced that stateful systems are ready for what is described.

The core argument here is seductive: "AI agents didn't make the SDLC faster. They killed it."

The new lifecycle is described as "Intent. Build. Observe. Repeat." and I won't argue with that. I also agree with observability as "the last line of defense."

The vision of agents that are "monitoring the rollout, adjusting traffic percentages based on error rates, automatically rolling back if latency spikes" is genuinely compelling.

But the grumpy DBA keeps asking questions that don't have good answers yet.

## Where It Already Works

For getting code into an integration testing environment where we can validate it, I'm all for it. For stateless services and low-risk deployments that are quick to roll back to a known state, the "intent, build, observe, repeat" cycle works today.

But someone, not something, has to be accountable for what ships to production. A human in the loop reviewing code and approving deployments isn't just prudent ... in regulated industries like insurance and finance, it's a compliance expectation.

And most systems exist to maintain state in a database or another data store. That state is not as easily rolled back, and the failure modes are far more complicated. The rest of this post is about that boundary.

## Modern Assumptions and Legacy Reality

The argument assumes systems modern enough to support what it describes. We're also talking about legacy environments that have only partially embraced test-driven development (TDD) and tight, small release cycles.

A greenfield solution built on these principles will not help you manage existing systems, especially [neglected systems](2026/neglected-systems) that still need to run while you build their replacement.

Many of those legacy environments aren't running the "feature flags, canary releases, progressive rollouts, automatic rollback triggers" described here either. Those are engineering investments in their own right.

More critically, sophisticated deployment strategies only limit the blast radius of a bad code release; they don't eliminate the window in which data can be corrupted.

## Code Rollbacks Don't Fix State

This is the [reversibility test](2025/risk) the piece doesn't fully reckon with: code can be rolled back. Corrupted data frequently cannot.

> Code rollback is a technical operation. Data recovery is an investigation.

The article frames the auto-rollback as a safety net, "if something fails, the agent fixes it," but that framing applies cleanly to code. It applies very differently to state.

## When Systems Carry Human Consequences

System issues carry consequences that extend well beyond outages or inconvenience. I work for a company whose mission is to support people during one of the most difficult days of their lives.

An insurance claim system failure isn't an outage. It determines whether someone can get to work after their car is totaled, or find temporary housing after their home is severely damaged.

For systems like ours, a poorly executed automated deployment wouldn't merely cause inconvenience. It risks real harm to real people and justified reputational damage if we fail to deliver on our promises.

If you approve a _completely_ collapsed lifecycle for systems that write customer data, you are accepting the risk that automated recovery will fail and no one on your team may have the knowledge to fix it manually. That's a business decision, not a technical one.

## Monitoring vs. Maintenance

The article concludes that "monitoring is the only stage of the SDLC that survives." I'd push back on the framing: in the [classical SDLC](https://en.wikipedia.org/wiki/Systems_development_life_cycle), the final phase isn't monitoring, it's maintenance.

Monitoring is passive. It tells you something went wrong. Maintenance is active and includes far more than catching and squashing application bugs or performance regressions.

It includes understanding why the system is in the state it's in, tracing the sequence of events that led there, determining what data was affected, and deciding how to restore data integrity safely.

## Why Auto-Recovery Fails

### Data Corruption Is Not a Revert

The article asks us to imagine agents that detect regressions and fix them: "the agent investigates and fixes." But someone still has to decide which corrupted data needs remediation and how to do it safely.

Corrupted data doesn't stay in one place. It propagates across systems, gets saved, gets transmitted, gets consumed downstream. You can't fix it with a system rollback or database restore because that also undoes the good updates that happened in the same window. The failure modes get more complex when transactions span services ... I wrote about that in [Distributed Transactions](2025/transactions).

Data recovery requires surgical precision, applied to systems you need to understand deeply and intimately.

There are options to help with this: event sourcing, immutable audit logs, point-in-time recovery, and automated anomaly detection. These can reduce recovery effort, but narrowing the gap is not closing it. The tools help you find the damage faster. Someone still has to decide what to do about it.

### Tacit Knowledge and Institutional Memory

The knowledge needed to recover from data corruption isn't written down for LLMs to train on. Companies have every incentive to bury detailed postmortems on data corruption or breaches. Outside of privacy breach notices stating "something bad happened," the specifics of how production data was corrupted and how it was repaired are institutional memory that never gets published. It lives in people's heads, and it stays there.

### GenAI as Decision Makers

The data needed to determine what to fix is also situational. If I could predict failure modes that would cause data corruption, I wouldn't make the mistake in the first place.

It's tempting to reach for GenAI to fill the gap. That temptation is understandable, and I hope to see cases where we can have automated reasoning to assist data engineers and DBAs during a recovery.

But GenAI tools shouldn't be the decision makers. Their confidence can exceed their accuracy, they lack deep context about a specific system's history and invariants, and when they get it wrong, no one is accountable for what breaks next.

If you look at how GenAI tools approach coding, the pattern is telling. It's broken till it's fixed, with multiple attempts and corrections along the way. The LLM itself will say things like, "You're absolutely right! The file is corrupted, let me revert the changes."

For data recovery, that sounds risky. Messy. Reckless.

If iterative automated data recovery goes wrong, you aren't just dealing with the original corruption. You are layering new inconsistencies on top of it, making eventual human intervention exponentially harder. And that intervention will require exactly the kind of deep, system-specific knowledge that atrophies fastest when humans stop being in the reasoning loop.

## Before You Collapse the Lifecycle

Before adopting an agent-driven deploy loop for systems that store state, ask these questions:

- **Does your system write state?** Stateless services and read-only systems are better candidates. Systems that write customer, financial, or claims data are not.
- **Can that state be surgically recovered?** If a bad deployment corrupts data, do you have the tooling and expertise to identify exactly what changed, roll back only the bad writes, and verify integrity without a full restore?
- **Who is accountable?** When the agent gets it wrong, someone still has to explain what happened and fix it. If that person doesn't exist or no longer holds the context, you have a gap no amount of automation closes.
- **Does your team hold the institutional knowledge?** If the answer is "it's in the runbooks," test that claim. Runbooks describe expected failure modes. Data corruption is rarely one of them.

## Context Requires Stewardship

The article is right that "the quality of what you build with agents is directly proportional to the quality of context you give them." But context engineering assumes someone still holds the context.

In [The GenAI Arc](2025/genai-arc), I argued that what makes agentic AI's blast radius larger than earlier automation is that it reaches data, not just code. The same distinction applies here: code generation failures are recoverable. Data failures often aren't.

That's the deeper problem: if we automate the reasoning, our mental models of these complex systems will atrophy. When a catastrophic data issue eventually arrives, the human nominally in the loop will no longer have the knowledge to fix it.

You can automate development.
You can accelerate delivery.
You can compress the lifecycle.

> You cannot automate accountability.

## Links

- [The Software Development Lifecycle is Dead - Boris Tane](https://boristane.com/blog/the-software-development-lifecycle-is-dead/) - the original piece this post responds to
- [Distributed Transactions](2025/transactions) - transaction strategies and failure behavior across distributed systems
- [The GenAI Arc](2025/genai-arc) - why agentic AI's blast radius is larger when it reaches data, not just code
- [Human in the Loop](2023/human-in-the-loop) - why accountability requires a human reviewing and approving what ships
- [Willing to Fail](2025/risk) - the reversibility test: know whether a change is reversible before you make it
- [Bridging the Knowledge Chasm](2025/bridging-knowledge-chasm) - what happens when institutional knowledge walks out the door
- [Neglected Systems](2026/neglected-systems) - what happens when you stop investing in the platforms you depend on
- [Sarbanes-Oxley Act Section 404 - Wikipedia](https://en.wikipedia.org/wiki/Sarbanes%E2%80%93Oxley_Act#Section_404:_Assessment_of_internal_control) - internal control requirements over financial reporting systems, including IT change management
- [Systems Development Life Cycle - Wikipedia](https://en.wikipedia.org/wiki/Systems_development_life_cycle) - the classical SDLC, where the final phase is maintenance
