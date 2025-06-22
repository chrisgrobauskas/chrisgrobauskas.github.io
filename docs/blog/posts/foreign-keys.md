---
title: Foreign Keys
date: 
  created: 2024-12-22
authors: 
  - grobauskas
categories:
  - Database
---

I learned something new today about Postgres!

Laurenz Albe’s blog post on how you can break foreign keys in Postgres includes the tidbit that BEFORE triggers that return NULL can stop enforcement of foreign keys.

While I knew system triggers enforced referential integrity in Postgres, I had not considered the consequences of BEFORE triggers with that feature.

Learn more from Laurenz Albe here:

[Broken Foreign Keys in Postgres](https://www.cybertec-postgresql.com/en/broken-foreign-keys-postgresql/)