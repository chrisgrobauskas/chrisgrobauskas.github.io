---
title: "Microservices and Microliths"
description: "Microservices and microliths solve different problems and represent different bets about your organization. Knowing when each fits matters more than picking a side."
author: "Chris Grobauskas"
date: "2026-02-28"
draft: true
tags:
  - Architecture
  - Design
  - Modernization
---

# Microservices and Microliths

Every service boundary you draw represents a bet about your organization's future. Draw it along today's team structure, and you've embedded Conway's Law into your architecture. If the org changes (and it will), those boundaries become expensive to move.

<!-- more -->

Decomposition into services can lock in boundaries based on how teams are organized today. When the organization realigns, your service boundaries don't follow.

You're left with services that no longer match team ownership, with data in tables now effectively owned by two teams. The coordination costs grow with every reorg. This is why Martin Fowler's [Monolith First](https://martinfowler.com/bliki/MonolithFirst.html) argues most successful microservices systems started as a monolith that was later decomposed, because you rarely know the right boundaries until you've lived with the domain. Even then, our systems span decades while our org structures will not.

Microservices and microliths both have real strengths. The question isn't which is better. The question is which tradeoffs match your system, your organization, and the transition you can actually fund.

## The Distributed Monolith Trap

Splitting an application into services without splitting the data creates a [distributed monolith](https://dev.to/saeedhbi/three-signs-your-microservices-are-actually-a-distributed-monolith-177j): you get all the complexity of a distributed system without the independence microservices are supposed to deliver.

Watch for these patterns:

- **Direct table access across services.** Once a consuming team joins directly to your tables, the owning team can't change their implementation without coordinating with every consumer.
- **Tables with split ownership.** A single table where 80% of the data belongs to one product team and 20% to another ... typically the result of an organizational realignment that didn't come with an application redesign. The split was right when it was built and wrong after the reorg. Fixing it requires an expensive migration.
- **Triggers on shared tables.** Triggers that enforce cross-service business logic create hidden coupling and lead to bottlenecks under load.
- **Legacy stored procedures spanning services.** Procedures written when the application was one system, now straddling service boundaries (and ownership) no one planned for.

These patterns persist because unwinding them is expensive and rarely prioritized. I've seen this play out with a shared data service originally designed with direct table access for consumers. Ownership of that data shifted during a reorg, but the consumers didn't change. Years later, the team responsible for it was still working to move consumers to an API-based model, because each consuming team had different priorities and timelines. Once you couple at the data layer, you introduce organizational coordination costs that outlast the original technical decision.

## Data Sovereignty First

The principle is straightforward: each service owns its data, and other services access it only through the service's API. No direct table access across service boundaries. This applies across microservices _and_ microliths.

There are practical exceptions. Lookup tables with stable, read-only reference data (allowed values, etc.) can be directly accessed by multiple teams because ownership is unambiguous and the data design does not change even if the data itself does. Even those lookups may benefit from a caching service in a microservices architecture, but the risk of direct access is low when the data is truly read-only and the schema doesn't change.

The real cost of violating data sovereignty is organizational, not just technical. After you allow direct access, every schema change requires cross-team coordination. The owning team loses the ability to evolve independently. In an environment working toward unified platforms and reduced fragmentation, clear data ownership isn't just good architecture. It reduces the cost of future changes by limiting coordination to the old and new owning teams, rather than dragging in every consumer who joined directly.

## The Case for Microservices

The strongest argument for microservices is organizational agility. Independent teams deploying independent services on independent schedules, with clear ownership of both the code and the data. When service boundaries match team boundaries and domain boundaries, teams move faster because they coordinate less.

Microservices also align well with a platform strategy. When you're building shared capabilities (customer, inventory, billing, fulfillment) meant to serve multiple lines of business, well-bounded microservices let each capability evolve at its own pace. They enable reuse without tight coupling between the teams consuming and producing those capabilities.

Notice though, the domains above are broad ones. I'm calling these macro-domains: order processing vs. customer management vs. billing.

Versus micro-domains for fine-grained business capabilities within a larger domain. Subsets of the domains above. Services for smaller micro-domains owned by different teams are the boundaries where data ownership and transactional guarantees come into conflict.

> Micro-domain boundaries are much harder to get right than macro-domain boundaries over time.

Getting this right requires discipline:

- **Strict data ownership.** Each service manages its own data.
- **API-first communication.** Services interact through APIs, never through shared tables.
- **Team alignment.** Teams match service boundaries ([Conway's Law](https://martinfowler.com/bliki/ConwaysLaw.html)). When your team structure doesn't match your service boundaries, the architecture drifts back toward the monolith.

## When a Microlith Fits Better

Before committing to a microservices split, **especially a re-write**, ask whether you actually need independent deployment at every boundary. Microservices impose real operational overhead: distributed tracing, extensive error handling for failure modes, eventual consistency across service boundaries, and the complexity of [distributed transactions](2025/transactions).

> For some systems, a **microlith** (a system with internal modularity but shared deployment) is the better fit. A large mission-critical processing environment I worked in is a concrete example.

That system was deployed as a set of compiled artifacts that shared a codebase layout. What made it a microlith is how the shared modules were assembled. Micro-domains each lived in their own source structures. A framework layer managed passing value objects across calls between micro-domains, keeping the coupling explicit and controlled in most cases. The components were composed into larger deployables through a coordinated enterprise build process.

Because the micro-domains share the same deployable, they can share the same transaction boundary if necessary. The framework manages that boundary, which reduces database contention and enables reuse across micro-domains without breaking into separate services.

Teams develop independently against their own micro-domains, but the assembled deployable gives them transactional guarantees that independent microservices cannot provide without significant additional complexity.

## Two-Phase Commit: Reality Check

The industry narrative has moved away from two-phase commit (2PC), and for platforms and frameworks that don't support it well, the criticism is fair. The coordinator is a single point of failure, all participants must implement the protocol, and under failure conditions it holds locks across systems.

But inside platforms and frameworks that support 2PC natively, the downsides are overstated and the benefits to simpler processing are understated. The system I worked on used 2PC deliberately, and it was a key feature of the architecture.

2PC coordinates rollback across multiple databases and message queues, ensuring that on errors all changes roll back consistently. This is what enabled the system to scale through asynchronous processing without building extensive compensating transaction logic. It also reduced system resource usage compared to each application independently maintaining its own database and MQ connections.

The system it replaced did not use 2PC. It achieved strong consistency through application-based locking and an asynchronous transaction manager that used the outbox pattern with step functions. When the replacement was designed, eventual consistency was a hot topic. We debated it extensively. The debate resurfaced when we started adopting microservices through APIs. For the core processing platform, however, we rejected compensating transactions across micro-domains.

That didn't mean the system avoided eventual consistency entirely. It used extensive asynchronous processing, which is a form of eventual consistency. Ledger processing for accounting data used reversals and corrections, another form. The distinction is that the system rejected eventual consistency _across micro-domains for transactional processing_. When an action required an audit trail, the audit record committed in the same transaction as the change. When an action initiated asynchronous work, the request wrote to a message queue in the same transaction.

> When updates need to be coordinated in a _business workflow_ across several micro-domains. They are managed in the same transaction.

Implementing the same guarantees with compensating transactions would require significantly more error handling and would have real consequences for business workflows. Compensation is not always a simple matter of reversing an action if data has been sent to other systems. Or, it may mean waiting to send that data to other systems by using pended transactions, etc. These are not problems technically, they just happen to have business consequences in some cases.

Because this system ran on a vertically-integrated enterprise platform (Mainframe relational databases, queuing, and application servers from the same vendor) that enables 2PC at scale, tradeoffs look different inside a controlled boundary than they do across independently deployed services. Dismissing 2PC because it doesn't work well in loosely coupled microservices ignores the systems where it works exactly as intended.

## The Coexistence Problem

In practice, most larger enterprises that have older systems run both patterns. A microlith may handle core processing for a macro-domain while microservices coexist enabling newer capabilities, but the coexistence creates friction worth naming.

**Transactional guarantee mismatch.** Inside the microlith, 2PC ensures consistency. Outside, services rely on application-level enforcement or eventual consistency. The boundary between these two models requires careful design. Teams that don't understand the difference introduce bugs that look like database issues but are actually architectural mismatches. Data teams field these questions regularly, even though the root cause isn't the database.

**Cyclical dependencies.** When a microlith calls an external API that calls back into the microlith (directly or indirectly through another API), both paths compete for the same application and database locks. The direct case creates visible contention. The indirect case is worse because the cycle isn't visible in any single call chain. You're competing with yourself for database resources, and the symptom is _locking yourself out_ of your own micro-domain's data.

**Ownership drift.** Organizational realignments reassign teams without redesigning the systems those teams own. A table that belonged to one team now serves two. A service built for one micro-domain now straddles two. These aren't failures of architecture. They're the natural consequence of organizations changing faster than applications can follow.

> Microservices and microliths represent different bets. Microservices bet that your org boundaries are right and stable. Microliths bet that transactional consistency across domains matters more than independent deployment. Know which bet you're making.

## Choosing Your Architecture

These questions help you decide which tradeoffs to accept:

- **Do you know your domain boundaries well enough to split?** If you're still discovering them, decomposing now locks in a bet for transactional boundaries. A microlith lets you refactor boundaries without re-architecting integrations and reduces (but does not eliminate) the need to rework micro-domain boundaries with organization changes.
- **What does your transaction model require?** If updates across micro-domains must fully succeed or fully roll back, and compensation is not acceptable, 2PC inside a microlith gives you that with simpler code. If eventual consistency is acceptable, microservices with sagas may be the better fit.
- **Can your teams deploy independently?** If team and service boundaries align, microservices deliver real velocity. If they don't, independent deployment creates coordination overhead that offsets the benefit.
- **Are you mixing both patterns?** If so, design the boundary between 2PC and eventual consistency explicitly. Identify cyclical call paths before they cause production outages.

More Importantly:

- **What's the cost of re-architecture vs. coexistence?** For existing systems that work and serve the business, the question isn't whether the pattern is ideal. It's whether the cost of rewriting to a different model (millions of dollars and years of effort) is justified by the benefit, or whether disciplined coexistence is the more responsible path.

## Links

- [Distributed Monolith Signs - Saeed HBI](https://dev.to/saeedhbi/three-signs-your-microservices-are-actually-a-distributed-monolith-177j) - how to identify a distributed monolith
- [MonolithFirst - Martin Fowler](https://martinfowler.com/bliki/MonolithFirst.html) - why most successful microservices started as monoliths
- [Conway's Law - Martin Fowler](https://martinfowler.com/bliki/ConwaysLaw.html) - how org structure shapes architecture
- [Distributed Transactions](2025/transactions) - tradeoffs between 2PC, sagas, and compensating transactions
