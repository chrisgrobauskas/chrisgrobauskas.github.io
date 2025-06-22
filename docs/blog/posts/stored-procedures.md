---
title: Stored Procedures
date: 
  created: 2024-05-02
authors: 
  - grobauskas
categories:
  - Database
  - Design
---
One valid use case for stored procedures in operational systems can be to reduce round trips to the database for some transactions. In (some) databases, it can also mean running compiled code close to the database. 

Both are more efficient in some cases, but it can also be more difficult to debug stored procedures than normal code.

<!-- more -->

Furthermore, after the person who wrote them moves on, stored procedures are often a “hidden” part of your code base. Not all developers will have experience with stored procedures.

- Do you find performance a compelling argument for stored procedures (in some cases)? 

- Do you agree stored procedures are frequently “hidden code” less understood by the average developer?