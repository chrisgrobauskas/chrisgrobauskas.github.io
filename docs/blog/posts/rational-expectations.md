---
title: Rational Expectations
date: 
  created: 2023-12-02
authors: 
  - grobauskas
categories:
  - Database
  - Teams
---
"If you give a man a fish, you feed him for a day. If you teach a man to fish, you feed him for a lifetime." ~ Anonymous 

While database engineers (and administrators) want to be helpful and answer questions, you should not expect your database engineer to:

1. Make “the database” work the way you *think* it works.
2. Teach you how to use Google to answer what a particular SQL error means.
3. Magically make database contention go away.

<!-- more -->

## Prepare, Investigate, Report
It is important for software engineers to have some knowledge about "the database" to be able to do their work effectively and efficiently.

Software Engineers should prepare for, investigate, and report issues correctly.

📖 **Prepare**

How do you prepare for an issue? You read a good book for your chosen database, subscribe to database blogs, or (heaven forbid!) look at a manual. If video or audio is your preferred media, find training videos or podcasts. Or experiment!

> Learning is how you prepare to handle issues.

You need to understand what your database will do with your queries. Learn how transactions and locking work within your database. As a stretch goal, learn how to "explain" the queries you are using to find out the plan that will be followed when the database evaluates one.

Moreover, learn how to view the table and index definitions for your database. This allows you to easily find current information about the database while programming or investigating errors.

The same tool you are using to query your database can describe objects within the database using catalog tables. Catalog tables contain meta-data about the database including lists of tables, indexes, columns, data types, foreign keys, triggers, procedures, functions, etc.

While you can query these catalog tables directly, tools like DBeaver can format this data into a tree view or DDL (data definition language).

Of course, you should also know how to catch, log, and view SQL error messages.

🔎 **Investigate**

Follow the “15-minute rule” with errors and attempt to find the answer to your question independently for at least 15 minutes. Most can be answered using Google and are not “database issues”.

You should look at SQL errors to find an SQL code, state, error, or warning. You will find something you can search on Google. 

Digging into errors to understand them on your own will help you be a better developer. You will learn not only what is wrong with your code, but how to avoid the issue in the future!

📰 **Report**

If you need help, please be a good reporter and include: 

- **W**ho (ID)
- **W**hat (full error message and SQL)
- **W**hen (date/time in UTC)
- **W**here (host and database name)

If you include these in your report, you will find out the last of the “5 **W**s” … **W**hy?

## Database Contention
A particularly vexing question for database engineers is database contention. 

> Database contention is vexing because it is normally NOT a database issue!

The most likely cause of database contention is poor application design due to a lack of understanding how the database will run a particular workload.

### Units of Work
The relevant concept is a “unit of work” within the database. A unit of work contains all the changes for a given database “transaction” during the time span from the first change (insert, update, delete, merge) to the point where you (or a framework you use) commits those changes.

Actually, the term transaction is probably used by itself more these days, but I wanted to mention both as you will see both terms in blogs and journals.

> Contention occurs when two different transactions are updating the same item(s) within the database at the same time.

Let's assume you have two methods in two different web services. These APIs (Application Programming Interfaces) both update the **same item** in the database:

- API #1 issues an update … *and does NOT commit*
- API #1 calls API #2
- API #2 issues an update … *a timeout occurs waiting for a lock*

Why did this happen?

- Both APIs connect to the **database**.
- Both APIs start a database **transaction**.
- Both APIs attempt to acquire locks held until **commit**.

### Lock Contention
What does the locking look like in this scenario?

- API #1 will acquire a lock and does not commit.
- API #1 retains its lock and calls API #2.
- API #2 will attempt to acquire a lock on the same data and will wait on #1 to commit.
- API #2 will eventually hit a timeout (we hope).

Situations like this are why poor application design is the first candidate for causing deadlocks or timeouts. There are many variations on this scenario, and most cannot be resolved by your database engineer.

While your database engineer may be able to do something to *reduce* contention in some situations, good application design is the only way to avoid contention.

The scenario above might seem contrived, but it is a common scenario even experienced software engineers stumble into when frameworks, database triggers, or database routines hide or obfuscate what is going on in the database.

### Frameworks
If you are using an Object Relational Mapping (ORM) or database persistence framework, you need to understand how it manages *transactions* within the database. 

- When are transactions initiated and committed?  
- Does your framework ever create sub-transactions?

With a sub-transaction, the parent transaction can acquire locks that a child sub-transaction may have to wait on to be released. The dilemma is that when a sub-transaction is initiated, the parent is suspended. So it cannot release locks until the child returns.

One example of this is Spring JDBC when using REQUIRES_NEW, but the situation is not limited to Spring, or JDBC. While there can be cases where sub-transactions are appropriate, it does make reasoning about transaction boundaries more difficult. Think twice before using sub-transactions.

### Database Triggers and Routines
Another place with hidden functionality is within database triggers and routines. While called triggers and routines are normally part of the calling application's transaction, they represent "hidden code" that can modify the database. 

Triggers are database objects that "fire" on certain events. For example, you can create a trigger to insert into a history table when a table is modified. Those triggers might call database routines, or may have inline routines to make changes directly to the database. Triggers are normally defined by database administrators.

Database routines are functions and stored procedures that can be called to make changes within the database. They represent code external to the main application that is installed within the database and callable by one or more applications. These routines are often written by a smaller subset of developers, or may be maintained by your database administrator.

Because the individuals with knowledge of how triggers and routines work are frequently not the developers writing your business logic, their functionality is typically hidden from team members not familiar with them. This can lead to issues in application design. 

In our contrived locking example, it is possible that the developers were not modifying the same item in the database *directly* in their code. The change to the same database item could have been caused by a trigger updating a table common to both APIs.

There are cases where triggers and routines are needed for performance, auditing, or data integrity.

To tell if your code base makes use of them, you should be able to view them in the same tool you run SQL. As long as the routines are written in a flavor of SQL/PL you should be able to view them, but some databases allow external procedures written in C, COBOL, etc. In those cases, you would want to speak with your database administrator to find out where the code for those is located.

Database triggers and routines bring us full circle. These are items that you may need your database administrator's help to understand.  However, you should know if they exist and what they do to make good design choices.

## Closing Thoughts
It is not uncommon for database contention to lead to system outages. Work to avoid that in your code by seeking understanding.

Try to start learning more by subscribing to a top database blog: [Feedly Top Database Blogs](https://feedly.com/i/top/database-blogs)