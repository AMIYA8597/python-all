# Databases: SQL vs NoSQL, ACID, Indexing, and Joins

## Prerequisites
- Basic understanding of data structures (arrays, dictionaries/hash maps).
- Familiarity with the concept of persistent storage (saving data to a disk).

## Objectives
- Understand the fundamental differences between SQL (Relational) and NoSQL (Non-Relational) databases.
- Grasp the ACID properties that guarantee reliable database transactions.
- Learn how database indexing works and why it is crucial for performance.
- Master the concept of SQL Joins to combine data from multiple tables.

## Intuition
Imagine you are running a library. 
- A **SQL Database** is like a meticulously organized card catalog where every book has a strict, predefined set of attributes (Title, Author, ISBN). If you want to add a book with a new attribute (e.g., "Audiobook Length"), you have to formally update the rules for the entire catalog.
- A **NoSQL Database** is like a flexible filing system. You can drop in a folder for a book, and another folder for a DVD, each containing completely different types of information. It's highly flexible and easy to scale across multiple filing cabinets.

## Core Concepts

### 1. SQL vs NoSQL
**SQL (Relational Databases):**
- **Structure:** Tabular (Rows and Columns).
- **Schema:** Rigid, schema-on-write. Data must fit the predefined structure.
- **Scaling:** Primarily vertically scalable (adding more CPU/RAM to a single server).
- **Examples:** PostgreSQL, MySQL, Oracle, SQL Server.
- **Best for:** Complex queries, transactional systems (finance, inventory), highly structured data.

**NoSQL (Non-Relational Databases):**
- **Structure:** Document-based (JSON), Key-Value, Column-family, or Graph.
- **Schema:** Flexible, dynamic schema.
- **Scaling:** Horizontally scalable (adding more servers to a cluster).
- **Examples:** MongoDB, Redis, Cassandra, Neo4j.
- **Best for:** Unstructured/semi-structured data, rapid prototyping, highly scalable applications, real-time big data.

### 2. ACID Properties
ACID is a set of properties of database transactions intended to guarantee data validity despite errors, power failures, or other mishaps.
- **Atomicity:** "All or nothing." A transaction is treated as a single, indivisible unit. If one part fails, the entire transaction fails, and the database state is left unchanged.
- **Consistency:** Ensures that a transaction can only bring the database from one valid state to another, maintaining all predefined rules (constraints, cascades, triggers).
- **Isolation:** Concurrent execution of transactions leaves the database in the same state that would have been obtained if the transactions were executed sequentially.
- **Durability:** Once a transaction has been committed, it will remain so, even in the event of a power loss, crashes, or errors (usually by writing to a transaction log).

### 3. Database Indexing
An index is a data structure (typically a B-Tree or Hash Table) that improves the speed of data retrieval operations on a database table at the cost of additional writes and storage space.
- **Analogy:** The index at the back of a textbook. Instead of reading every page (Full Table Scan) to find a topic, you look it up in the index to find the exact page number.
- **Clustered Index:** Defines the physical sorting order of the data in the table. A table can only have one clustered index (usually the Primary Key).
- **Non-Clustered Index:** A separate data structure that contains a copy of the indexed columns and a pointer to the actual data row.

### 4. SQL Joins
Joins are used to combine rows from two or more tables, based on a related column between them.
- **INNER JOIN:** Returns records that have matching values in both tables.
- **LEFT (OUTER) JOIN:** Returns all records from the left table, and the matched records from the right table.
- **RIGHT (OUTER) JOIN:** Returns all records from the right table, and the matched records from the left table.
- **FULL (OUTER) JOIN:** Returns all records when there is a match in either left or right table.
- **CROSS JOIN:** Returns the Cartesian product of the sets of records from the two tables.

## Code / SQL Examples

### SQL Tables and Joins
```sql
-- Create Users Table
CREATE TABLE Users (
    user_id INT PRIMARY KEY,
    username VARCHAR(50)
);

-- Create Orders Table
CREATE TABLE Orders (
    order_id INT PRIMARY KEY,
    user_id INT,
    amount DECIMAL(10, 2),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- INNER JOIN Example
SELECT Users.username, Orders.amount
FROM Users
INNER JOIN Orders ON Users.user_id = Orders.user_id;
```

### Indexing Example
```sql
-- Creating an index to speed up username lookups
CREATE INDEX idx_username ON Users(username);
```

## Summary
Databases are the foundation of data engineering and software development. Choosing between SQL and NoSQL depends on the strictness of your data schema and scalability requirements. Understanding ACID ensures data integrity, while Indexing and Joins are critical for efficient data retrieval.

## Interview Questions
1. **What is the difference between SQL and NoSQL?**
   *Answer:* SQL is relational, structured, and scales vertically. NoSQL is non-relational, flexible, and scales horizontally.
2. **Explain the ACID properties.**
   *Answer:* Atomicity (all or nothing), Consistency (valid state transitions), Isolation (concurrent transactions don't interfere), Durability (committed data is saved permanently).
3. **What is the difference between a clustered and non-clustered index?**
   *Answer:* A clustered index determines the physical order of data (only 1 per table). A non-clustered index is a separate structure pointing to the physical data (multiple allowed).
4. **Explain the difference between a LEFT JOIN and an INNER JOIN.**
   *Answer:* INNER JOIN returns only rows with a match in both tables. LEFT JOIN returns all rows from the left table, filling in NULLs for the right table if no match exists.
