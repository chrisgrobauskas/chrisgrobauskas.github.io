---
title: "The Neglect Trap"
description: "When you signal disinvestment, the organization stops caring before the system stops running."
author: "Chris Grobauskas"
date: "2026-03-09"
slug: "neglected-systems"
tags:
  - Risk
  - Modernization
  - Portfolio Management
  - Legacy Systems
  - Technical History
---

I joined a team in 2000 only to learn the platform I was training for was already obsolete.

That platform was the [HP 3000](https://en.wikipedia.org/wiki/HP_3000), and our organization ran a mission-critical business system across hundreds of mid-range servers. We were moving from green-screen terminals to a modern web application. The Internet era made this inevitable, but HP's decision to kill the platform forced our hand.

What followed took twelve years and taught me the true risk of platform migrations.

The **neglect trap** happens when leadership signals disinvestment, and the rest of the organization hears "stop caring."

<!-- more -->

## HP Killed Our Platform

When HP killed the HP 3000, a massive replacement program kicked off. The pressure to disinvest was immediate, and the arguments were sound. The [sunk-cost fallacy](https://en.wikipedia.org/wiki/Sunk_cost) traps organizations into pouring resources into platforms they should abandon. Budgets are finite. Every dollar keeping the old system alive is a dollar not building the new one.

I started on the team that supported data movement and quickly picked up new responsibilities as other team members moved to the new build. Eventually I ended up on the team that owned the architecture for the old system. We consulted on changes for the old system and the new one. We could explain what did and didn't work with the current system design.

As the years dragged on, we ended up owning almost everything on the legacy side while support staff moved on to the future.

The replacement program changed direction repeatedly. Anyone who has worked on a modernization effort knows the drill: build-versus-buy debates, technology going end-of-life mid-project, timelines slip-sliding into the future.

We completed an emergency port from HP 3000 to HP 9000 hardware just to stay on a supported platform, a pivot no one had planned for, and one I'll come back to. What was supposed to take a few years took over a decade. A colleague had a running nursery rhyme as the deadlines slipped: _2008 would be great, 2009 would be fine, 2010 here we go again, 2011 would be heaven._

> Nobody wants to be the person advocating for more spending on the thing being replaced.

If you're leading a migration, communicate that you intend to maintain support for the system you're replacing. You don't want disinvestment to become neglect. Avoiding it means you've honestly accounted for how long the transition will take, and you've funded the old platform through the gap. In my experience, the first condition is almost never met.

## The Trap We Avoided

The neglect trap didn't arrive as one bad decision. It arrived as a series of reasonable ones.

Teams elsewhere in the organization, teams that owned contracts and budgets but didn't own the mission-critical business functionality, saw the disinvestment signal and acted on it. 

Leaders who managed the test environments repeatedly sought to cut test resources even though we needed those systems to complete the migration. The performance environment also served as our Disaster Recovery site in those days. In the event we lost a major location, we would have had to recover there. And yet we still discussed removing hardware.

Leaders who owned software contracts wanted to reduce licensing costs for the old platform. Reasonable on the surface, but misguided because these were shared components that could not easily be replaced.

From their perspective, they were managing costs on a declining platform. But those cuts needed review by people who understood what the system actually required.

Our leadership fought for funding. That mattered. What kept us out of the trap was a series of expensive, targeted investments where the argument against them was always the same: spend those resources finishing the replacement instead.

- **The HP 9000 port.** When timelines got near the platform's end-of-life, we ported the application to HP 9000 hardware running HP-UX with an emulation layer. The argument against it was straightforward: if we redirected those same resources to the replacement, could we finish before the hardware died? The answer was no. The port took two years. The replacement program continued another eight years from the same point.
- **Hardware stockpiling.** We hit the final date to purchase new HP 9000 hardware and had to estimate capacity needs years in advance. The initial plan was built from partial information and came in nearly bare-bones. We were lucky the right person happened to be assigned to review the numbers ... that person's clear evidence for year-over-year capacity growth prevented a gap that would have been catastrophic. There was no guarantee that review would happen. Without it, we'd have been dependent on a secondary hardware market where support was restricted.
- **Building on the old system mid-migration.** Every new feature on the old system meant building the same capability twice ... doubling the cost. The argument was always the same: delay for the business, or delay the replacement timeline. But the timeline was too long for the business to wait, and earlier implementations required the old system to remain the system of record until all legacy data could migrate.

**That created a dual-support period.**

Even with those investments, the trap still pulled at us. We cut corners on new features because we'd be "off this system soon." Engineers moved to the new build, and the remaining team owned more of the application with less depth to cover it.

When we saw timelines slipping, leadership funded the targeted investments and pulled people back from the new build when the old system needed them. That wasn't luck. That was leaders who took the operational risk seriously and engineers with support experience who spoke up in time to adjust course.

But each of those saves depended on someone being in the right room at the right time. The margin between "we avoided the trap" and "we didn't" was thin.

## People Are the Platform

The hardest part is always people.

If you've signaled disinvestment in a platform, people will reasonably choose to move to the future. The interesting work is on the new build. The career growth is on the new build. For some, it's a signal to find a new employer.

I took training to move to the new build. Twice. Both times I was pulled back to legacy support because no one else could cover it when we lost key resources.

The old platform was an island. It was a distributed client-server system running on mid-range servers, but the screens were still terminal-based. It wasn't Mainframe. It wasn't the web. Nothing else in the company ran on the same technology, and we were moving _to_ those platforms, not _from_ them.

It was incredibly difficult to hire for it. Imagine trying to hire a programmer for a dead platform, and needing them to have five years of experience in your custom-built codebase.

> If you can't hire for it and you can't train for it, the people who already know it are the platform.

We outsourced large parts of the support, but our vendor obviously couldn't staff roles that required in-house experience. Most of the system was homegrown ... from the transaction manager to RPC libraries. This increased the surface area that required experienced support. Internal backfill was impractical for the same reason. Some people were stuck.

How you maintain support when your experienced people leave is a question that outsourcing alone doesn't answer. This is the [knowledge chasm](/blog/2025/bridging-knowledge-chasm/) playing out in real time, and by the time you notice the gap, it can be permanent.

## Recognizing the Trap

That experience shaped how I think about every migration since. If you're leading one, ask:

- **How long will this really take?** Not the plan, the honest answer. If you don't know, that's your answer.
- **What happens to the old platform in the gap?** Can you still staff and support it when you need to move people to finish the migration?
- **Are you retaining the people who understand the system?** Do you know what happens when they leave?
- **Who is advocating for the old system, and are they being heard or penalized?**

If you don't like your answers, you're closer to the neglect trap than you think.

> The old system needs explicit support until the last production workload moves off it. Not until the new system launches. Not until the first migration phase. Until it's actually done.

Neglect sneaks in as a series of reasonable choices. Each one makes sense because "we're two years from done." It stops making sense when you've been two years from done for the last six years.

"Declining" describes a strategic direction, not an invitation to stop caring.

## Links

- [Sunk cost - Wikipedia](https://en.wikipedia.org/wiki/Sunk_cost) - the reasoning trap that makes disinvestment feel rational
- [Legacy Teams](/blog/2025/legacy-teams/) - why the people who know the old system need a seat at the table
- [Bridging the Knowledge Chasm](/blog/2025/bridging-knowledge-chasm/) - what happens when institutional knowledge walks out the door
- [The Colossus Bet](/blog/2024/colossus/) - when the stakes are high enough, funding two approaches beats betting on one
- [Willing to Fail](/blog/2025/willing-to-fail/) - the reversibility test and why some risks can't be undone
- [HP 3000 - Wikipedia](https://en.wikipedia.org/wiki/HP_3000) - history of the platform and HP's end-of-life decision