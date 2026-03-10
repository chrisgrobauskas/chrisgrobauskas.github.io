---
title: "The Colossus Bet"
description: "When the stakes are high enough, funding two approaches beats betting on one. The Colossus Bet explains when parallel options earn their cost."
author: "Chris Grobauskas"
date: "2024-02-18"
updated: "2026-02-27"
tags:
  - Technical History
  - Optionality
---

"Should we modernize the legacy system or build a new one?" I've watched this question consume months of debate. The instinct is to pick one path, commit, and move. But eighty years ago, a wartime memo made the opposite call ... and it changed the course of history.

<!-- more -->

## Both Options

In 1944, British codebreakers at Bletchley Park faced a problem: they needed to crack the Lorenz cipher faster than existing methods allowed. A [GCHQ retrospective](https://www.gchq.gov.uk/news/colossus-80) describes how a memo proposed two competing approaches. One was incremental. The other, Colossus, was called a "much more ambitious scheme" ... the first digital computer. The recommendation was to pursue both.

That decision preserved optionality. Colossus succeeded, and its intelligence helped convince Hitler that the Allied invasion would land at Pas de Calais rather than Normandy. If the committee had forced a single bet and chosen the safer option, D-Day might have gone differently.

## When to Keep Two Options Alive

I call this the **Colossus Bet**: deliberately funding two approaches when the stakes are high enough that picking wrong is worse than the cost of running both.

I've seen it work in enterprise modernization. Early in my career I worked on a large-scale system rewrite that was racing against a hardware end-of-life. We didn't expect to finish the rewrite before the support contract for our current platform expired. So we doubled down: port the existing application to a new hardware platform and operating system, while continuing the strategic direction of a full rewrite.

The rewrite program ran for six years after the port project was complete in production. Moving to the new platform was hard work and expensive, but it kept us on supported hardware until we could finish the rewrite.

> Running parallel efforts does split focus and increase cost. For most decisions, that is wasteful. But when uncertainty is genuine and the cost of guessing wrong is severe, taking a both-and approach can be the wiser decision.

The alternative in our case was too costly. Without the port, we would have run out of hardware and support mid-rewrite at the mercy of the secondary market for used equipment to keep a critical production system running. That was unacceptable.

Three questions to decide whether the Colossus Bet applies:

- **Is the uncertainty real?** If you can resolve it with a spike or a proof of concept, do that instead.
- **What's the cost of being wrong?** If the losing path is cheap to abandon, just pick one.
- **Can you afford the overlap?** Parallel options only work if you can staff and fund both without starving either.