---
layout: post
title:  "Expectations"
date:   2023-12-03 10:00:00 -0600
categories: teams
---
“If you give a man a fish, you feed him for a day. If you teach a man to fish, you feed him for a lifetime.” ~ Anonymous

# Expectations
Three things you should not expect your database administrator, engineer, or magician to do:

1) Make “the database” work the way you *think* it works.
2) Teach you how to use Google to answer what a particular SQL error means.
3) Magically make database contention go away.

Instead, as a developer or engineer, you should:

📖 Read a good introductory book for your chosen database, subscribe to database blogs, or (heaven forbid!) look at a manual. You need to understand what your database will do with your queries. You should also learn how to view the table and index definitions for your database.

🔎 Follow the “15-minute rule” and attempt to find the answer to your question about SQL errors independently for at least 15 minutes. Most can be answered using Google and are not “database issues”.

📰 If you need help, please be a good reporter and include: who (ID), what (full error message and SQL), when (date/time in UTC), and where (host and database name). If you include these, you will find out the last of the “5 Ws” … why.

👉 Accept that application design is the first candidate for causing deadlocks or timeouts. While your database administrator or engineer may be able to do something to *reduce* contention, good application design is the only way to avoid contention.