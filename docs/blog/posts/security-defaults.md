---
title: "Security Defaults"
date: 2023-08-28
authors:
  - grobauskas
categories:
  - Security
  - Database
---

Security access controls extend into your databases. The principle of least privilege needs to be enforced not only for who can connect but also for what they can do within your databases.

For example, until PostgreSQL version 15, PUBLIC (which all users are a member of) could create tables within the public schema unless REVOKE’d. This is just one example.

It’s important to review what the security defaults are for your database product to ensure you are enforcing the least privilege access model where you explicitly grant access to resources.

[PostgreSQL 15.0 Release Notes](https://www.postgresql.org/docs/release/15.0/)
