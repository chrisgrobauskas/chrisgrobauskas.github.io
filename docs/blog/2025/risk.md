---
title: "Willing to Fail"
description: "The real risk isn't moving too fast or too slow. It's making irreversible changes without knowing which ones they are."
author: "Chris Grobauskas"
date: "2025-03-22"
tags:
  - Risk
---
# Willing to Fail

Being willing to fail is different from being reckless. But in software, the line is often drawn in the wrong place.

The real risk in engineering isn't moving too fast or too slow; it's making irreversible changes without knowing which ones they are.

<!-- more -->

Some decisions are reversible: a feature flag can be turned off, a proof of concept can be thrown away, a pilot covering a smaller set of use cases can be stopped before it scales. A new operational reporting store can be built alongside the existing one, allowing gradual migration without committing to a hard cut-over.

Others aren't: a schema change deployed to production without a rollback path, a missed backup before a destructive operation, a security misconfiguration that's already been exploited.

The goal isn't courage or caution. It's classification. Know which kind of change you're making before you make it. I call this the **reversibility test**: before you commit, ask whether the change is reversible. If it is, move fast. If it isn't, slow down and build a fallback.

> Classify the change before you make it. Reversible changes can move fast. Irreversible changes earn caution.

Move too fast on an irreversible change, and you own the outage. Move too slow on a reversible one, and you own the missed opportunity. Both carry real cost: in time, in trust, and in the systems you're responsible for.

Smart risk-taking in software means building the habits that let you move fast on the things that are safe to get wrong, while slowing down appropriately on the things that aren't.

Test your failure scenarios. Use feature flags. Build on-ramps that preserve the exit. Not because they slow you down. They're what let you move faster over time.

## Links

- [Feature Toggles - Pete Hodgson, Martin Fowler](https://martinfowler.com/articles/feature-toggles.html) - a practical guide to using feature flags for safe deployments
- [Reversible and Irreversible Decisions - Farnam Street](https://fs.blog/reversible-irreversible-decisions/) - Jeff Bezos's Type 1 and Type 2 decision framework