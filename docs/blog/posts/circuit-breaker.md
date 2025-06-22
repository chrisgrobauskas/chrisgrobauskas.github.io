---
title: Circuit Breaker Pattern
date: 
  created: 2025-03-23
authors: 
  - grobauskas
categories:
  - Design
---

Imagine forgetting your electric tea kettle was on. No big deal ... it shuts itself off when it senses danger, like potentially burning your house down. This is the circuit breaker pattern in action.

<!-- more -->

When a service starts failing, you don't keep hammering it. Instead, you back off, stop calling it for a while, and let it recover.

Simple, right? Well, as with most things in engineering, it depends.

- Should my kettle retry a few times before giving up? Nope. In this case, retrying is dangerous. But for a network request? Maybe! That’s max retries with exponential backoff giving a service time to recover without making things worse.

- What if my kettle completely fails? Do I just give up on tea? Of course not. I grab a pot and boil water on the stove, or I make coffee. That’s a fallback strategy like calling a secondary service, serving cached data, or skipping a step if it’s not critical.

So, should your system trip a circuit breaker and stop retrying? It depends. On the failure mode, the risk, and the alternatives. Context matters.

My tea kettle gets it. Maybe our systems should too?