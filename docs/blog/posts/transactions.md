---
title: Distributed Transactions
date: 
  created: 2025-03-21
authors: 
  - grobauskas
categories:
  - Database
---

Most engineers think they understand transactions until they deal with distributed systems, different storage engines, or frameworks that abstract too much. 

<!-- more -->

## Common Pitfalls

- Rollback means everything is undone: Not for external calls or side effects.
- It’s all or nothing: Only if a single system is involved. Across databases and queues, you need two-phase commit (2PC) or compensating transactions and/or robust retry.
- 2PC is better: 2PC means simpler code but requires full protocol support from all participants and has performance implications.
- Compensating transactions are better: While they reduce coupling, they also require more error handling and introduce eventual consistency.
- Nested transactions are simple: Nope. They cause unexpected locking and failure behavior. In longer lived code bases they often surprise engineers who do not know they are there.

## What Engineers Should Focus On

- Understand what the behavior is for your storage engine for transactions, isolation, rollback, message delivery, and retry.
- Test error handling for all failure scenarios, including partial failures and retries.
- Handle side effects explicitly with patterns like the outbox pattern and idempotent operations.
- Avoid external calls in transactions if possible. These can make transactions run longer and have external side effects.
- Keep transactions fast and small to reduce database contention and locking issues.
- Pick a strategy that works for YOUR system based on trade-offs. Don’t make it a “religious” decision. There are environments where 2PC will work well, and eventual consistency is OK for some use cases.

## Bottom Line

Transactions aren’t magic. If you don’t deeply understand how they work in your system, assumptions will break under load and failure. 

Choose what is best for your system, whether compensating transactions or 2PC, and test for failure conditions.