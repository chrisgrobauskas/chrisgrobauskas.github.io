---
title: "Working with Your Database Team"
description: "How software engineers and database teams work together effectively through preparation, investigation, and clear reporting."
author: "Chris Grobauskas"
date: "2023-12-02"
updated: "2026-02-27"
tags:
  - Database
  - Teams
---

# Working with Your Database Team

If your "database ticket" says "it's slow" or "it timed out," you're not asking for help ... you're asking someone else to guess.

I've watched good database engineers lose days to vague reports that are basically "something happened" with a request for help. Not because teams are careless, but because nobody taught them what DBAs actually need to investigate: the query, the error, the timing, and the context.

Database engineers want to be helpful. But their expertise is best used when developers can solve common issues independently and escalate the non-obvious ones with enough evidence to act.

> The fastest way to get database help is to show up prepared: query + full error + timestamp + environment + what changed.

<!-- more -->

## Prepare, Investigate, Report

I think about working with database teams as a simple framework: **Prepare, Investigate, Report**.

The point isn't to turn every developer into a database engineer. It's to stop treating the database like a black box. When you understand how your database behaves, you write better code, you debug faster, and you know when you're holding a lock across an API call.

### Prepare

How do you prepare for an issue? You read one good book for your chosen database, subscribe to a few database blogs, and experiment in a sandbox where you can break things safely.

> Learning is how you prepare to handle issues.

You need to understand what your database will do with your queries. Learn how transactions and locking work. Learn what an index actually changes. As a stretch goal, learn how to run `EXPLAIN` (or your database's equivalent) so you can see the plan that will be used.

Also learn how to view table and index definitions for your database. It keeps you from guessing about schema, keys, and constraints while you're trying to debug. And for some errors it's the key to solving problems on your own (missing table, column, or wrong datatype).

The same tool you use to query your database can usually describe objects using catalog tables. Those catalog tables contain metadata about the database: tables, indexes, columns, types, foreign keys, triggers, procedures, functions, and more.

While you can query these catalog tables directly, tools like DBeaver can format the results into a tree view or DDL (data definition language).

You should also know how to capture and log SQL error messages in a way that lets you find them again.

### Investigate

Try to make progress independently first. Most database issues aren't "database issues" ... they're application behavior running into rules enforced by the database. Primary keys and unique indexes blocking duplicates. Column data types blocking storing the wrong type or length of data. Locking ensuring that your transactions remain atomic, consistent, isolated, and durable (ACID). Or maybe your insert is firing a trigger a former co-worker requested to ensure that there are no orphaned rows without parents in other tables.

Start with the error itself. Look for an SQLSTATE/SQLCODE, error code, or constraint name. Those details usually tell you whether you're looking at syntax, permissions, data integrity, deadlocks, timeouts, or a resource limit. And they are easily searched for on Google.

Digging into errors will make you a better developer. You'll learn what's wrong with your code and how to avoid the same class of error next time.

### Report

If you need help, be a good reporter. Include:

- **W**ho (ID)
- **W**hat (full error message and SQL)
- **W**hen (date/time in UTC)
- **W**here (host and database name)

If you include these, you make it possible to answer the fifth "W" ... **Why?**

It's fair to say this feels like paperwork, but the alternative is worse: a wild goose chase with everyone guessing what to look at.

## Database Contention

A particularly vexing question for database engineers and administrators is contention.

> Database contention is vexing because its roots are often in the application code, not the database itself.

The most common cause is application design that doesn't account for how the database enforces isolation. When you hold locks for too long, the database is doing what you asked. Deadlocks are almost always an application design issue, and timeouts normally are too.

### Units of Work

The relevant concept is a "unit of work" ... what most of us now just call a transaction. It spans from the first write (insert, update, delete, merge) to the commit.

> Contention occurs when two different transactions are updating the same item(s) within the database at the same time.

Here's a common failure pattern. Two different APIs both update the same row:

- API #1 issues an update ... _and does NOT commit_
- API #1 calls API #2
- API #2 issues an update ... _a timeout occurs waiting for a lock_

Why does this happen?

- Both APIs connect to the **database**.
- Both APIs start a database **transaction**.
- Both APIs attempt to acquire locks held until **commit**.

### Lock Contention

What does the locking look like in this scenario?

- API #1 will acquire a lock and does not commit.
- API #1 retains its lock and calls API #2.
- API #2 will attempt to acquire a lock on the same data and will wait on #1 to commit.
- API #2 will eventually hit a timeout (we hope).

Situations like this are why poor application design is the first candidate for causing deadlocks or timeouts. There are many variations on this scenario, and most cannot be resolved by your database engineer.

While your database engineer may be able to reduce contention in some situations via indexes or other optimizations, good application design is the only way to reliably avoid contention.

This scenario sounds contrived until you've seen it in production, regularly. Frameworks, triggers, and stored procedures can hide transaction boundaries and surprise even experienced engineers.

### Frameworks

If you are using an Object Relational Mapping (ORM) or database persistence framework, you need to understand how it manages _transactions_ within the database.

- When are transactions initiated and committed?
- Does your framework ever create nested or independent secondary transactions?

With behavior like this, an outer transaction can acquire locks that an inner or secondary transaction may have to wait on to be released. The dilemma is that when a secondary transaction is initiated, the first one is suspended. So it cannot release locks until the new connection returns.

One example is Spring JDBC when using `REQUIRES_NEW`. Under the hood, this actually requests a completely new database connection from the pool to start an independent transaction while suspending the current one. There are times this is appropriate, but it makes transaction boundaries harder to reason about and can exhaust connection pools. Think twice before you reach for it.

### Database Triggers and Routines

Triggers and routines are another source of hidden functionality. While they are normally part of the calling application's transaction, they represent code that can modify the database in ways that aren't visible in your application layer.

Triggers are database objects that "fire" on certain events. For example, you can create a trigger to insert into a history table when a table is modified. Those triggers might call database routines, or may have inline routines to make changes directly to the database. Triggers are normally defined by database administrators.

Database routines are functions and stored procedures that can be called to make changes within the database. They represent code external to the main application that is installed within the database and callable by one or more applications. These routines are often written by a smaller subset of developers, or may be maintained by your database administrator.

Because the individuals with knowledge of how triggers and routines work are frequently not the developers writing your business logic, their functionality is typically hidden from team members not familiar with them. This can lead to issues in application design.

This is also an organizational problem. When more than one team owns business logic spread across multiple application layers, different teams will have different priorities and knowledge about your system. A trigger written by a DBA team to enforce a business rule may silently conflict with a change made by a product team that had no visibility into it.

Your DBA and product teams will likely have different release cadences, priorities, and understanding. DBAs are not experts on business rules and will take guidance from product teams on what to implement, but product teams are not database experts and may not understand the side effects of what they are requesting. While this is workable through discussions, it will take more work for both teams to understand the context and consequences of changes.

> Even with discussion, there is a gap between teams that can lead to design risks, extra work, and production outages that are easily avoidable if you have all the context.

In our contrived locking example, it is possible that the developers were not modifying the same item in the database _directly_ in their code. The change to the same database item could have been caused by a trigger updating a table common to both APIs.

Triggers and routines are sometimes the right tool. Performance, auditing, and data integrity are legitimate reasons to reach for them. But they also increase coupling and coordination costs across teams.

Database contention leads to outages more often than it should. Business logic hidden in the database layer makes contention harder to spot and harder to fix. The way out is shared understanding and disciplined reporting.

## When It Really Is the Database

Not every problem is an application problem. Databases do fail in ways that have nothing to do with your code.

A query plan can degrade after a large data load causes statistics to go stale. An index can fragment under heavy write load due to page splits. A configuration change by your operations team ... a memory limit, a timeout setting, an isolation level ... can shift behavior without touching a single line of application code. In a shared environment, a noisy neighbor can saturate CPU, storage, or connection limits and affect every team using that database at once.

The pattern is usually what tells you which side the problem is on. Performance degradation that hits multiple callers simultaneously with no recent deployment points toward the database or infrastructure. A single caller hitting an error after a release, or a timeout that only appears when two specific APIs run together, points toward the application.

> If the behavior is consistent and reproducible with no recent change on your side, that is a strong signal to involve your DBA sooner rather than later.

The framework above handles both cases. The same information that helps you diagnose the problem helps your DBA start in the right place when you need to escalate.

## Before You Escalate

If you're about to contact your database team, ask yourself:

- Do I have the exact SQL and parameters that ran?
- If there was an error, do I have the full error, and have I tried looking up the SQLCODE/SQLSTATE?
- Do I know the transaction boundary ... where it begins and where it commits?
- Do I have an `EXPLAIN` plan (or at least row counts and indexes involved)?
- Do I have a timestamp and environment?
- Did anything change ... not whether anything _you think_ is related changed, but whether _anything_ changed.

If you can answer those, you won't just get faster help. You'll often solve the problem yourself.

## Links

- [Feedly Top Database Blogs](https://feedly.com/i/top/database-blogs) - curated list of database engineering blogs
- [Use The Index, Luke!](https://use-the-index-luke.com/) - practical indexing and query performance guidance
- [PostgreSQL EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html) - how to inspect query plans
