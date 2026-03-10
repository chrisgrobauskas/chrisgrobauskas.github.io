---
title: "Prepare, Investigate, Report"
description: "A framework for working with your database team: show up prepared, debug independently, and report with evidence. (Database Collaboration, Part 1)"
author: "Chris Grobauskas"
date: "2023-12-02"
updated: "2026-03-07"
tags:
  - Database
  - Teams
---

If your "database ticket" says "it's slow" or "it timed out," you're not asking for help ... you're asking someone else to guess.

I've watched good database engineers (DBAs) lose days to vague reports that are basically "something happened" with a request for help. Not because teams are careless, but because nobody taught them what DBAs actually need to investigate: the query, the error, the timing, and the context.

DBAs want to be helpful. But their expertise is best used when developers can solve common issues independently and escalate the non-obvious ones with enough evidence to act.

> The fastest way to get database help is to show up prepared: query + full error + timestamp + environment + what changed.

<!-- more -->

## The Framework

I think about working with database teams as a simple framework: **Prepare, Investigate, Report**.

The point isn't to turn every developer into a DBA. It's to stop treating the database like a black box. When you understand how your database behaves, you write better code, you debug faster, and you know when you're holding a lock across an API call.

### Prepare

How do you prepare for an issue? You read one good book for your chosen database, subscribe to a few database blogs, and experiment in a sandbox where you can break things safely.

> Learning is how you prepare to handle issues.

You need to understand what your database will do with your queries. Learn how transactions and locking work. Learn what an index actually changes. As a stretch goal, learn how to run `EXPLAIN` (or your database's equivalent) so you can see the plan that will be used.

Also learn how to view table and index definitions for your database. It keeps you from guessing about schema, keys, and constraints while you're trying to debug. And for some errors, it's the key to solving problems on your own (missing table, column, or wrong datatype).

Beyond transactions and indexes, there are a few practical skills worth building before you need them:

- **Catalog tables:** The same tool you use to query your database can usually describe objects using catalog tables. Those tables contain metadata about the database: tables, indexes, columns, types, foreign keys, triggers, procedures, functions, and more.
- **Schema inspection:** Tools like [DBeaver](https://dbeaver.io/) can format catalog results into a tree view or DDL (data definition language), which is faster than querying catalogs directly.
- **Error logging:** Know how to capture and log SQL error messages in a way that lets you find them again. You will need this.

### Investigate

Try to make progress independently first. Most database issues aren't "database issues" ... they're application behavior running into rules enforced by the database. Primary keys and unique indexes blocking duplicates. Column data types blocking storing the wrong type or length of data. Locking enforcing isolation between concurrent transactions. Or maybe your insert is firing a trigger someone added to prevent orphaned rows in a related table.

Start with the error itself. Look for an SQLSTATE/SQLCODE, error code, or constraint name. Those details usually tell you whether you're looking at syntax, permissions, data integrity, deadlocks, timeouts, or a resource limit. Both are easily searchable.

Digging into errors will make you a better developer. You'll learn what's wrong with your code and how to avoid the same class of error next time. A team that investigates independently escalates less and resolves faster.

### Report

If you need help, be a good reporter. Include:

- **W**ho (ID)
- **W**hat (full error message and SQL)
- **W**hen (date/time in UTC)
- **W**here (host and database name)

If you include these, you make it possible to answer the fifth "W" ... **Why?**

It's fair to say this feels like paperwork, but the alternative is worse: a wild goose chase with everyone guessing what to look at.

## Before You Escalate

If you're about to contact your database team, ask yourself:

- Do I have the exact SQL and parameters that ran?
- If there was an error, do I have the full error, and have I tried looking up the SQLCODE/SQLSTATE?
- Do I know the transaction boundary ... where it begins and where it commits?
- Do I have an `EXPLAIN` plan (or at least row counts and indexes involved)?
- Do I have a timestamp and environment?
- Did anything change ... not whether anything _you think_ is related changed, but whether _anything_ changed.

If you can answer those, you won't just get faster help. You'll often solve the problem yourself.

> A DBA who receives a well-prepared report can start investigating immediately. One who receives "it's slow" has to ask five questions before they can even begin.

The framework here covers the self-service side. But when things get harder ... deadlocks, timeouts, hidden triggers ... the problem is usually [contention, and it lives in your application code](/blog/2023/database-contention/).

## Links

- [Database Contention Is an Application Problem](/blog/2023/database-contention/) - why deadlocks and timeouts usually trace back to application design (Database Collaboration, Part 2)
- [Feedly Top Database Blogs](https://feedly.com/i/top/database-blogs) - curated list of database engineering blogs
- [Use The Index, Luke!](https://use-the-index-luke.com/) - practical indexing and query performance guidance
- [PostgreSQL EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html) - how to inspect query plans
