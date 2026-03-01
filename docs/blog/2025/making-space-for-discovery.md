---
title: "Making Space for Discovery"
description: "Safe environments for experimentation and targeted research spikes uncover what lies beneath the surface."
author: "Chris Grobauskas"
date: "2025-04-18"
updated: "2026-02-27"
tags:
  - Leadership
  - Research
---
# Making Space for Discovery

As children, we built forts out of pillows and cardboard boxes ... no approvals, no fear of failure, just imagination and play. Now, as adults, we optimize for uptime and reliability. Production must be stable.

The challenge isn't choosing between creativity and stability. It's building the structures that support both.

<!-- more -->

## Safe Spaces for Experimentation

You can carve out space away from production: sandbox environments, hack days, prototypes. Or you can enable safe experiments within production: pilot rollouts, [feature flags](https://martinfowler.com/articles/feature-toggles.html), [A/B testing](https://en.wikipedia.org/wiki/A/B_testing). Ideally, you're doing both.

But these methods alone aren't enough. People need to feel safe using them. If the culture punishes failed experiments, no one will run them regardless of how many sandbox environments you provision.

> How do you make space for safe exploration on your team? More importantly, how do you help people feel safe doing it?

## Research Spikes

Once you've built the space, the next question is how to use it. Just as scientists choose experiments to validate theories, strong technical leaders use targeted research spikes to uncover what lies beneath the surface.

To make your research spikes count, aim beyond the obvious:

- **Explore intersections.** Look where infrastructure, user experience, and data flows converge. Systemic issues often emerge at the edges.
- **Validate assumptions.** Use early research to pressure-test architectural decisions that may no longer serve your evolving system.
- **Trace bottlenecks.** Minor slowdowns can signal deeper structural flaws. Don't stop at the symptom; follow the signal to the source.

Consider how this plays out in a real-world scenario like platform migration. While a spike on session limits might confirm server needs, it can also reveal scaling constraints, challenge outdated assumptions, and reshape service boundaries. 

On a platform migration I worked on with colleagues, a spike confirmed that we could push beyond a default limit for write transactions — but also that the new platform would not match the throughput of the legacy system it was replacing. That was expected, but confirming it early allowed design conversations to start sooner rather than later.

That's systems thinking: understanding how local choices ripple through your entire architecture and using that insight to build smarter.

## Tactical vs. Strategic

I think about spikes in two categories. **Tactical spikes** solve a specific problem: "Can this system handle our TPS?" **Strategic spikes** reveal broader issues: "Are our service boundaries in the right place?"

The best technical leaders don't just solve today's problem. They see the whole system and investigate how to improve it.

A few questions before you start a spike:

- **What assumption are you testing?** If you can't name it, the spike will wander. What is the definition of done?
- **What would change your mind?** Define the outcome that would alter your direction. Otherwise you're confirming, not discovering.
- **Who needs the result?** A spike that doesn't reach the decision-maker is wasted work. Plan the audience before you plan the experiment.

You don't have to be perfect. The goal of a spike is often "horseshoes and hand grenades" work: you can't reproduce production exactly, but you can determine whether the best case gives you a signal about whether you'll need to redesign anything.

## Links

- [Feature Toggles - Pete Hodgson, Martin Fowler](https://martinfowler.com/articles/feature-toggles.html) - a practical guide to feature flags for safe deployments
- [A/B Testing - Wikipedia](https://en.wikipedia.org/wiki/A/B_testing) - controlled experiments for comparing outcomes
- [Blue-Green Deployment - Martin Fowler](https://martinfowler.com/bliki/BlueGreenDeployment.html) - zero-downtime releases by running two production environments
