---
title: "Working with Your Database Team"
description: "How software engineers and database teams work together effectively."
author: "Chris Grobauskas"
date: "2023-12-02"
updated: "2026-03-07"
tags:
  - Database
  - Teams
---

This is a two-part series on how software engineers and database teams work together effectively.

<!-- more -->

Good database collaboration starts with developers who can debug common issues independently and escalate the hard ones with enough evidence to act. When things get harder ... deadlocks, timeouts, hidden triggers ... the problem usually lives in your application code, not the database.

- [Prepare, Investigate, Report](/blog/2023/prepare-investigate-report/) - a framework for debugging database issues independently, reporting with evidence, and knowing when to escalate
- [Database Contention Is an Application Problem](/blog/2023/database-contention/) - why deadlocks and timeouts usually trace back to application design: transactions, locks, frameworks, and triggers
