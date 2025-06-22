---
title: Microservices & Shared Data
date: 
  created: 2025-03-25
authors: 
  - grobauskas
categories:
  - Database
  - Design
---


# Microservices: The Data Ownership Trap

Microservices promise agility and scalability, but there's a hidden pitfall that can derail your chosen architecture: shared data.

<!-- more -->

## The Silent Killer: Shared Tables

Splitting your application into services isn't enough. If your services are still reaching into shared database tables, you're not building a true microservices architecture.

### Red Flags to Watch Out For:

- Direct table access across services
- Pseudo-independent copies of tables within the same operational system
- Triggers creating bottlenecks on shared tables
- Legacy stored procedures spanning multiple services
- The dangerous "we'll fix it later" mentality

## The Fundamental Principle: Data Sovereignty

While there are exceptions, sharing tables across two or more microservices will create a tangled web of dependencies.

## The Path to True Microservices:

- **Strict data ownership:** Each service manages its own data.
- **API-first communication:** Services interact via APIs, not direct database access.
- **Team alignment:** Organize teams to match architectural boundaries (hello, Conway's Law!).

## The Bottom Line
Good data design always included clear boundaries around data access; this was equally true with monoliths. 

Things you might have gotten away with before, though … like direct data access to update a shared table across two services inside a monolith … will not work with microservices.

Microservices are complex. Your data boundaries must be as clear and intentional as your service boundaries.

