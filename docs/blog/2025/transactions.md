---
title: "Distributed Transactions"
description: "Your transaction strategy defines your failure behavior. Understanding the tradeoffs between 2PC, sagas, and compensating transactions matters more than picking a favorite."
author: "Chris Grobauskas"
date: "2025-03-21"
tags:
  - Architecture
  - Design
  - Database
---
# Distributed Transactions

Transactions in a single database are well-understood. Transactions across databases, queues, and external services are not. The failure modes are different, the guarantees are weaker, and the abstractions your framework provides often hide what's actually happening.

<!-- more -->

## Common Pitfalls

- Rollback means everything is undone: Not for external calls or side effects.
- It's all or nothing: Only if a single system is involved. Across databases and queues, you need [two-phase commit (2PC)](https://martinfowler.com/articles/patterns-of-distributed-systems/two-phase-commit.html), compensating transactions, or robust retry.
- 2PC is better: 2PC means simpler code but requires full protocol support from all participants. The coordinator is also a single point of failure, and under failure conditions it holds locks across all participating systems until the outcome is resolved. That's why the industry has largely moved away from it in loosely coupled distributed systems. Inside controlled boundaries where the platform supports the protocol natively, the tradeoffs look very different.
- Compensating transactions are better: While they reduce coupling, they also require significantly more error handling and introduce eventual consistency. For some business workflows, compensation carries real risk ... you can't un-notify a customer. If a payment already went out, all you can do is issue a stop payment, which looks to the customer like you don't know what you're doing.
- Sagas are simple: The [saga pattern](https://microservices.io/patterns/data/saga.html) (choreography or orchestration) gives you a structured way to coordinate compensating transactions across services. But sagas trade atomicity for availability. Every step needs a defined rollback path, and failure handling must be explicit and tested, which means more coding and testing for the same outcomes.
- Nested transactions are simple: Nope. They cause unexpected locking and failure behavior. In longer-lived codebases they often surprise engineers who do not know they are there.

## What Engineers Should Focus On

- Understand what the behavior is for your storage engine for transactions, isolation, rollback, message delivery, and retry.
- Test error handling for all failure scenarios, including partial failures and retries.
- Handle side effects explicitly. The [outbox pattern](https://microservices.io/patterns/data/transactional-outbox.html) (write the side effect to a local table in the same transaction, then process it asynchronously) is a reliable approach. [Idempotent](https://en.wikipedia.org/wiki/Idempotence) operations (those that produce the same result no matter how many times they run) ensure retries don't cause duplicate effects.
- Avoid external calls in transactions if possible. These can make transactions run longer and have external side effects.
- Keep transactions fast and small to reduce database contention and locking issues.
- Pick the strategy that fits your system. 2PC works well inside controlled boundaries. Compensating transactions and sagas work better across independently deployed services. Eventual consistency is acceptable for some use cases and unacceptable for others. Know which situation you're in.

> Your transaction strategy defines your failure behavior. Pick it deliberately, test the failure modes, and design the boundaries between different strategies with the same care you give the strategies themselves.

## Bottom Line

The strategy you choose for distributed transactions shapes your system's failure behavior under load. Assumptions that hold in development will break in production if you haven't tested partial failures, retries, and rollback paths explicitly. When systems mix strategies (2PC internally, eventual consistency across services), the boundary between those models requires its own careful design. Pick the right tool for your context, understand its failure modes, and test for them.

## Links

- [Two-Phase Commit - Martin Fowler](https://martinfowler.com/articles/patterns-of-distributed-systems/two-phase-commit.html) - the protocol, its guarantees, and its failure modes
- [Saga Pattern - microservices.io](https://microservices.io/patterns/data/saga.html) - choreography and orchestration for distributed workflows
- [Transactional Outbox - microservices.io](https://microservices.io/patterns/data/transactional-outbox.html) - reliable side-effect handling
<!-- - [Microservices and Microliths](2026/microservices) - how these tradeoffs play out in architectural decisions -->