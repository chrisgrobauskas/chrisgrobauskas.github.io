---
title: "Patterns Worth Knowing"
description: "Good design solves problems people actually have. Circuit breakers, the fit-for-purpose test, and the outbox pattern earn their keep through impact."
author: "Chris Grobauskas"
date: "2025-03-15"
updated: "2026-02-27"
tags:
  - Design
  - Simplicity
  - Design Patterns
  - Technical History
---

Christopher Alexander wrote about livable cities before the Gang of Four applied his thinking to software. The message was the same: good design solves problems people actually have, not problems that look interesting on a whiteboard.

<!-- more -->

## The Pattern Instinct

Alexander's 1977 book, *[A Pattern Language](https://en.m.wikipedia.org/wiki/A_Pattern_Language)*, revealed how timeless design principles create spaces where people thrive. The same thinking has made software systems more maintainable, more adaptable, and easier to reason about. Even if you don't know the pattern names, you've almost certainly worked with them.

The first system I supported was a distributed COBOL application written about a decade before AWS existed. Technically a microlith (a system with internal modularity but shared deployment), it needed to handle distributed transactions without two-phase commit. To do this it had a homegrown transaction manager implementing what we now call the [outbox pattern](https://microservices.io/patterns/data/transactional-outbox.html). It handled retries with a circuit breaker. It even offered functionality resembling step functions.

It just worked. And that's the point. Good systems, like good cities, are livable.

## Fit for Purpose

I've been sipping hot tea lately. My gas stove is painfully slow at boiling water, so I looked into switching to an induction stove. It would be faster and more efficient, but my kitchen isn't wired for it. And buying an entirely new stove would be expensive and over-engineered for the problem of boiling water faster.

Instead, I spent $15 on an electric kettle. Problem solved.

Knowing exactly what you're solving usually reveals the simplest path. The kettle didn't require new wiring, new countertops, or a contractor. It required fifteen dollars and a power outlet. I call this the **fit-for-purpose test**: before you commit to a solution, ask whether you're solving the actual problem or a bigger one you invented along the way.

## Circuit Breakers

That same kettle illustrates another pattern. Forget it's on? No big deal ... it shuts itself off when it senses danger. That's a circuit breaker.

In software, the idea is the same: when a service starts failing, stop hammering it. Back off, let it recover, and route around the failure.

But context determines the strategy:

- **Should you retry?** For a kettle that could burn your house down, no. For a network request, maybe ... with exponential backoff so you're not making things worse.
- **What's the fallback?** The kettle fails, so you grab a pot and boil water on the stove. In software, that's calling a secondary service, serving cached data, skipping a non-critical step, or degrading gracefully to partial functionality.

> A circuit breaker is only part of the answer. You still need to know your failure modes well enough to choose between retry, fallback, and fail fast.

## Impact Over Elegance

William Sealy Gosset worked as a statistician at Guinness. Publishing under the pseudonym "Student," he developed the t-test to improve quality control while keeping sample sizes small. [The story](https://www.scientificamerican.com/article/how-the-guinness-brewery-invented-the-most-important-statistical-method-in/) is worth reading.

A perfect model, an elegant design, or an aesthetic bit of code means nothing if it doesn't solve a problem. Gosset's work is also a fun example of data-driven decision making and optimization.

Three questions before you commit to a pattern:

- **Are you solving the real problem?** The fit-for-purpose test. Don't buy a stove when a kettle will do.
- **Do you know your failure modes?** Circuit breakers only help if you've mapped what can go wrong and how you'll respond.
- **Does it deliver impact?** Elegance without results is decoration.

## Links

- [A Pattern Language](https://en.m.wikipedia.org/wiki/A_Pattern_Language) - Christopher Alexander's 1977 book that introduced pattern-based design thinking
- [Transactional Outbox Pattern](https://microservices.io/patterns/data/transactional-outbox.html) - how to reliably publish messages as part of a database transaction
- [Circuit Breaker Pattern](https://martinfowler.com/bliki/CircuitBreaker.html) - Martin Fowler's explanation of circuit breakers in distributed systems
- [How the Guinness Brewery Invented the t-test](https://www.scientificamerican.com/article/how-the-guinness-brewery-invented-the-most-important-statistical-method-in/) - the story of William Sealy Gosset and impact-driven statistics
- [Microservices Patterns](https://microservices.io/patterns/index.html) - catalog of patterns for distributed systems
