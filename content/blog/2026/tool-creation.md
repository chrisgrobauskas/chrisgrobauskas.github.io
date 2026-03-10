---
title: "What are you solving?"
description: "Code generation can be a powerful tool or a code smell. Sometimes, it's both."
author: "Chris Grobauskas"
date: "2026-02-28"
updated: "2026-03-07"
tags:
  - Coding
  - Automation
  - Tooling
---

The recent explosion of GenAI got me thinking about the older code generation tools I've worked with. The appeal is the same as it's always been: get more done, reduce the toil. That's all goodness, but it can be used to "solve" the wrong problems too. Problems you could remove and not need to fix.

We have had code generation for decades; it's a side effect of being able to generate output programmatically. Sometimes it's useful, but sometimes it just masks problems.

<!-- more -->

## Good: Configuration as Code

Mainframe batch jobs are defined in JCL (Job Control Language). In some ways, it was an early enterprise scripting language. My employer had a template engine that rendered source files into environment-specific JCL at deploy time. 

One template could target different systems, run a single step against more than one database, or expand into a full set of related jobs. It reduced the number of assets teams needed to maintain by moving what varied into configuration, reducing the duplication we would have seen if we were manually coding a version for each system.

At its core, it was a [templating engine](https://en.wikipedia.org/wiki/Template_processor) and an early, effective form of application configuration.

What made it good, though, was twofold: it solved a real problem, and the abstraction was thin. You could read the template JCL and immediately understand what the output would look like. The mapping between input and output was relatively visible if used well.

## Complicated: Miniature Languages

I have also worked with a more complicated version of code generation. One earlier, homegrown tool I worked with generated scripts and JCLs. The tool was implemented as a domain-specific language, and it did solve problems. 

Structurally, it was a custom language interpreter written in REXX and built to run as an editor macro. REXX is a scripting language common on Mainframes, and text editor macros let you automate tasks within ISPF Edit (the Mainframe's primary text editor).

It was, however, very complicated to use. The implementation was an entire miniature language packed into one file, with difficult-to-read syntax.

It wasn't "bad" in the sense of being useless. It solved real problems. But it was also hard to read, hard to learn, and hard to reason about. There was no tooling support for code highlighting, linting, validation, or debugging. It was slow, because edit macros are slow when you point them at large files. And, it was written for and understood by only one team. Even within the team, it was only fully understood by its author.

While it was originally designed to generate data sets for testing, you _could_ generate anything with it:

- It was used to generate _JCL templates_.
- It was used to generate _its own input_ for some workflows that were used to generate _JCL templates_.
- It was used to generate input for itself that varied by target system to generate _JCL templates_ that generated different output on different systems.

Code generating other code that generates more code is where reasoning starts to get tricky. It isn't that it can't work; it's that it becomes hard to be confident the output is correct.

> At some point, it became archaeology instead of debugging.

The tool generated difficult-to-read code that would in turn generate more code, which is confusing enough on its own. The real issue, however, was that it was solving a symptom rather than the root problem.

## The Organizational Constraint

Here's the thing I tried to remember when I felt myself getting a headache from working with it: the generator existed mostly because of an organizational constraint, not a technical one.

When the tool was created, some test environments did not look like production. Multiple environments were nested like Russian dolls and compressed into a single logical system, whereas in production they would have been 10, 20, or 30 different systems.

This was done to save money, but it introduced a problem. Names for data sets, database schemas, and other resources that were uniquely named in production were colliding in test.

> Something had to manage that complexity. Several tools were created to solve this by different people. The one my team used had the most features, but it was also the hardest to use.

I prefer test environments to look as much like production as possible, but the cost constraint was a serious one at the time. The business "saved money" on infrastructure, but paid for it in lost productivity as people had to work around the environment not looking like production.

## The Constraint Test

Before you build a new internal tool, ask what problem you are actually solving. What constraint are you working around?

- **Is this a technical problem or an organizational constraint?** Are you automating away genuine technical complexity, or creating a workaround for how the environment or organization is structured?
- **Does this simplify, or just move the pain around?** A good tool reduces work in a way you can explain in one sentence. A bad one adds a new, obscure layer that everyone has to learn.

> If your tool exists because the environment is complicated, fix the environment if you can. Don't build more tools to hide the ugliness.
> 
> If you cannot remove the constraint, don't make multiple tools to solve the same problem.

Both the JCL template engine and the REXX code generator attempted to solve the same problem: environment-specific configuration. The JCL template engine was the first, and it was the easier one to use. A fair question is why someone would build a second tool instead of extending the first. The honest answer is that the teams who needed the solution were not the teams who owned the existing tool, and their priorities did not overlap enough to align on one approach. That is a common pattern in large organizations.

It would have made more sense to enhance the tool everyone already understood to manage the complexity across multiple environments.

> GenAI makes creating tools easier, which makes this pattern worse. If everyone creates tools to solve common problems, you get the opposite of the [tragedy of the commons](https://en.wikipedia.org/wiki/Tragedy_of_the_commons): instead of depleting a shared resource, you end up with a fragmented mess of competing, siloed solutions.

Code generation is a lever. Point it at the right problem and it multiplies your effort. Point it at the wrong one and it multiplies your confusion.

## Links

- [Template processor - Wikipedia](https://en.wikipedia.org/wiki/Template_processor) - the pattern behind configuration-as-code tools
- [Tragedy of the commons - Wikipedia](https://en.wikipedia.org/wiki/Tragedy_of_the_commons) - the classic shared-resource problem, inverted when everyone builds their own tool
