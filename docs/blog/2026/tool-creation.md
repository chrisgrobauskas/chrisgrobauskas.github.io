---
title: "What are you solving?"
description: "Code generation can be a powerful tool or a code smell. Sometimes, it's both."
author: "Chris Grobauskas"
date: "2026-02-28"
tags:
  - Coding
  - Automation
  - Platform
  - Tooling
---

# What are you solving?

GenAI is what got me thinking about code generation and older versions of it that I have worked with. The appeal is the same as it's always been: get more done, reduce the toil. That's all goodness, but it can be used to "solve" the wrong problems too. Problems you could remove and not need to fix.

I've worked with code generation for decades, solving real problems and making platforms easier to use.

<!-- more -->

## Good: Configuration as Code

Mainframe batch jobs are defined in JCL (Job Control Language), an early enterprise scripting language. My employer had a template engine that rendered source files into environment-specific JCL at deploy time. One template can target different systems, run a single step against more than one database, or expand into a full set of related jobs. It reduces the number of assets teams need to maintain by moving what varies into configuration. It reduces mistakes manually coding a version for each system.

This isn't really a Mainframe technology. At its core, it's a [templating engine](https://en.wikipedia.org/wiki/Template_processor) and an early, effective form of application configuration.

What makes it good is that the abstraction is thin. You can read the template JCL and immediately understand what the output will look like. The mapping between input and output is relatively visible if used well.

A more modern example is a pattern I've seen in enterprise environments: developers model business flows in a structured GUI, and those models are compiled into application code by an internal framework. The model _is_ the implementation: a living document that generates working code.

## Complicated: Miniature Languages

I also worked with earlier, homegrown tools that generated scripts and JCLs. The tool was a custom language interpreter written in REXX and built to run as an editor macro. REXX is a scripting language common on Mainframes, and text editor macros let you automate tasks within ISPF Edit.

> One homegrown tool contained an entire miniature language packed into one file, with difficult-to-read syntax.

It wasn't "bad" in the sense of being useless. It solved real problems. But it was also hard to read, hard to learn, and hard to make safe. We didn't have editor support (highlighting, linting, validation, debugging) that would have made a custom language less risky. And it was slow, because edit macros are slow when you point them at large files.

It got worse when it was used to generate _JCL templates_. Code generating other code that generates more code is where reasoning starts to get tricky. It isn't that it can't work; it's that it becomes hard to be confident the output is correct. Changing it was even worse, because it also generated configuration files for itself.

> Code generation to create configs, to create code, to write templates for JCL, that would generate different code on different systems. At some point, it became archaeology instead of debugging.

## The Organizational Constraint

Here's the thing I tried to remember when I felt myself getting a headache from working with it: the generator existed mostly because of a cost constraint, not a technical one.

Some test environments did not look like production when it was created. To save money, systems were consolidated or shared, and production names could not be reused. If the environment had matched production, the tool would never have been needed. And it wouldn't have grown into something that required archaeology to debug.

I prefer that test environments look as much like production as possible, but in this case the cost constraint was a serious one at the time.

## The Constraint Test

Before you build new tools, ask what problem you are solving. What constraint are you solving?

- **Is this a technical problem or an organizational constraint?** Are you automating away genuine technical complexity, or creating a workaround for how the environment or organization is structured?
- **Does this simplify, or just move the pain around?** A good tool reduces work in a way you can explain in one sentence. A bad one adds a new, obscure layer that everyone has to learn.

> If your tool exists because the environment is complicated, fix the environment if you can. Don't build more tools to hide the ugliness.

The JCL templating engine passes the constraint test. It solves a real technical problem (environment-specific configuration). The REXX generator fails it. It encoded an organizational workaround ... test environments that don't match production ... into a tool that became its own source of complexity.

Code generation is a lever. Point it at the right problem and it multiplies your effort. Point it at the wrong one and it multiplies your confusion.
