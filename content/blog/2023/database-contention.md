---
title: "Database Contention Is an Application Problem"
description: "Why deadlocks and timeouts usually trace back to application design: transactions, locks, frameworks, and triggers. (Database Collaboration, Part 2)"
author: "Chris Grobauskas"
date: "2023-12-02"
updated: "2026-03-07"
tags:
  - Database
  - Teams
---

Most database contention isn't a database problem. It's an application design problem that the database makes visible.

If you haven't already, start with the [Prepare, Investigate, Report](/blog/2023/prepare-investigate-report/) framework ... it covers how to debug and report database issues before you get to the harder stuff here.

> Database contention is vexing because its roots are often in the application code, not the database itself.

<!-- more -->

## What Causes Contention

The most common cause is application design that doesn't account for how the database manages concurrency. When you hold locks for too long, the database is doing what you asked. Deadlocks are almost always an application design issue, and timeouts normally are too.

### Units of Work

The relevant concept is a "unit of work" ... what most of us now just call a transaction. How a transaction begins depends on the database. Some require an explicit `BEGIN`, others (like Db2) start one implicitly at the first SQL statement. Either way, it ends at the commit or rollback, and every lock acquired during that window is held until it does.

You might not explicitly issue a `BEGIN` if you're using a framework, but the framework will do this on your behalf.

> Contention occurs when two different transactions need locks on the same data at the same time. Writes are the most common cause, but reads can cause it too via `SELECT FOR UPDATE`, or under isolation levels that require locks.

The exact behavior depends on your database, but here's a common failure pattern. Two different APIs both update the same row, each on its own database connection:

- API #1 issues an update ... _and does NOT commit_
- API #1 calls API #2
- API #2 issues an update ... _a timeout occurs waiting for a lock_

Why does this happen?

- Each API opens its own **database connection** and starts its own **transaction**.
- Both transactions attempt to acquire locks on the same data, held until **commit**.
- API #1 can't commit until API #2 returns, and API #2 can't proceed until API #1's lock is released.

Situations like this are why poor application design is the first candidate for causing deadlocks or timeouts. There are many variations on this scenario, and most cannot be resolved by your DBA.

While your DBA may be able to reduce contention in some situations via indexes or other optimizations, good application design is the only way to reliably avoid contention.

This scenario sounds contrived until you've seen it in production. Regularly. Frameworks, triggers, and stored procedures can hide transaction boundaries and surprise even experienced engineers. Call it the **API chain trap**: any time one API calls another within an open transaction, you've created the conditions for this failure.

### Frameworks

If you are using an Object Relational Mapping (ORM) or database persistence framework, you need to understand how it manages _transactions_ within the database.

- When are transactions initiated and committed?
- Does your framework ever create nested or independent secondary transactions?

With behavior like this, an outer transaction can acquire locks that an inner or secondary transaction may have to wait on to be released. The dilemma is that when a secondary transaction is initiated, the first one is suspended. So it cannot release locks until the new connection returns.

One example is Spring's `@Transactional` annotation when using `REQUIRES_NEW` propagation. Under the hood, this actually requests a completely new database connection from the pool to start an independent transaction while suspending the current one. There are times this is appropriate, but it makes transaction boundaries harder to reason about and can exhaust connection pools. Think twice before you reach for it.

### Database Triggers and Routines

Triggers and routines are another source of hidden functionality. While they are normally part of the calling application's transaction, they represent code that can modify the database in ways that aren't visible in your application layer.

Triggers are database objects that "fire" on certain events. For example, you can create a trigger to insert into a history table when a table is modified. Those triggers might call database routines, or may have inline routines to make changes directly to the database. Triggers are normally defined by DBAs.

Database routines are functions and stored procedures that can be called to make changes within the database. They represent code external to the main application that is installed within the database and callable by one or more applications. These routines are often written by a smaller subset of developers, or may be maintained by your DBA.

Because the individuals with knowledge of how triggers and routines work are frequently not the developers writing your business logic, their functionality is typically hidden from team members not familiar with them. This can lead to issues in application design.

This is also an organizational problem. When more than one team owns business logic spread across multiple application layers, different teams will have different priorities and knowledge about your system. A trigger written by a DBA team to enforce a business rule may silently conflict with a change made by a product team that had no visibility into it.

Your DBA and product teams will likely have different release cadences, priorities, and understanding. DBAs are not experts on business rules and will take guidance from product teams on what to implement, but product teams are not database experts and may not understand the side effects of what they are requesting. While this is workable through discussions, it will take more work for both teams to understand the context and consequences of changes.

> A trigger written by a DBA team and a change made by a product team can conflict silently. Neither team did anything wrong. The system just wasn't designed for shared ownership of business logic.

In our contrived locking example, it is possible that the developers were not modifying the same item in the database _directly_ in their code. The change to the same database item could have been caused by a trigger updating a table common to both APIs.

Triggers and routines are sometimes the right tool. Performance, auditing, and data integrity are legitimate reasons to reach for them. But they also increase coupling and coordination costs across teams.

Database contention leads to outages more often than it should. Business logic hidden in the database layer makes contention harder to spot and harder to fix. The way out is shared understanding and disciplined reporting.

## When It Really Is the Database

Not every problem is an application problem. Databases do fail in ways that have nothing to do with your code.

A query plan can degrade after a large data load causes statistics to go stale. An index can fragment under heavy write load due to page splits. A configuration change by your operations team ... a memory limit, a timeout setting, changes that increase network latency ... can shift behavior without touching a single line of application code. In a shared environment, a noisy neighbor can saturate CPU, storage, or connection limits and affect every team using that database at once.

The pattern is usually what tells you which side the problem is on. Use the **shared resource test**: if performance degrades for multiple callers simultaneously with no recent deployment, the problem is likely the database or infrastructure. If a single caller hits an error after a release, or a timeout only appears when two specific APIs run together, the problem is likely the application.

> If the behavior is consistent and reproducible with no recent change on your side, that is a strong signal to involve your DBA sooner rather than later.

The same information that helps you diagnose the problem helps your DBA start in the right place when you need to escalate.

## Links

- [Prepare, Investigate, Report](/blog/2023/prepare-investigate-report/) - a framework for debugging and reporting database issues (Database Collaboration, Part 1)
- [Distributed Transactions](/blog/2025/transactions/) - transaction strategies, locking tradeoffs, and failure behavior across systems
- [Feedly Top Database Blogs](https://feedly.com/i/top/database-blogs) - curated list of database engineering blogs
- [Use The Index, Luke!](https://use-the-index-luke.com/) - practical indexing and query performance guidance
- [PostgreSQL EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html) - how to inspect query plans
