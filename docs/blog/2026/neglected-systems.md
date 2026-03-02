---
title: "Neglected Systems"
description: "The most dangerous systems aren't old or new. They're the ones no one is investing in."
author: "Chris Grobauskas"
date: "2026-02-28"
draft: true
tags:
  - Risk
  - Modernization
  - Technical History
---

# Neglected Systems

The most dangerous systems aren't old or new. The most dangerous systems are neglected systems.

It's tempting to view Mainframe, distributed, and cloud systems as a linear progression from old to new. In reality, every platform is a bundle of trade-offs with an end-of-life date. You can choose one platform or follow a hybrid strategy, but you cannot stop investing in the platforms you rely on.

<!-- more -->

When you under-invest (or worse, disinvest), platforms become rigid, outdated, and harder to evolve. I call this **the neglect trap**: you stop investing, the platform decays, your migration takes longer than planned, you have problems beyond the timeline, and your old system becomes riskier to operate. It may even be self-reinforcing ... when you have to pour resources into large tactical fixes on the legacy system while waiting for the future strategic system to arrive, those fixes pull investment away from the very replacement that was supposed to end the cycle.

## The Case for Disinvestment

The strongest argument for disinvestment is that sunk-cost reasoning traps organizations into pouring resources into platforms they should abandon. Controlled disinvestment signals strategic clarity. Budgets are finite. Redirecting resources toward a modern replacement is exactly what portfolio management looks like, and refusing to let go of the old system can starve the new one.

That argument holds ... but only under two conditions: you've honestly accounted for how long the transition will take, and you've funded the old platform through the gap. When a migration stretches into a decade, and the platform you stopped investing in decays in place, disinvestment becomes the neglect trap.

## A Pioneer Platform, Then Abandoned

I've seen this firsthand. In the 2000s, Hewlett-Packard decided to sunset the HP 3000 hardware platform and MPE/iX operating system. One of our core business systems ran on that platform, using HP Allbase and IMAGE databases with HP COBOL applications. HP's decision forced a full replacement program.

The HP 3000 and its cousin the HP 9000 were serious platforms. Introduced in 1972, the HP 3000 outlasted both the DEC VAX and PDP-11, running for over 30 years. HP positioned it as one of the earliest "business servers." The HP 9000 rivaled Mainframe performance at a fraction of the cost. Our largest systems were N-Class 8-way servers, each hosting thousands of concurrent connections.

HP's final investments in the HP 3000 brought POSIX (a set of Unix interoperability standards) compatibility to MPE/iX and JDBC (Java database connectivity) support to HP Allbase, opening the door to Apache and other open-source tools. But by then, it was too little, too late.

These were the "HP Mainframes" at the heart of this production platform. We had hundreds of them.

## Our Distributed Processing Systems

We built distributed computing primitives on this platform years before the industry named the patterns.

Our HP 3000 systems were among the first using TCP/IP for core business workloads. We utilized a Remote Procedure Call (RPC) framework that enabled distributed computing across a fleet that spanned hundreds of servers. A consolidation effort later reduced server counts while still supporting thousands of active employee sessions across the enterprise.

The system spanned the fleet, not a single server. RPC calls let employees search and access records across the fleet, spreading workloads across smaller, less expensive hardware rather than concentrating them on a few large systems.

The system also ran a multi-threaded transaction manager that processed background work using step-functions: multi-step workflows with built-in retry mechanisms, where each step could fail and resume independently. Running across hundreds of servers, this was a robust distributed transaction processing system and a very early example of what we now call the outbox pattern (writing an event record alongside the business transaction, then processing it asynchronously). The system implemented this _decades before microservices gave the pattern a name_.

## When Investment Stops

When HP announced the end of the HP 3000, we made a reasonable choice: stop investing in the old platform and redirect resources toward building its replacement. But unrealistic timelines meant the program took far longer than expected. We joked it was always "two years in the future." A colleague even had a running nursery rhyme: _2008 would be great, 2009 would be fine, 2010 here we go again, 2011 would be heaven._ The work spanned more than a decade.

Mid-effort, we completed a port project just to stay on supported hardware, moving the system from HP 3000/MPE/iX to HP 9000/HP-UX. That port kept us running but did not remove the risk of outliving the platform. Eventually, we hit the final date we could purchase new hardware. We had to estimate capacity needs years in advance, stockpile enough hardware to outlive the platform, or turn to the secondary market, where support was restricted. We also paid exorbitant end-of-life support extensions to remain under extended software support.

Even during this period, we added significant functionality: integrating with a precursor to the replacement system, adding several centralized operations to make business workflows more efficient. These were good business decisions, but they stressed the architecture.

Workloads followed data placement. Each record lived on a single server based on the office handling it. Interactive logins and RPC calls from remote systems concentrated load on the servers with the most records and the largest workforces. Because we could not easily buy new hardware or upgrade past a certain point, we faced a real risk of running out of capacity with limited ways to scale.

The consequences were concrete. A single office cluster's work architecturally could not span multiple servers. If a server ran out of capacity, the only option was a complex data migration to split workloads across systems.

Centralized operations funneled logins and remote access onto a small number of servers. The risk was not for every server, but it was a looming threat for all of our high-volume systems.

Our systems workloads had seasonal variation. The staff who had worked on the system understood exactly how fragile the platform had become in higher volume processing periods, but explaining that was difficult. The danger was invisible to most of our organization.

## The People Are the Platform

Systems that were once well-regarded became liabilities as the architecture aged and investment stopped. And the impact went beyond hardware. HP laid off engineers who had built and maintained the platform for decades. Some of those people were our partners. They had helped us troubleshoot production issues, optimize system configurations, and plan capacity. When they left, their knowledge left with them.

The same pattern played out internally. As the replacement program dragged on, many people who understood the old system's architecture were reassigned to finish the migration. This was the correct decision, but it left a smaller number of internal staff alongside outsourced support to operate a system that was live in production.

The extended support helped, but by the end, a lean core team was responsible for keeping the lights on. The neglect trap didn't just affect the platform. It trapped the people who remained. Those maintaining the legacy system had to keep it running while consulting on the new one. People were stretched thin just to maintain support.

> People are just as critical to your technology portfolio as the platforms themselves.

We had no choice. HP made the decision for us, and everything that followed ... the reassignments, the outsourcing, the skeleton crew ... was what it took to get off a burning platform. Even as one of the largest HP 3000 customers, we could not reverse their decisions. We could only manage the consequences.

I still think about this 15 years later. Not as a cautionary tale about old systems, but as a reminder of what happens when your platform's future is in someone else's hands.

## Are You in the Neglect Trap?

Before you assume your disinvestment is rational, run through these questions. If you don't like your answers, you're neglecting a core asset.

- **How long will the transition really take?** Not the plan ... the realistic timeline. How long have similar efforts taken in your organization?
- **What happens to the old platform in the gap?** Can you still patch, scale, and staff it? Is your support model realistic when you need to move people to finish your migration?
- **Do you still control the hardware and software lifecycle?** Or has a vendor already made that decision for you?
- **Are you retaining the people who understand the system?** Do you know who holds critical operational knowledge, and what happens when they leave? Do you have a succession plan for these key people?
- **Is anyone tracking the operational risk?** Not the project risk of the replacement ... the operational risk of the system you are sunsetting.

## Links

- [HP 3000 - Wikipedia](https://en.wikipedia.org/wiki/HP_3000) - history, hardware generations, and the 1972 recall
- [Enterprising: HP 3000 Business Servers - HP Archives](https://www.hewlettpackardhistory.com/item/an-enterprising-endeavor/) - the "business server" origins
- [HP 9000 and PA-RISC Story - OpenPA](https://www.openpa.net/systems/hp-9000_pa-risc_story.html) - four decades of PA-RISC evolution
- [HP N4000 rp7405/rp7410 - OpenPA](https://www.openpa.net/systems/hp_n4000-rp7405_rp7410.html) - Superdome cell architecture in mid-range servers
- [HP Unveils Mainframe-Class Unix Machines - TechMonitor (1993)](https://www.techmonitor.ai/technology/hewlett_packard_unveils_mainframe_class_unix_mpeix_machines/) - the T500 announcement
