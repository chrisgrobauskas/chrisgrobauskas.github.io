---
title: Design Patterns
date: 
  created: 2025-03-27
authors: 
  - grobauskas
categories:
  - Design
---

Design patterns didn’t start with software. Before the Gang of Four introduced them to software engineering, Christopher Alexander used patterns to explain how to make cities and buildings more livable.

His 1977 book, *A Pattern Language*, revealed how timeless design principles create spaces where people thrive.

<!-- more -->

The same thinking has made software systems more adaptable, maintainable, and human-friendly. Even if you don’t know their names, you’ve likely worked with these patterns.

The first system I supported was a distributed COBOL application written about a decade before AWS existed. Technically a microlith, it needed to handle distributed transactions without two-phase commit. To do this it had a homegrown transaction manager, implementing what we now call the outbox pattern. It handled retries with a circuit breaker. Not only that, but it even offered functionality that resembled step functions.

It just worked. And that’s the point. Good systems, like good cities, are livable.

The tools to make them that way already exist. Are you using them?

[Learn more about A Pattern Language](https://en.m.wikipedia.org/wiki/A_Pattern_Language)